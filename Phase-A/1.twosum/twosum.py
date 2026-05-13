class Solution(object):

    # Approach 1 : Brute force
    def twoSum_brute(self, nums, target):
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]

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

Time : O(n²)  all pairs checked in worst case.

Space : O(1)  only a few variables used.
"""
