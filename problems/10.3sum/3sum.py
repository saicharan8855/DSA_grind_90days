class Solution(object):
    def threeSum(self , nums):
        n = len(nums)
        result = []

        for i in range(n):
            for j in range(i + 1 , n):
                for k in range(j + 1 , n):
                    three_sum = nums[i] + nums[j] + nums[k]
                    if three_sum == 0:
                        triplet = [nums[i] , nums[j] , nums[k]]
                        triplet.sort()
                        if triplet not in result:
                            result.append(triplet)
        return result 

""" 
Complesity :
Time : O(n^3)
space : O(n)
"""
    def threesum2(self , nums):
        nums.sort()
        result = []
        n = len(nums)
        for i in range(n - 2):
            if nums[i] > 0:
                break
            if i > 0 and nums[i] == nums[i + 1]:
                continue
            left = i + 1
            right = n - 1
            while left < right:
                three_sum = nums[i] + nums[left] + nums[right]
                if three_sum == 0:
                    result.append([nums[i] , nums[left] , nums[right]])
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif three_sum < 0:
                    left += 1
                else:
                    right -= 1
            return result 
        
""" complexity :
time : O(n^2)
space : O(n)
"""
