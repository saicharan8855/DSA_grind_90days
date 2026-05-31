class Solution(object):
    def MaxProfit(self , prices):
        max_price = 0
        n = len(prices)

        for i in range(n):
            for j in range(i + 1 , n):
                profit = prices[j] - prices[i]
                max_price = max(max_price , profit)
        return max_price
    
"""Complexity :
Time : O(n^2)
Space : O(1)
"""
    def MaxProfit2(self , prices):
        min_price = float('inf')
        max_profit = 0

        for price in prices:
        if price < min_price:
            min_price = price          
        elif price - min_price > max_profit:
            max_profit = price - min_price  

    return max_profit

"""Complexity :
Time : O(n)
Space : O(1)
"""