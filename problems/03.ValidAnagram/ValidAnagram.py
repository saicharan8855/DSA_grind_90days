class Solution(object): 
    def is_anagram(self , s , t):
        if len(s) != len(t):
            return False
        return sorted(s) == sorted(t)

"""
Complexity :
Time Complexity : O(n logn)
Space Complexity : O(1)
"""
    def is_anagram2(self , s , t):
        if len(s) != lrn(t):
            return False
        
        char_count = {}
        for char in s:
            if char in char_count:
                char_count[char] += 1
            else:
                char_count[char] = 1
        for char in t:
            if char in char_count:
                char_count[char] -= 1
            else:
                return False
        for count in char_count.values():
            if count != 0:
                return False
        return True
"""
Complexity :
time : O(n)
space : O(k)
"""
