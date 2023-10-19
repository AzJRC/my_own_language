class Data():
    def __init__(self):
        self.variables = {}

    def read(self, name):
        return self.variables[name]

    def read_all(self):
        return self.variables

    def write(self, variable, value):
        self.variables[variable.value] = value
