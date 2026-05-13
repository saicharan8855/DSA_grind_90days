# Two Sum - Python Solution



## Problem Statement

Given an array of integers nums and an integer target, return the indices

of the two numbers such that they add up to target.



You may assume that each input has exactly one solution, and you may not

use the same element twice. You can return the answer in any order.





## Examples



Example 1:

&#x20; Input:  nums = \[2, 7, 11, 15], target = 9

&#x20; Output: \[0, 1]

&#x20; Reason: nums\[0] + nums\[1] = 2 + 7 = 9



Example 2:

&#x20; Input:  nums = \[3, 2, 4], target = 6

&#x20; Output: \[1, 2]



Example 3:

&#x20; Input:  nums = \[3, 3], target = 6

&#x20; Output: \[0, 1]





## Constraints

&#x20; - 2 <= nums.length <= 10^4

&#x20; - -10^9 <= nums\[i] <= 10^9

&#x20; - -10^9 <= target <= 10^9

&#x20; - Exactly one valid answer exists.





## Intuition

The naive idea is to try all pairs and check whether their sum equals target.

However, that takes quadratic time because for each element, you scan the

remaining array.



To do better, notice that for each element x, you only need to know whether

(target - x) has appeared before. This "have we seen the complement?" question

is a constant-time lookup in a hash map (Python dict).





## Brute-force Approach (O(n^2))



Idea:

&#x20; Use two nested loops to check every pair (i, j) with i < j.

&#x20; If nums\[i] + nums\[j] == target, return \[i, j].



Pseudocode:

&#x20; for i from 0 to n-1:

&#x20;     for j from i+1 to n-1:

&#x20;         if nums\[i] + nums\[j] == target:

&#x20;             return \[i, j]



Complexity:

&#x20; Time  : O(n^2) - all pairs checked in worst case.

&#x20; Space : O(1)   - only a few variables used.



This is straightforward but too slow for large arrays.





## Optimized Hash Map Approach (O(n))



Key Idea:

&#x20; When at element nums\[i], the required complement is:

&#x20;     complement = target - nums\[i]



&#x20; If that complement is already in a dictionary, then its index and i

&#x20; are the answer. If not, store the current number and its index in the

&#x20; dictionary and move on.



Algorithm Steps:

&#x20; 1. Initialize an empty dictionary seen = {} to map value -> index.

&#x20; 2. Loop over the array with index i and value num = nums\[i].

&#x20; 3. Compute complement = target - num.

&#x20; 4. If complement exists in seen, return \[seen\[complement], i].

&#x20; 5. Otherwise, store the current value: seen\[num] = i.



&#x20; By the end of the loop, the answer will have already been returned

&#x20; because the problem guarantees exactly one solution.

