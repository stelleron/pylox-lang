import lox
import expr
import environment
import scanner
import stmt
import ast_printer
import runtime_error

class Interpreter(expr.ExprVisitor, stmt.StmtVisitor):
    def __init__(self):
        self.environment = environment.Environment()

    def visitLiteral(self, obj):
        return obj.value
    
    def visitGrouping(self, obj):
        return self.evaluate(obj.expression)
    
    def visitUnary(self, obj):
        right = self.evaluate(obj.right)
        if (obj.operator.type == scanner.TokenType.BANG):
            return not(self.is_truthy(right))
        elif (obj.operator.type == scanner.TokenType.MINUS):
            self.check_number_operand(obj.operator, right)
            return -float(right)
        return None
            
    def visitBinary(self, obj):
        left = self.evaluate(obj.left)
        right = self.evaluate(obj.right)

        if (obj.operator.type == scanner.TokenType.PLUS):
            if (type(left) == float and type(right) == float):
                return float(left) + float(right)
            elif (type(left) == str and type(right) == str):
                return str(left) + str(right)
            raise runtime_error.LoxRuntimeError(obj.operator, "Operands must be two numbers or two strings")
        elif (obj.operator.type == scanner.TokenType.MINUS):
            self.check_number_operands(obj.operator, left, right)
            return float(left) - float(right)
        elif (obj.operator.type == scanner.TokenType.STAR):
            self.check_number_operands(obj.operator, left, right)
            return float(left) * float(right)
        elif (obj.operator.type == scanner.TokenType.SLASH):
            self.check_number_operands(obj.operator, left, right)
            return float(left) / float(right)
        elif (obj.operator.type == scanner.TokenType.GREATER):
            self.check_number_operands(obj.operator, left, right)
            return float(left) > float(right)
        elif (obj.operator.type == scanner.TokenType.GREATER_EQUAL):
            self.check_number_operands(obj.operator, left, right)
            return float(left) >= float(right)
        elif (obj.operator.type == scanner.TokenType.LESS):
            self.check_number_operands(obj.operator, left, right)
            return float(left) < float(right)
        elif (obj.operator.type == scanner.TokenType.LESS_EQUAL):
            self.check_number_operands(obj.operator, left, right)
            return float(left) <= float(right)
        elif (obj.operator.type == scanner.TokenType.EQUAL_EQUAL):
            return (left == right)
        elif (obj.operator.type == scanner.TokenType.BANG_EQUAL):
            return not(left == right)
        
    def visitAssign(self, obj):
        value = self.evaluate(obj.value)
        self.environment.assign(obj.name, value)
        return value
        
    def visitVariable(self, obj):
        return self.environment.get(obj.name)
        
    def visitExpression(self, stmt):
        self.evaluate(stmt.expression)
        return None
    
    def visitPrint(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None
    
    def visitVar(self, stmt):
        value = None
        if (stmt.initializer != None):
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None
    
    def evaluate(self, obj):
        return obj.accept(self)
    
    def execute(self, stmt):
        stmt.accept(self)
    
    def is_truthy(self, obj):
        if obj == None:
            return False
        if type(obj) == bool:
            return bool(obj)
        return True
    
    def check_number_operand(self, operator, operand):
        if (type(operand) == float):
            return
        raise runtime_error.LoxRuntimeError(operator, "Operand must be a number")
    
    def check_number_operands(self, operator, left, right):
        if (type(left) == float and type(left) == float):
            return
        raise runtime_error.LoxRuntimeError(operator, "Operands must be numbers")
    
    def stringify(self, object):
        if (object == None):
            return "nil"
        if type(object) == float:
            text = str(object)
            if (text.endswith(".0")):
                text = text[0:(len(text)-2)]
            return text
        
        return str(object)
    
    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except runtime_error.LoxRuntimeError as error:
            lox.Lox.runtime_error(error)


    
