class Solution(object):
    def LongestConsecutive(self , nums):
        if not nums:
            return 0
        nums.sort()
        long = 1
        curr = 1
        for i in range(1, len(nums)):
            if nums[i] == nums[i-1]:
                continue
            if nums[i] == nums[i-1] + 1:
                curr += 1
            else:
                long = max(long, curr)
                curr = 1
        return max(long, curr)
    
"""
Complexity :
Time : O(n*logn)
Space : O(1)
"""
    
    def LongestConsecutive2(self , nums)
        if not nums:
            return 0
        num_set = set(nums)
        longest = 1
        for num in num_set:
            if num - 1 not in num_set:
                curr_num =num
                curr_streak = 1

                while curr_num + 1 in num_set:
                    curr_num += 1
                    curr_streak += 1
                longest = max(longest , curr_streak)
        return longest

""" 
Complexity :
Time : O(n)
Space : O(n)
"""