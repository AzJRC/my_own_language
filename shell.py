from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
from data import Data
from tokens import Error

data_bank = Data()

while True:

    user_inp = input('> ')
    untokenized = Lexer(user_inp)
    tokens = untokenized.tokenize()
    
    print('tokens: ', tokens)

    parser = Parser(tokens)
    parsed = parser.parse()

    print('parsed: ', parsed)

    interpreter = Interpreter(parsed, data_bank)
    result = interpreter.interpreter()

    print('result: ', result, type(result))

