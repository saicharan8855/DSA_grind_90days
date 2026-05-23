class Solution(object):
    def ContainerWithMostwater(self , height):

        max_water = 0
        n = len(height)

        for i in range(n):
            for j in range(i + 1, n):
        
                h = min(height[i], height[j])
            
                w = j - i
                area = h * w
                max_water = max(max_water, area)

        return max_water
    
    def ContainerWithMostwater2(self , height):
        left = 0 
        right = len(height) - 1
        maximum_area = 0

        while left < right:
            distance = right - left
            minimum_height = min(height[left] , height[right])
            area = diastance * minimum_height

            if area > maximum_area:
                maximum_area = area 

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return maximum_area


            