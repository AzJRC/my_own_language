# README 

I started watching a video about python and how to do a programming language. At the moment, I have the Lexer, Parser, and Interpreter defined and they can perform arithmetic and logical operations.

## How to use

- Download the repository using `git clone https://github.com/AzJRC/my_own_language.git`
- Run the following command to start the program `python shell.py`
- You already using the shell! If you want to exit, use `Ctrl + C`

## What can you do with the shell at the moment?

- Perform simple arithmetic and logical operations
- Declare variables. Use the syntax `auto <var_name> = <exp>`
- Use if... else... statements. Use the syntax `if <exp>: <statement> else if <exp>: <statement> ... else: <statement>`
- You can also use Boolean operators such as `AND`, `OR`, and `NOT`, and the Boolean expressions `True` and `False`.
- 

## Definitions

The syntaxis was defined using BNF (Backus-Naur Form). The following are definitions used to refer to specific code snipets:

- An statement is either a variable declaration, if... else... (case) statement, or a set of arithmetic expression.
- An arithmetic expression if compossed of terms and specific operands.
- A term is composed of factos and specific operands.
- A factor is either an integer or a float number.

# TODO

There is a lot of work to do yet. Here is a list of todos:

1. Fix if... else... statements. There are issues when evaluating the else case.
2. Implement loops. (While and for loops)
3. Implement arrays and dictionaries.
4. Implement a multiline function to write longer code.
5. Implement bulit in functions. Important to create an exit() function to close to program.
6. ...
