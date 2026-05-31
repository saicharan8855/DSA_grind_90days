class Solution(object):
    def twoSum_II(self , numbers , target):
        n = len(numbers)
        for i in range(n):
            for j in range(i+1 , n):
                if numbers[i] +numbers[j] == target:
                    return[i+1 , j+1]
                
""" Complexity :
Time : O(n^2)
space : O(1)
"""

    def two_sum_II_2(self , numbers , target):
    
        left = 0
        right = len(numbers) - 1
        while left < right:
            current_num = numbers[left] + numbers[right]
            if current_num == target:
                return [left + 1 , rigth + 1]
            elif current_num < target:
                left += 1
            else:
                right -= 1

""" complexity :
time : O(n)
Space = O(1)
"""