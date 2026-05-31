
class Solution(object):
    def product_except_self_brute(self,nums):
        n = len(nums)
        result = []

        # For each position, multiply everything except itself
        for i in range(n):
            product = 1
            for j in range(n):
                if i != j:           # skip the current index
                    product *= nums[j]
            result.append(product)

        return result

""" Complexity :
Time : O(n^2)
Space : O(n)
"""
    def product_except_self2(self , nums):
        n = len(nums)
        var = [1] * n 

        left = 1
        for i in range(1 , n):
            temp = nums[i]
            num[i] = left 
            left = left * nums[i]
        right = 1
        for i in range(n - 1 , -1 , -1):
            var[i] = var[i] * right 
            right = right * nums[i] 
        return var

"""Complexity : 
Time : O(n)
Space : O(1)
"""