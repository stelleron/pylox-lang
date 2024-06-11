import runtime_error

class Environment():
    def __init__(self):
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name.lexeme in list(self.values.keys()):
            return self.values[name.lexeme]
        raise runtime_error.LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")
    
    def assign(self, name, value):
        if name.lexeme in list(self.values.keys()):
            self.values[name.lexeme] = value
            return
        raise runtime_error.LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")
    
    