# Longest Consecutive Sequence – Hash Set O(n) Approach

## What’s the problem asking?

You’re given an unsorted array of integers `nums`.  
You need to find the **length of the longest sequence of consecutive integers** that appear in `nums`.

Important:  
- The numbers don’t need to be adjacent in the array.  
- They just need to form a consecutive run when sorted, like `1,2,3,4`.

Example:

- `nums = [100, 4, 200, 1, 3, 2]`  
  Consecutive sequence: `1, 2, 3, 4`  
  Longest length = `4`

- `nums = [0,3,7,2,5,8,4,6,0,1]`  
  Consecutive sequence: `0,1,2,3,4,5,6,7,8`  
  Longest length = `9`

So the task is: find the longest chain like `x, x+1, x+2, ...` that exists in the array.

---

## The brute force idea – sort and scan

The simplest intuitive approach:

1. Sort the array.
2. Walk through it and count how long consecutive runs are.
3. Skip duplicates.
4. Track the longest run.

### Brute force code

```python
def longest_consecutive_brute(nums):
    if not nums:
        return 0

    nums.sort()        # sort so consecutive numbers are adjacent

    longest = 1
    current = 1

    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            continue               # skip duplicates
        elif nums[i] == nums[i - 1] + 1:
            current += 1           # extend the streak
            longest = max(longest, current)
        else:
            current = 1            # streak broken, reset

    return longest
```

### How it works, step by step

Take `nums = [100, 4, 200, 1, 3, 2]`.

1. After sorting:

   ```python
   nums =[1][2][3][4]
   ```

2. Initialize:

   ```python
   longest = 1
   current = 1
   ```

3. Walk from index 1:

   - i = 1: `nums[1] = 2`, `nums[0] = 1`  
     `2 == 1 + 1` → consecutive  
     `current = 2`, `longest = 2`

   - i = 2: `nums[2] = 3`, `nums[1] = 2`  
     `3 == 2 + 1` → consecutive  
     `current = 3`, `longest = 3`

   - i = 3: `nums[3] = 4`, `nums[2] = 3`  
     `4 == 3 + 1` → consecutive  
     `current = 4`, `longest = 4`

   - i = 4: `nums[4] = 100`, `nums[3] = 4`  
     `100 != 4 + 1` → streak broken  
     `current = 1`

   - i = 5: `nums[5] = 200`, `nums[4] = 100`  
     `200 != 100 + 1` → streak broken  
     `current = 1`

Final `longest = 4`.

### Why brute force is slower

- Sorting takes **O(n log n)**.
- The linear scan is **O(n)**.
- Overall: **O(n log n)** time.

This is fine for many cases, but we can do better: **O(n)** without sorting.

---

## The key insight behind the optimal approach

Instead of sorting, use a **hash set** and a clever observation:

A number `num` is the **start of a consecutive sequence** if and only if `num - 1` is **not** in the set.

Why?

- If `num - 1` exists, then `num` is part of a longer sequence that starts earlier.
- If `num - 1` does **not** exist, then `num` must be the smallest element of some sequence.

So the strategy:

1. Put all numbers into a set for O(1) lookups.
2. For each number `num` in the set:
   - If `num - 1` is **not** in the set, it’s a sequence start.
   - From there, count how long the sequence goes by checking `num+1`, `num+2`, …
3. Track the longest streak found.

This avoids sorting and ensures each number is part of at most one inner while-loop scan, giving **O(n)** total time.

---

## The optimal code

```python
def longestConsecutive(self, nums):
    if not nums:
        return 0 
    longest = 0
    set_nums = set(nums)
    for num in set_nums:
        if num - 1 not in set_nums:
            curr_num = num
            curr_streak = 1

            while curr_num + 1 in set_nums:
                curr_num += 1
                curr_streak += 1
            longest = max(longest, curr_streak)
    return longest
```

---

## Step-by-step walkthrough

Use the same example:

```python
nums =[1][2][3][4]
```

### Step 1 – Build the set

```python
set_nums = set(nums)
# set_nums = {100, 4, 200, 1, 3, 2}
```

Now lookups like `x in set_nums` are **O(1)**.

---

### Step 2 – Iterate over each number

```python
longest = 0
for num in set_nums:
    if num - 1 not in set_nums:
        ...
```

We only start counting when `num - 1` is **not** in the set.

#### Consider `num = 100`

- Is `99` in `set_nums`? No.
- So `100` is a sequence start.

```python
curr_num = 100
curr_streak = 1

while curr_num + 1 in set_nums:
    # check 101
```

- Is `101` in set? No → loop doesn’t run.
- `longest = max(0, 1) = 1`

#### Consider `num = 4`

- Is `3` in set? Yes → skip (4 is not a start).

#### Consider `num = 200`

- Is `199` in set? No → start.
- Check `201` → not in set → streak = 1.
- `longest = max(1, 1) = 1`

#### Consider `num = 1`

- Is `0` in set? No → start of a sequence.

Now grow the streak:

```python
curr_num = 1
curr_streak = 1
```

- Is `2` in set? Yes →  
  `curr_num = 2`, `curr_streak = 2`
- Is `3` in set? Yes →  
  `curr_num = 3`, `curr_streak = 3`
- Is `4` in set? Yes →  
  `curr_num = 4`, `curr_streak = 4`
- Is `5` in set? No → stop.

Now:

```python
longest = max(1, 4) = 4
```

#### Consider `num = 3`

- Is `2` in set? Yes → skip (not a start).

#### Consider `num = 2`

- Is `1` in set? Yes → skip (not a start).

Final result:

```python
return longest  # 4
```

---

## Why we only start at `num - 1 not in set`

This is the core optimization.

If we started from every number and scanned forward:

- For `1,2,3,4`, we’d start at 1, then 2, then 3, then 4, redundantly re-scanning the same sequence multiple times.
- That could approach **O(n²)** in the worst case.

By only starting when `num - 1` is missing:

- We start **once per sequence**, at its smallest element.
- Each number is visited:
  - Once in the outer `for` loop (as a candidate start), and
  - At most once in the inner `while` loop as part of exactly one sequence.

So total work is **O(n)**.

---

## Complexity

### Brute force (sort + scan)

| Approach | Time | Space | Why |
|---------|------|-------|-----|
| Sort + scan | O(n log n) | O(1) extra (or O(n) if sort isn’t in-place) | Sorting dominates |

### Optimal hash-set approach

| Approach | Time | Space | Why |
|---------|------|-------|-----|
| Hash set + sequence start check | O(n) | O(n) | Build set O(n); each number visited O(1) times total |

This is why the hash-set solution is considered optimal for this problem.

---

## One-line takeaway

Put all numbers in a set, start counting a streak only when `num-1` is missing (sequence start), and grow the streak forward; this gives the longest consecutive sequence in linear time.
