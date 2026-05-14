class Solution(object):
    def ContainsDuplicate(self , nums):
        for i in range (len(nums)):
            for j in range(i + 1 , len(nums)):
                if nums[i] == nums[j]:
                    return True
        return False
    """ 
Complexity :
Time complexity : O(n^2)
Space complexity : O(1)

"""
    
    def ContainsDuplicate2(self , nums):
        nums.sort()
        for in in range(len(nums) - 1):
            if nums[i] == nums[i + 1]:
                return True 
        return False
"""
Complexity :
Time Complexity : O(nlogn)
Space Complexity : O(1)

"""
    