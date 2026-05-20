class Solution(object):
    def isPalindrome(self , s):
        clean = ""
        for ch in s:
            if ch.isalnum():
                clean += ch.lower()
            
        return clean == clean[::-1]
    
""" Complexity :
Time : O(n)
Space : O(n)
"""
    
    def isPaindrome2(self , s):
        left , right = 0 , len(s) - 1
        while left < right:
            if not s[left].isalnum():
                left += 1
            elif not s[right].isalnum():
                right -= 1
            else:
                if s[left].lower() != s[right].lower():
                    return False
                left += 1
                right -= 1
        return True
""" Complexity :
time : O(n)
Space : O(1)
"""