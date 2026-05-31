class Solution(object):

    # Approach 1 : Brute force
    def twoSum_brute(self, nums, target):
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
                
"""
complexity
Time : O(n²) — two nested loops check all pairs in the worst case.

Space : O(1) — only loop variables i, j, and n are used, no extra data structure.
"""

    # Approach 2 : Hashmap (optimal)
    def twoSum(self, nums, target):
        seen = {}  # value -> index
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i

""" 
Complexity

Time: O(n)  each element is processed once with O(1) average-time hash operations.
Space: O(n)  in the worst case the dictionary stores up to n entries.

"""
