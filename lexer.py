from tokens import Integer, Float, Operator, LogicalOperator, ComparisonOperator, SpecialOperator, Declaration, Variable, ReservedToken


class Lexer():
    static_entities = {
        'digits': "0123456789",
        'operators': '+-*/()=',
        'logical_operators': ['AND', 'OR', 'NOT'],
        'comparison_operators': ['!=', '<', '<=', '==', '>=', '>'],
        'stopwords': ' ',
        'reserved_words': ['True', 'False', 'if', 'else'],
        'letters': 'abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ',
        'special_characters': '<>!=:',
        'declarations': ['auto'],
    }

    def __init__(self, text):
        self.text = text
        self.textlen = len(text)
        self.i = 0
        self.char = text[self.i]
        self.token_list = []
        self.curr_token = None

    def move(self):
        self.i += 1
        if self.i < self.textlen:
            # Update the character if the index if within range
            self.char = self.text[self.i]

    def extractWord(self):
        word = ''
        while self.char in Lexer.static_entities['letters'] and self.i < self.textlen:
            word += self.char
            self.move()

        return word

    def extractOperator(self):
        operator = ''
        while self.char in Lexer.static_entities['special_characters']:
            operator += self.char
            self.move()
            if operator == ':': # For if... else... statements
                return SpecialOperator(operator)

        return ComparisonOperator(operator)

    def extractNumber(self):
        number = ''
        isFloat = False
        while ((self.char in Lexer.static_entities['digits'] or self.char == '.') and self.i < self.textlen):
            if self.char == '.':
                isFloat = True
            number += self.char
            self.move()

        return Integer(number) if not isFloat else Float(number)

    def tokenize(self):
        while self.i < self.textlen:

            # tokenize numbers
            if self.char in Lexer.static_entities['digits']:
                self.curr_token = self.extractNumber()

            # tokenize boolean operators
            elif self.char in Lexer.static_entities['special_characters']:
                self.curr_token = self.extractOperator()

            # tokenize words
            elif self.char in Lexer.static_entities['letters']:
                word = self.extractWord()
                if word in Lexer.static_entities['reserved_words']:
                    if word == 'True':
                        self.curr_token = Integer(1)
                    elif word == 'False':
                        self.curr_token = Integer(0)
                    else:
                        self.curr_token = ReservedToken(word)

                elif word in Lexer.static_entities['declarations']:
                    self.curr_token = Declaration(word)

                elif word in Lexer.static_entities['logical_operators']:
                    self.curr_token = LogicalOperator(word)

                else:
                    self.curr_token = Variable(word)

            # tokenize operators
            elif self.char in Lexer.static_entities['operators']:
                self.curr_token = Operator(self.char)
                self.move()

            # ommit stopwords
            elif self.char in Lexer.static_entities['stopwords']:
                self.move()
                continue

            # append current token to the token list
            self.token_list.append(self.curr_token)

        return self.token_list
