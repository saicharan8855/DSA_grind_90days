\# Longest Consecutive Sequence – Hash Set O(n) Approach



\## What’s the problem asking?



You’re given an unsorted array of integers `nums`.  

You need to find the \*\*length of the longest sequence of consecutive integers\*\* that appear in `nums`.



Important:  

\- The numbers don’t need to be adjacent in the array.  

\- They just need to form a consecutive run when sorted, like `1,2,3,4`.



Example:



\- `nums = \[100, 4, 200, 1, 3, 2]`  

&#x20; Consecutive sequence: `1, 2, 3, 4`  

&#x20; Longest length = `4`



\- `nums = \[0,3,7,2,5,8,4,6,0,1]`  

&#x20; Consecutive sequence: `0,1,2,3,4,5,6,7,8`  

&#x20; Longest length = `9`



So the task is: find the longest chain like `x, x+1, x+2, ...` that exists in the array.



\---



\## The brute force idea – sort and scan



The simplest intuitive approach:



1\. Sort the array.

2\. Walk through it and count how long consecutive runs are.

3\. Skip duplicates.

4\. Track the longest run.



\### Brute force code



```python

def longest\_consecutive\_brute(nums):

&#x20;   if not nums:

&#x20;       return 0



&#x20;   nums.sort()        # sort so consecutive numbers are adjacent



&#x20;   longest = 1

&#x20;   current = 1



&#x20;   for i in range(1, len(nums)):

&#x20;       if nums\[i] == nums\[i - 1]:

&#x20;           continue               # skip duplicates

&#x20;       elif nums\[i] == nums\[i - 1] + 1:

&#x20;           current += 1           # extend the streak

&#x20;           longest = max(longest, current)

&#x20;       else:

&#x20;           current = 1            # streak broken, reset



&#x20;   return longest

```



\### How it works, step by step



Take `nums = \[100, 4, 200, 1, 3, 2]`.



1\. After sorting:



&#x20;  ```python

&#x20;  nums =\[1]\[2]\[3]\[4]

&#x20;  ```



2\. Initialize:



&#x20;  ```python

&#x20;  longest = 1

&#x20;  current = 1

&#x20;  ```



3\. Walk from index 1:



&#x20;  - i = 1: `nums\[1] = 2`, `nums\[0] = 1`  

&#x20;    `2 == 1 + 1` → consecutive  

&#x20;    `current = 2`, `longest = 2`



&#x20;  - i = 2: `nums\[2] = 3`, `nums\[1] = 2`  

&#x20;    `3 == 2 + 1` → consecutive  

&#x20;    `current = 3`, `longest = 3`



&#x20;  - i = 3: `nums\[3] = 4`, `nums\[2] = 3`  

&#x20;    `4 == 3 + 1` → consecutive  

&#x20;    `current = 4`, `longest = 4`



&#x20;  - i = 4: `nums\[4] = 100`, `nums\[3] = 4`  

&#x20;    `100 != 4 + 1` → streak broken  

&#x20;    `current = 1`



&#x20;  - i = 5: `nums\[5] = 200`, `nums\[4] = 100`  

&#x20;    `200 != 100 + 1` → streak broken  

&#x20;    `current = 1`



Final `longest = 4`.



\### Why brute force is slower



\- Sorting takes \*\*O(n log n)\*\*.

\- The linear scan is \*\*O(n)\*\*.

\- Overall: \*\*O(n log n)\*\* time.



This is fine for many cases, but we can do better: \*\*O(n)\*\* without sorting.



\---



\## The key insight behind the optimal approach



Instead of sorting, use a \*\*hash set\*\* and a clever observation:



A number `num` is the \*\*start of a consecutive sequence\*\* if and only if `num - 1` is \*\*not\*\* in the set.



Why?



\- If `num - 1` exists, then `num` is part of a longer sequence that starts earlier.

\- If `num - 1` does \*\*not\*\* exist, then `num` must be the smallest element of some sequence.



So the strategy:



1\. Put all numbers into a set for O(1) lookups.

2\. For each number `num` in the set:

&#x20;  - If `num - 1` is \*\*not\*\* in the set, it’s a sequence start.

