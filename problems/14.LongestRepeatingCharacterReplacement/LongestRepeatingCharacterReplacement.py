class Solution(object):
    def character_replacement_brute(self , s, k):
    max_len = 0
    n = len(s)

    for i in range(n):
        freq = {}                
        for j in range(i, n):
           
            freq[s[j]] = freq.get(s[j], 0) + 1

            max_freq = max(freq.values())  
            window_size = j - i + 1
            replacements_needed = window_size - max_freq

            if replacements_needed <= k:
                max_len = max(max_len, window_size)
            else:
                break                     

    return max_len

"""complexity :
time: O(n^2) 
space: O(n) 
"""

    def character_replacement(self , s, k):
    freq = {}
    max_freq = 0      
    left = 0
    max_len = 0

    for right in range(len(s)):
      
        freq[s[right]] = freq.get(s[right], 0) + 1

        max_freq = max(max_freq, freq[s[right]])

        window_size = right - left + 1

        if window_size - max_freq > k:
            freq[s[left]] -= 1
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len

"""complexity :
time: O(n)
space: O(1) 
""" 