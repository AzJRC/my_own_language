class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

    # represent any token entity as its value property
    def __repr__(self):
        return str(self.value)


class Integer(Token):
    def __init__(self, value):
        super().__init__('INTEGER', value)


class Float(Token):
    def __init__(self, value):
        super().__init__('FLOAT', value)


class Operator(Token):
    def __init__(self, value):
        super().__init__('OPERATOR', value)


class LogicalOperator(Token):
    def __init__(self, value):
        super().__init__('LOGICAL_OPERATOR', value)


class ComparisonOperator(Token):
    def __init__(self, value):
        super().__init__('COMPARISON_OPERATOR', value)



class SpecialOperator(Token):
    def __init__(self, value):
        super().__init__('SPECIAL_OPERATOR', value)


class Boolean(Token):
    def __init__(self, value):
        super().__init__('BOOLEAN', value)

    def __repr__(self):
        if self.value == 0:
            return 'False'
        elif self.value == 1:
            return 'True'
        else:
            return 'None'


class Declaration(Token):
    def __init__(self, value):
        super().__init__('DECLARATION', value)


class Variable(Token):
    def __init__(self, value):
        super().__init__('VARIABLE', value)
        self.data_type = '?'


class Error(Token):
    def __init__(self, error_name):
        super().__init__('ERROR', error_name)


class ReservedToken(Token):
    def __init__(self, value):
        super().__init__('RESERVED_TOKEN', value)



class CaseStatement(Token):
    def __init__(self, value):
        super().__init__('CASE_STATEMENT', value)