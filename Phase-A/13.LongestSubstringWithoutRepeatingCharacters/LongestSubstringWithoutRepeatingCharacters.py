class Solution(object):
    def length_of_longest_substring_brute(self, s):
        max_len = 0
            n = len(s)

        for i in range(n):
            seen = set()               
            for j in range(i, n):
                if s[j] in seen:
                    break              
                seen.add(s[j])
                max_len = max(max_len, j - i + 1)

        return max_len
    
""" complexity 
time : O(n^2)
space : O(min(m  n))
"""

    def length_of_longest_substring_sliding_window(self, s):
        window = set()      
        left = 0
        max_len = 0

        for right in range(len(s)):
       
            while s[right] in window:
                window.remove(s[left])
                left += 1

       
            window.add(s[right])
            max_len = max(max_len, right - left + 1)

        return max_len
""" complexity :
time : O(n)
space : O(min(m , n))
"""