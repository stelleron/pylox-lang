import lox

class TokenType():
    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    COMMA = 5
    DOT = 6
    MINUS = 7
    PLUS = 8
    SEMICOLON = 9
    SLASH = 10
    STAR = 11

    BANG = 12
    BANG_EQUAL = 13
    EQUAL = 14
    EQUAL_EQUAL = 15
    GREATER = 16
    GREATER_EQUAL = 17
    LESS = 18
    LESS_EQUAL = 19


    IDENTIFIER = 20 
    STRING = 21
    NUMBER = 22

    AND = 23
    CLASS = 24
    ELSE = 25
    FALSE = 26
    FUN = 27
    FOR = 28
    IF = 29 
    NIL = 30
    OR = 31
    PRINT = 32
    RETURN = 33
    SUPER = 34
    THIS = 35
    TRUE = 36
    VAR = 37
    WHILE = 38

    EOF = 39

keywords = {
    "and":    TokenType.AND,
    "class":  TokenType.CLASS,
    "else":   TokenType.ELSE,
    "false":  TokenType.FALSE,
    "for":    TokenType.FOR,
    "fun":    TokenType.FUN,
    "if":     TokenType.IF,
    "nil":    TokenType.NIL,
    "or":     TokenType.OR,
    "print":  TokenType.PRINT,
    "return": TokenType.RETURN,
    "super":  TokenType.SUPER,
    "this":   TokenType.THIS,
    "true":   TokenType.TRUE,
    "var":    TokenType.VAR,
    "while":  TokenType.WHILE
}

class Token():
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal 
        self.line = line
    
    def __str__(self):
        return "" + str(self.type) + " " + str(self.lexeme) + " " + str(self.literal)

class Scanner():
    def __init__(self, source):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []

    def is_at_end(self):
        return self.current >= len(self.source)
    
    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c
    
    def add_token(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected):
        if (self.is_at_end()):
            return False
        if (self.source[self.current] != expected):
            return False
        
        self.current += 1
        return True
    
    def peek(self):
        if (self.is_at_end()):
            return "\0"
        return self.source[self.current]
    
    def peek_next(self):
        if (self.current + 1 >= len(self.source)):
            return "\0"
        return self.source[self.current + 1]
    
    def string(self):
        while not(self.peek() == '"') and not(self.is_at_end()):
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            lox.Lox.error(self.line, "Undetermined string.")
            return;

        self.advance()
        value = self.source[self.start + 1: self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()


        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def identifier(self):
        while self.peek().isalnum():
            self.advance()
        text = self.source[self.start: self.current]
        t_type = keywords.get(text, None)
        if (t_type == None):
            t_type = TokenType.IDENTIFIER
        self.add_token(t_type)

    def scan_token(self):
        c = self.advance()

        if (c == "("):
            self.add_token(TokenType.LEFT_PAREN)
        elif (c == ")"):
            self.add_token(TokenType.RIGHT_PAREN)
        elif (c == "{"):
            self.add_token(TokenType.LEFT_BRACE)
        elif (c == "}"):
            self.add_token(TokenType.RIGHT_BRACE)
        elif (c == ","):
            self.add_token(TokenType.COMMA)
        elif (c == "."):
            self.add_token(TokenType.DOT)
        elif (c == "-"):
            self.add_token(TokenType.MINUS)
        elif (c == "+"):
            self.add_token(TokenType.PLUS)
        elif (c == ";"):
            self.add_token(TokenType.SEMICOLON)
        elif (c == "*"):
            self.add_token(TokenType.STAR)

        elif (c == "!"):
            self.add_token(TokenType.BANG_EQUAL) if (self.match("=")) else self.add_token(TokenType.BANG)
        elif (c == "="):
            self.add_token(TokenType.EQUAL_EQUAL) if (self.match("=")) else self.add_token(TokenType.EQUAL)
        elif (c == "<"):
            self.add_token(TokenType.LESS_EQUAL) if (self.match("=")) else self.add_token(TokenType.LESS)
        elif (c == ">"):
            self.add_token(TokenType.GREATER_EQUAL) if (self.match("=")) else self.add_token(TokenType.GREATER)

        elif (c == "/"):
            if self.match("/"):
                while (self.peek() != "\n" and not (self.is_at_end())):
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        
        elif (c == '"'):
            self.string()

        elif (c == " "):
            pass
        elif (c == "\t"):
            pass
        elif (c == "\t"):
            pass
        elif (c == "\n"):
            self.line += 1

        else:
            if c.isdigit():
                self.number()
            elif c.isalpha():
                self.identifier()
            else:
                lox.Lox.error(self.line, "Unexpected character.")
            
        

    def scan_tokens(self):
        while not(self.is_at_end()):
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens