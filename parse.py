from tokens import Error

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenslen = len(tokens)
        self.i = 0
        self.curr_token = self.tokens[self.i]
    
    """ 
    BNF Definitions

    <DIGIT> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;
    <INTEGER> ::= <DIGIT> { <DIGIT> };
    <FLOAT> ::= <INTEGER> . <INTEGER>;
    <FACTOR> ::= <INTEGER> | <FLOAT>
    """

    # A factor is just a number alone
    def factor(self):
        if self.curr_token.type == 'INTEGER' or self.curr_token.type == 'FLOAT':
            return self.curr_token
        elif self.curr_token.value == '(': # consider the expression inside the parenthesis
            self.move()
            exp = self.expression()
            return exp
        elif self.curr_token.type == 'VARIABLE':
            return self.curr_token
        elif self.curr_token.value in ('+', '-'):
            operation = self.curr_token
            self.move()
            exp = self.factor()
            return [operation, exp]
        elif self.curr_token.value == 'NOT':
            operation = self.curr_token
            self.move()
            exp = self.expression()
            return [operation, exp]
    
    """ 
    BNF Definitions

    <OPERATION> ::= * | / ; ## Term operations are limited to multiplication and division
    <TERM> ::= <FACTOR> <OPERATOR> <FACTOR> { <OPERATOR> <FACTOR> };
    """

    # A term is an arithmetic or logical operation of 1 or more factors
    def term(self):
        lnode = self.factor()
        self.move()
        while self.curr_token.value in ['*','/']:
            operation = self.curr_token
            self.move()
            rnode = self.factor()
            lnode = [lnode, operation, rnode]
            self.move()    
        return lnode
    
    """
    BNF Definitions

    <OPERATOR> ::= + | - | != | < | <= | == | >= | >; ## Expression operations are limited to summation, subtraction and comparison operations.
    <EXPRESSION> ::= <TERM> <OPERATOR> <TERM> { <OPERATOR> <TERM> };
    """
    
    # An expression is a collection of terms
    def expression(self):
        lnode = self.term()
        while self.curr_token.value in ['+', '-','!=','<','<=','==','>=','>']:
            operation = self.curr_token
            self.move()
            rnode = self.term()
            lnode = [lnode, operation, rnode]
        if self.curr_token.value in ['AND','OR', 'NOT']:
            operation = self.curr_token
            self.move()
            rnode = self.expression()
            lnode = [lnode, operation, rnode]
        return lnode
    
    """
    BNF Definition

    <VARIABLE> ::= auto <VARIABLE> = <EXPRESSION>
    <STATEMENT> ::= <VARIABLE> | <EXPRESSION>
    """
    
    def variable(self):
        if self.curr_token.type == 'VARIABLE':  
            return self.curr_token
    
    def statement(self):
        # variable declaration case -> [auto, a, =, 20]
        if self.curr_token.type == 'DECLARATION':
            self.move()
            lnode = self.variable()
            self.move()
            if self.curr_token.value == '=':
                operation = self.curr_token
                self.move()
                rnode = self.expression()

                return [lnode, operation, rnode]

        elif self.curr_token.type == 'BUILT_IN_FUNCTION':
            return self.curr_token
        
        # arithmetic expression case
        elif self.curr_token.type in ('INTEGER', 'FLOAT', 'OPERATOR', 'LOGICAL_OPERATOR', 'VARIABLE'):
            return self.expression()
    
    #Move index
    def move(self):
        self.i += 1
        if self.i < self.tokenslen:
            self.curr_token = self.tokens[self.i]

    # Return parsed statement (either a variable declaration or an arithmetic expression)
    def parse(self):
        return self.statement()

    