&#x20;  - From there, count how long the sequence goes by checking `num+1`, `num+2`, …

3\. Track the longest streak found.



This avoids sorting and ensures each number is part of at most one inner while-loop scan, giving \*\*O(n)\*\* total time.



\---



\## The optimal code



```python

def longestConsecutive(self, nums):

&#x20;   if not nums:

&#x20;       return 0 

&#x20;   longest = 0

&#x20;   set\_nums = set(nums)

&#x20;   for num in set\_nums:

&#x20;       if num - 1 not in set\_nums:

&#x20;           curr\_num = num

&#x20;           curr\_streak = 1



&#x20;           while curr\_num + 1 in set\_nums:

&#x20;               curr\_num += 1

&#x20;               curr\_streak += 1

&#x20;           longest = max(longest, curr\_streak)

&#x20;   return longest

```



\---



\## Step-by-step walkthrough



Use the same example:



```python

nums =\[1]\[2]\[3]\[4]

```



\### Step 1 – Build the set



```python

set\_nums = set(nums)

\# set\_nums = {100, 4, 200, 1, 3, 2}

```



Now lookups like `x in set\_nums` are \*\*O(1)\*\*.



\---



\### Step 2 – Iterate over each number



```python

longest = 0

for num in set\_nums:

&#x20;   if num - 1 not in set\_nums:

&#x20;       ...

```



We only start counting when `num - 1` is \*\*not\*\* in the set.



\#### Consider `num = 100`



\- Is `99` in `set\_nums`? No.

\- So `100` is a sequence start.



```python

curr\_num = 100

curr\_streak = 1



while curr\_num + 1 in set\_nums:

&#x20;   # check 101

```



\- Is `101` in set? No → loop doesn’t run.

\- `longest = max(0, 1) = 1`



\#### Consider `num = 4`



\- Is `3` in set? Yes → skip (4 is not a start).



\#### Consider `num = 200`



\- Is `199` in set? No → start.

\- Check `201` → not in set → streak = 1.

\- `longest = max(1, 1) = 1`



\#### Consider `num = 1`



\- Is `0` in set? No → start of a sequence.



Now grow the streak:



```python

curr\_num = 1

curr\_streak = 1

```



\- Is `2` in set? Yes →  

&#x20; `curr\_num = 2`, `curr\_streak = 2`

\- Is `3` in set? Yes →  

&#x20; `curr\_num = 3`, `curr\_streak = 3`

\- Is `4` in set? Yes →  

&#x20; `curr\_num = 4`, `curr\_streak = 4`

\- Is `5` in set? No → stop.



Now:



```python

longest = max(1, 4) = 4

```



\#### Consider `num = 3`



\- Is `2` in set? Yes → skip (not a start).



\#### Consider `num = 2`



\- Is `1` in set? Yes → skip (not a start).



Final result:



```python

return longest  # 4

```



\---



\## Why we only start at `num - 1 not in set`



This is the core optimization.



If we started from every number and scanned forward:



\- For `1,2,3,4`, we’d start at 1, then 2, then 3, then 4, redundantly re-scanning the same sequence multiple times.

\- That could approach \*\*O(n²)\*\* in the worst case.



By only starting when `num - 1` is missing:



\- We start \*\*once per sequence\*\*, at its smallest element.

\- Each number is visited:

&#x20; - Once in the outer `for` loop (as a candidate start), and

&#x20; - At most once in the inner `while` loop as part of exactly one sequence.



So total work is \*\*O(n)\*\*.



\---



\## Complexity



\### Brute force (sort + scan)



| Approach | Time | Space | Why |

|---------|------|-------|-----|

| Sort + scan | O(n log n) | O(1) extra (or O(n) if sort isn’t in-place) | Sorting dominates |



\### Optimal hash-set approach



| Approach | Time | Space | Why |

|---------|------|-------|-----|

| Hash set + sequence start check | O(n) | O(n) | Build set O(n); each number visited O(1) times total |



This is why the hash-set solution is considered optimal for this problem.



\---



\## One-line takeaway



Put all numbers in a set, start counting a streak only when `num-1` is missing (sequence start), and grow the streak forward; this gives the longest consecutive sequence in linear time.

