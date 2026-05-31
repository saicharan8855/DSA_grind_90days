class MinStack(object):

    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append(val)        # add to top

    def pop(self):
        self.stack.pop()              # remove from top

    def top(self):
        return self.stack[-1]         # peek at top

    def getMin(self):
        return min(self.stack) 
    
"""
complexity:
Time complexity: O(n)
Space complexity: O(n)
"""
class Minstack2(onject):
    def __init__(self):
        self.stack = []
        self.min_stack = []         

    def push(self, val):
        self.stack.append(val)
        
        if self.min_stack:
            self.min_stack.append(min(val, self.min_stack[-1]))
        else:
            self.min_stack.append(val)   

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()        

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1] 
    
"""complexity:
Time complexity: O(1)
Space complexity: O(n)
"""