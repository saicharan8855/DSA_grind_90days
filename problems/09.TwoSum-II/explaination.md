# Two Sum II – Brute Force vs Two Pointers

## What’s the problem asking?

You’re given a **sorted** integer array `numbers` and an integer `target`.  
Your job is to find **two numbers** such that they add up to `target`, and return their **1-based indices** `[i+1, j+1]` where `i < j`.

Example:

- `numbers = [2, 7, 11, 15]`, `target = 9`
- `2 + 7 = 9`
- Indices in 0-based: `[0, 1]`
- Answer (1-based): `[1, 2]`

The array is guaranteed to be sorted in non-decreasing order, and exactly one solution exists.

---

## Approach 1 – Brute Force (Check All Pairs)

### Intuition

The most straightforward way to solve the problem is:

- For each index `i`, check every index `j > i`.
- If `nums[i] + nums[j] == target`, return that pair.

You ignore the “sorted” property here and just try every possible pair.

### Code

```python
class Solution(object):
    def twoSum(self, nums, target):
        n = len(nums)
        for i in range(n):
            for j in range(i+1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
```

### Step-by-step example

Let:

```python
nums =[1][2][3][4]
target = 9
```

Loop:

- `i = 0`, `j = 1`:
  - `nums[0] + nums[1] = 2 + 7 = 9`
  - This equals `target`, so return `[0, 1]`.

If the matching pair was later in the array, you would keep looping until the condition is met.

### Complexity

- Outer loop: up to `n` iterations.
- Inner loop: up to `n` iterations for each `i`.
- Time: **O(n²)**.
- Space: **O(1)** extra.

This is fine for small arrays but too slow for large inputs, especially when you are given that the array is sorted (which we aren’t using here).

---

## Approach 2 – Optimal Two-Pointer (Use Sorted Property)

### Core idea

Because `numbers` is sorted, you can use **two pointers**:

- `left` pointer at the **start** (index `0`).
- `right` pointer at the **end** (`len(numbers) - 1`).

At each step:

1. Compute `current_sum = numbers[left] + numbers[right]`.
2. If `current_sum == target`:
   - You’ve found the pair → return their **1-based** indices `[left + 1, right + 1]`.
3. If `current_sum < target`:
   - You need a **bigger** sum → move `left` one step to the right (`left += 1`) to increase the sum.
4. If `current_sum > target`:
   - You need a **smaller** sum → move `right` one step to the left (`right -= 1`) to decrease the sum.

Because the array is sorted, moving `left` right increases the value, and moving `right` left decreases the value. That’s what makes this approach work.

### Code

```python
class Solution(object):
    def twoSum(self, numbers, target):
        n = len(numbers)
        left = 0
        right = len(numbers) - 1

        while left < right:
            current_num = numbers[left] + numbers[right]

            if current_num == target:
                return [left + 1, right + 1]
            elif current_num < target:
                left += 1
            else:
                right -= 1
```

---

## Step-by-step walkthrough

Use the example:

```python
numbers =[2][3][4][1]
target = 9
```

### Initial state

- `left = 0` → `numbers[left] = 2`
- `right = 3` → `numbers[right] = 15`

Compute:

- `current_num = 2 + 15 = 17`

Compare:

- `17 > 9` → sum too large → move `right` left:

```python
right = 2   # now numbers[right] = 11
```

### Next iteration

- `left = 0` → `numbers[left] = 2`
- `right = 2` → `numbers[right] = 11`

`current_num = 2 + 11 = 13`

- `13 > 9` → still too large → move `right` left:

```python
right = 1   # now numbers[right] = 7
```

### Next iteration

- `left = 0` → `numbers[left] = 2`
- `right = 1` → `numbers[right] = 7`

`current_num = 2 + 7 = 9`

- `9 == target` → found the answer:

```python
return [left + 1, right + 1]  #[5][1]
```

Note: the answer is **1-based** index, as required by the problem.

---

## Why the two-pointer approach works

Key reasons:

- The array is sorted in non-decreasing order.
- Using `left` and `right`, you always know how the sum changes when moving pointers:
  - Moving `left` right increases `numbers[left]`.
  - Moving `right` left decreases `numbers[right]`.
- Therefore:
  - If sum is too small, increasing the smaller side (`left`) is the only way to possibly hit the target.
  - If sum is too big, decreasing the larger side (`right`) is the only way to possibly hit the target.

You never need to revisit pairs; each pointer moves at most `n` times.

---

## Complexity comparison

### Brute Force

- Time: **O(n²)** (double loop)
- Space: **O(1)**

### Two Pointers

- Time: **O(n)** (each pointer moves at most `n` steps)
- Space: **O(1)** extra

For large inputs, the two-pointer solution is dramatically more efficient.

---

## One-line takeaway

Brute force checks all pairs and is O(n²), but since the array is sorted, you can use a left-right two-pointer scan in O(n) by shrinking the search window based on whether the current sum is smaller or larger than the target.