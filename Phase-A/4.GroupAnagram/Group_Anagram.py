from collections import defaultdict
class Solution(object): 
    def group_anagrams_brute(self , strs):
        n = len(strs)
        visited = [False] * n  # track strings already assigned to a group
        result = []

        for i in range(n):
            if visited[i]:
                continue
            group = [strs[i]]
            visited[i] = True

            for j in range(i + 1, n):
                if not visited[j]:
                # Two strings are anagrams if their sorted form is equal
                    if sorted(strs[i]) == sorted(strs[j]):
                        group.append(strs[j])
                        visited[j] = True

            result.append(group)

        return result
    
""" Complexity :
Time : O(n^2 * k log k)
Space : O(n * k) 
"""
    def group_anagrams_optimal(strs):
        anagram_map = defaultdict(list)

        for s in strs:
            count = [0] * 26  

            for c in s:
                count[ord(c) - ord('a')] += 1  
            key = tuple(count)          
            anagram_map[key].append(s)  

        return list(anagram_map.values())

""" complexity : 
Time : O(n*k)
Space : O(n*k)
"""
    