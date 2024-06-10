import lox
import expr
import scanner
import ast_printer
import runtime_error

class Interpreter(expr.ExprVisitor):
    def __init__(self):
        pass

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
    
    def evaluate(self, obj):
        return obj.accept(self)
    
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
    
    def interpret(self, expression):
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except runtime_error.LoxRuntimeError as error:
            lox.Lox.runtime_error(error)


    
