class Stack:
    def __init__(self, stack_list = []):
        self.stack_list = stack_list

    def read(self):
        return self.stack_list[-1]
    
    def append(self, value):
        if isinstance(value, int):
            self.stack_list.append(value)
        elif isinstance(value, list):
            self.stack_list += value

    def pop(self):
        return self.stack_list.pop()
    
    def unstack(self):
        stack = self.stack_list.copy()
        self.stack_list.clear()
        stack.reverse()
        return stack

    

stack1 = Stack()
print(stack1.stack_list)
stack1.append(5)
print(stack1.stack_list)
stack1.append([1,2,3])
print(stack1.stack_list)
print(stack1.pop())
print(stack1.read())
print(stack1.stack_list)
print(stack1.unstack())

