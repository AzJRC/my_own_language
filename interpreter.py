from tokens import Integer, Float, Variable, Boolean, CaseStatement, loopStatement

class Interpreter:
    def __init__(self, tree, data):
        self.tree = tree
        self.data = data

    def read_INTEGER(self, value):
        return int(value)
    
    def read_FLOAT(self, value):
        return float(value)
    
    def read_BOOLEAN(self, value):
        return int(value)
    
    def read_VARIABLE(self, var_name):
        var = self.data.read(var_name)
        return getattr(self, f'read_{var.type}')(var.value)
    
    def compute_b_compare(self, lval, rval, operator):
        if operator.value == '!=':
            return 1 if lval != rval else 0

        elif operator.value == '<':
            return 1 if lval < rval else 0
            
        elif operator.value == '<=':
            return 1 if lval <= rval else 0

        elif operator.value == '==':
            return 1 if lval == rval else 0

        elif operator.value == '>=':
            return 1 if lval >= rval else 0

        elif operator.value == '>':
            return 1 if lval > rval else 0
        
    def compute_b_logical(self, lnode, rnode, operator):
        if operator.value == 'AND':
            return 1 if lnode.value in ['1', 1] and rnode.value in ['1', 1] else 0
            
        if operator.value == 'OR':
            return 1 if lnode.value in ['1', 1] or rnode.value in ['1', 1] else 0
        
        if operator.value == 'NOT':
            return 0 if rnode.value not in ['0', 0] else 1


    def compute_b(self, lnode, rnode, operator):
        lnode_type = lnode.type
        rnode_type = rnode.type

        # variable assignment

        if operator.value == '=':
            lnode.data_type = rnode.type
            self.data.write(lnode, rnode)
            return self.data.read_all() # break code here and show variables
        
        # Compute expressions
        
        lvalue = getattr(self, f'read_{lnode_type}')(lnode.value)
        rvalue = getattr(self, f'read_{rnode_type}')(rnode.value)

        if operator.type == 'COMPARISON_OPERATOR':
            bool_value = self.compute_b_compare(lvalue, rvalue, operator)
            return Boolean(bool_value)
        elif operator.type == 'LOGICAL_OPERATOR':
            bool_value = self.compute_b_logical(lvalue, rvalue, operator)
            return Boolean(bool_value)

        if operator.value == '+':
            output = lvalue + rvalue
        elif operator.value == '-':
            output = lvalue - rvalue
        elif operator.value == '*':
            output = lvalue * rvalue
        elif operator.value == '/':
            output = lvalue / rvalue

        return Integer(output) if (lnode_type != 'FLOAT' and rnode_type != 'FLOAT') else Float(output)
    
    def interpret_case(self, expressions, statements):
        for i in range(len(expressions)):
            expression = self.interpreter(expressions[i])
            if expression:
                return self.interpreter(statements[i])
        return


    
    def interpreter(self, tree=None):
        if tree is None:
            tree = self.tree

        if isinstance(tree, CaseStatement):
            exp = tree.value[0]
            val = tree.value[1]
            return self.interpret_case(exp, val)
        
        elif isinstance(tree, loopStatement):
            loop_type = tree.value[0]
            if loop_type == 'while':
                loop_condition = tree.value[1]
                loop_statement = tree.value[2]

                while True:
                    condition_outcome = self.interpreter(loop_condition)
                    if condition_outcome.value:
                        res = self.interpreter(loop_statement)
                        print(res)
                    else:
                        return res
                    

        #no operation
        elif not isinstance(tree, list) and not isinstance(tree, Variable):
            return tree
        
        elif not isinstance(tree, list) and isinstance(tree, Variable):
            return self.data.read(tree.value)
        
        # Unary operation
        elif len(tree) == 2:

            # left subtree
            lnode = Integer(0)

            # right subtree
            rnode = tree[1]
            if isinstance(rnode, list):
                rnode = self.interpreter(rnode)

            # operator
            operator = tree[0]
            return self.compute_b(lnode, rnode, operator)

        # binary operation
        else:
            # left subtree
            lnode = tree[0]
            if isinstance(lnode, list):
                lnode = self.interpreter(lnode)

            # right subtree
            rnode = tree[2]
            if isinstance(rnode, list):
                rnode = self.interpreter(rnode)

            # operator
            operator = tree[1]
            return self.compute_b(lnode, rnode, operator)