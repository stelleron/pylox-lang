import scanner

class LoxRuntimeError(Exception):
    def __init__(self, token, message):
        super().__init__()
        self.message = message
        self.token = token