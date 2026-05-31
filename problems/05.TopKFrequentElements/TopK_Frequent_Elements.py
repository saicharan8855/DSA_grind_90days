from collections import Counter
class Solution(object):
    def top_k_frequent_naive(self , nums, k):
        # Step 1: manually build frequency map
        freq = {}
        for num in nums:
            freq[num] = freq.get(num, 0) + 1

        # Step 2: sort unique elements by frequency descending
        sorted_keys = sorted(freq, key=lambda x: freq[x], reverse=True)

        # Step 3: return top k
        return sorted_keys[:k]
    
"""Complexity :
Time : O(n log n)
Space : O(n) 
"""
    def top_K_frequent2(self , nums , k):
        # Step 1: manually build frequency map
        freq = {}
        for num in nums:
            freq[num] = freq.get(num, 0) + 1

        # Step 2: bucket[i] = list of elements with frequency i
        bucket = [[] for _ in range(len(nums) + 1)]
        for num, count in freq.items():
            bucket[count].append(num)

        # Step 3: scan from highest freq bucket, collect top k
        result = []
        for i in range(len(bucket) - 1, 0, -1):
            for num in bucket[i]:
                result.append(num)
                if len(result) == k:
                    return result
