import expr
import scanner

class AstPrinter(expr.ExprVisitor):
    def __init__(self):
        pass

    def parenthesize(self, name, *args):
        string = "(" + name
        for arg in args:
            string += " "
            string += arg.accept(self)
        
        string += ")"
        return string

    def print(self, expr):
        return expr.accept(self)

    def visitBinary(self, obj):
        return self.parenthesize(obj.operator.lexeme, obj.left, obj.right)

    def visitGrouping(self, obj):
        return self.parenthesize("group", obj.expression)
    
    def visitLiteral(self, obj):
        if obj.value == None:
            return "nil"
        return str(obj.value)

    def visitUnary(self, obj):
        return self.parenthesize(obj.operator.lexeme, obj.right)
    
    def visitAssign(self, obj):
        return self.parenthesize(obj.name, obj.value)
    
    def visitVariable(self, obj):
        return self.parenthesize(obj.name)
    
if __name__ == "__main__":
    expression = expr.Binary(
        expr.Unary(
            scanner.Token(scanner.TokenType.MINUS, "-", None, 1),
            expr.Literal(123)),
        scanner.Token(scanner.TokenType.STAR, "*", None, 1),
        expr.Grouping(
            expr.Literal(45.67)
        )
    )

    print(AstPrinter().print(expression))