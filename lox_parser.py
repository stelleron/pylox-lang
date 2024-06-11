import scanner
import expr as Expr
import ast_printer
import stmt
import lox

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
    
    def parse(self):
        statements = []
        while not(self.is_at_end()):
            statements.append(self.declaration())
        return statements

    def expression(self):
        return self.assignment()
    
    def declaration(self):
        try:
            if self.match(scanner.TokenType.VAR):
                return self.var_declaration();
            return self.statement()
        except:
            self.synchronize()
            return None
        
    def statement(self):
        if self.match(scanner.TokenType.PRINT):
            return self.print_statement()
        else:
            return self.expression_statement()

    def print_statement(self):
        value = self.expression()
        self.consume(scanner.TokenType.SEMICOLON, "Expect ';' after value.")
        return stmt.Print(value)
    
    def expression_statement(self):
        value = self.expression()
        self.consume(scanner.TokenType.SEMICOLON, "Expect ';' after value.")
        return stmt.Expression(value)
    
    def assignment(self):
        expr = self.equality()
        if (self.match(scanner.TokenType.EQUAL)):
            equals = self.previous()
            value = self.assignment()
            if (type(expr) == Expr.Variable):
                name = expr.name
                return Expr.Assign(name, value)
            self.error(equals, "Invalid assignment target.")
        return expr
    
    def var_declaration(self):
        name = self.consume(scanner.TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if (self.match(scanner.TokenType.EQUAL)):
            initializer = self.expression()
        self.consume(scanner.TokenType.SEMICOLON, "Expect ';' after value.")
        return stmt.Var(name, initializer)


    def equality(self):
        expr = self.comparision()
        while (self.match(scanner.TokenType.BANG_EQUAL, scanner.TokenType.EQUAL_EQUAL)):
            operator = self.previous()
            right = self.comparision()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    def match(self, *args):
        for arg in args:
            if self.check(arg):
                self.advance()
                return True
        return False
    
    def check(self, type):
        if (self.is_at_end()):
            return False
        return (self.peek().type == type)
    
    def advance(self):
        if not(self.is_at_end()):
            self.current += 1
        return self.previous()
    
    def is_at_end(self):
        return (self.peek().type == scanner.TokenType.EOF)
    
    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current - 1]
    
    def comparision(self):
        expr = self.term()
        while self.match(scanner.TokenType.GREATER, scanner.TokenType.GREATER_EQUAL, scanner.TokenType.LESS, scanner.TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    def term(self):
        expr = self.factor()
        while self.match(scanner.TokenType.MINUS, scanner.TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    def factor(self):
        expr = self.unary()
        while self.match(scanner.TokenType.SLASH, scanner.TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    def unary(self):
        if self.match(scanner.TokenType.BANG, scanner.TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.primary()
    
    def primary(self):
        if (self.match(scanner.TokenType.FALSE)):
            return Expr.Literal(False)
        if (self.match(scanner.TokenType.TRUE)):
            return Expr.Literal(True)
        if (self.match(scanner.TokenType.NIL)):
            return Expr.Literal(None)
        
        if self.match(scanner.TokenType.NUMBER, scanner.TokenType.STRING):
            return Expr.Literal(self.previous().literal)
        
        if (self.match(scanner.TokenType.IDENTIFIER)):
            return Expr.Variable(self.previous())
        
        if self.match(scanner.TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(scanner.TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        
        raise self.error(self.peek(), "Expect expression.")
        
    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token, message):
        lox.Lox.error(token, message)
        return ValueError()
    
    def synchronize(self):
        self.advance()
        while not(self.is_at_end()):
            if self.previous().type == scanner.TokenType.SEMICOLON:
                return
            
            if (self.peek().type == scanner.TokenType.CLASS):
                return
            if (self.peek().type == scanner.TokenType.FUN):
                return
            if (self.peek().type == scanner.TokenType.VAR):
                return
            if (self.peek().type == scanner.TokenType.FOR):
                return
            if (self.peek().type == scanner.TokenType.IF):
                return
            if (self.peek().type == scanner.TokenType.WHILE):
                return
            if (self.peek().type == scanner.TokenType.PRINT):
                return
            if (self.peek().type == scanner.TokenType.RETURN):
                return
            
            self.advance()