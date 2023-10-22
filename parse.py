from tokens import CaseStatement, loopStatement

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
        while self.curr_token.value in ['AND','OR', 'NOT']:
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
        return lnode
    
    """
    BNF Definition

    <CASE EXPRESSION> ::= if <EXPRESSION> : <STATEMENT> { else if <EXPRESSION> : <STATEMENT> } { else : <STATEMENT> }
    """
    
    def ifElseExpression(self):
        if_exps = []
        acts = []
        
        # <IF_EXP> ::= if <exp>: <statement> { else if <exp>: <statement> } { else: <statement> }
        while self.curr_token.value == 'if' or self.curr_token.value == 'else' and not (self.curr_token.value == 'else' and self.tokens[self.i + 1] != 'if'):
            if self.curr_token.value == 'else' and self.tokens[self.i + 1].value == 'if':
                self.move()
            self.move()
            if_exps.append(self.expression())
            if self.curr_token.value == ':':
                self.move()   
                acts.append(self.statement())
        
        # final else case
        if self.curr_token.value == 'else':
            if_exps.append('else')
            self.move()
            self.move()
            acts.append(self.statement())

        return CaseStatement([if_exps, acts])
    

    """ 
    BNF Definition

    <WHILE LOOP> ::= while <EXPRESSION> : <STATEMENT>
    """

    def loopExpression(self):
        loop_type = self.curr_token.value
        if self.curr_token.value == 'while':
            self.move()
            if_exp = self.expression()
            if self.curr_token.value == ':':
                self.move()
                stat = self.statement()
            
            return loopStatement([loop_type, if_exp, stat])

    
    """
    BNF Definition

    <VARIABLE> ::= auto <VARIABLE> = <EXPRESSION>
    <STATEMENT> ::= <VARIABLE> | <EXPRESSION> | <CASE STATEMENT>
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
        
        # if... else... (case) statement case
        elif self.curr_token.value == 'if':
            return self.ifElseExpression()
        
        # while loop case
        elif self.curr_token.value in ['while']:
            return self.loopExpression()

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

    