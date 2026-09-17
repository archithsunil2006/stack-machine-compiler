class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, data_type):
        if name in self.symbols:
            return False

        self.symbols[name] = data_type
        return True

    def lookup(self, name):
        return self.symbols.get(name)

    def contains(self, name):
        return name in self.symbols

    def __repr__(self):
        return repr(self.symbols)