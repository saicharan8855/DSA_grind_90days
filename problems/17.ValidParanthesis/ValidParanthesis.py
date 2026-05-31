class Solution(object):
    def ValidParanthesis(self , s):
        while '()' in s or '[]' in s or '{}' in s:
            s = s.replace('()' , '')
            s = s.replace('[]' , '')
            s = s.replace('{}' , '')

        return s == ''
    
"""
comlpexity
Time : O(n^2)
space : O(n)
"""

    def ValidParanthesis2(self , s):
        stack = []
        mapping = {')' : '(' , ']' : '[' , '}' : '{'}

        for char in s:
            if char in mapping:
                top_element = stack.pop() if stack else '#'
                if mapping[char] != top_element:
                    return False
            else:
                stack.append(char)

        return not stack

""" 
comlpexity :
time : O(n)
space : O(n)
"""