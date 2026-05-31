from itertools import permutations
from collections import Counter
class Solution(object):
    def PermutationInString(self , s1 , s2):
        s1_count = set("".join(p) for p in permutations(s1))
        for i in range(len(s2) - len(s1) + 1):
            if s2[i : i + len(s1)] in s1_count:
                return True
        return False

"""
Complexity :
Time : O(n * m!)
Space : O(m!)
"""

    def PermutationInString2(self , s1 , s2):
        s1_count = Counter(s1)
        window = Counter()
        k = len(s1)

        if len(s2) < k:
            return False
        for i in range(len(s2)):
            window[s2[i]] += 1
            
            if i >= k:
                left_char = [s2[i - k]]
                window[left_char] -= 1

            if window[left_char] == 0:
                del window[left_char]

        if window == s1_count:
            return True
        return False

"""
compexity :
time : O(n)
space : O(1)
"""
        