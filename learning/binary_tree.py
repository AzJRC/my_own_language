class Node:
    def __init__(self, value = 0):
        self.value = value
        self.lnode = None
        self.rnode = None

class bTree:
    def __init__(self, root = 0):
        self.root = Node(root)

    def preorder(self, start, record = []):
        if start:
            record.append(start.value)
            record = self.preorder(start.lnode, record)
            record = self.preorder(start.rnode, record)
        
        return record

    def postorder(self, start, record = []):
        if start:
            record = self.postorder(start.lnode, record)
            record = self.postorder(start.rnode, record)
            record.append(start.value)
        
        return record
        

tree = bTree(10)
tree.root.lnode = Node(9)
tree.root.rnode = Node(11)
print(tree.preorder(tree.root))
print(tree.postorder(tree.root))