# 3Sum – Brute Force vs Sort + Two Pointers

## What's the problem asking?

You're given an integer array `nums`.
You need to find all **unique triplets** `[nums[i], nums[j], nums[k]]` such that:

- `i != j`, `i != k`, `j != k`
- `nums[i] + nums[j] + nums[k] == 0`

The result must contain **no duplicate triplets**.

Example:

- `nums = [-1, 0, 1, 2, -1, -4]`
- Output: `[[-1, -1, 2], [-1, 0, 1]]`

This is different from Two Sum: you are finding triplets that sum to zero, and you must skip all duplicate combinations in the result.

---

## Approach 1 – Brute Force (Triple Nested Loop)

### Intuition

Try every possible combination of three indices `i`, `j`, `k` where `i < j < k`.
If the three numbers sum to zero, add the **sorted** triplet to a set to automatically avoid duplicates.

Using a set here handles the deduplication because a sorted tuple like `(-1, 0, 1)` will always look identical regardless of the order the indices were visited.

### Code

```python
def three_sum_brute(nums):
    n = len(nums)
    result = set()

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    # Sort triplet so duplicates like (-1,0,1) and (0,-1,1)
                    # are treated as the same
                    triplet = tuple(sorted([nums[i], nums[j], nums[k]]))
                    result.add(triplet)

    return [list(t) for t in result]
```

### Walkthrough

Take `nums = [-1, 0, 1, 2, -1, -4]`.

- `i=0, j=1, k=2`: `-1 + 0 + 1 = 0` → sorted triplet `(-1, 0, 1)` → add to set.
- `i=0, j=1, k=3`: `-1 + 0 + 2 = 1` → skip.
- `i=0, j=2, k=4`: `-1 + 1 + (-1) = -1` → skip.
- `i=0, j=3, k=4`: `-1 + 2 + (-1) = 0` → sorted `(-1, -1, 2)` → add to set.
- ... continues checking all remaining combinations.

Final result: `[[-1, -1, 2], [-1, 0, 1]]`.

### Complexity

- Three nested loops: each up to `n` elements.
- Time: **O(n³)**.
- Space: **O(k)** for storing at most `k` unique triplets.

---

## The key insight behind the optimal approach

The brute force is O(n³) because it tries every combination blindly.

The optimal idea:

1. **Sort the array first.**
2. Fix one element `nums[i]` using an outer loop.
3. For the remaining two elements, use **two pointers** (`left`, `right`) on the sorted subarray to find pairs that sum to `-nums[i]`.

Sorting enables two things:

- Two pointers work correctly because the array is ordered.
- Duplicate elements are adjacent, so you can skip them easily.

---

## The optimal code

```python
def three_sum(nums):
    nums.sort()                    # sort first — key to everything
    result = []

    for i in range(len(nums) - 2):
        # If smallest number > 0, no triplet can sum to 0
        if nums[i] > 0:
            break

        # Skip duplicate values for the fixed element
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        left = i + 1
        right = len(nums) - 1

        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total == 0:
                result.append([nums[i], nums[left], nums[right]])

                # Skip duplicates for left pointer
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for right pointer
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1

                left += 1          # move both inward after recording
                right -= 1

            elif total < 0:
                left += 1          # need bigger sum
            else:
                right -= 1         # need smaller sum

    return result
```

---

## Step-by-step walkthrough of the optimal approach

Take:

```python
nums = [-1, 0, 1, 2, -1, -4]
```

### Step 1 – Sort the array

```python
nums.sort()
# nums = [-4, -1, -1, 0, 1, 2]
```

Now duplicates are adjacent and the array is ordered. Two-pointer logic will work.

---

### Step 2 – Outer loop: fix nums[i]

```python
for i in range(len(nums) - 2):
```

We stop at `len(nums) - 2` because we need at least two elements after `i` for the two pointers.

---

### Iteration i = 0, nums[i] = -4

- `nums[0] = -4`, not greater than 0, so continue.
- No previous duplicate to skip.

Set up two pointers:

```python
left = 1    # nums[left] = -1
right = 5   # nums[right] = 2
```

**While left < right:**

- `total = -4 + (-1) + 2 = -3 < 0` → need bigger sum → `left += 1`

  ```python
  left = 2    # nums[left] = -1
  ```

- `total = -4 + (-1) + 2 = -3 < 0` → `left += 1`

  ```python
  left = 3    # nums[left] = 0
  ```

- `total = -4 + 0 + 2 = -2 < 0` → `left += 1`

  ```python
  left = 4    # nums[left] = 1
  ```

- `total = -4 + 1 + 2 = -1 < 0` → `left += 1`

  ```python
  left = 5    # left == right, exit while loop
  ```

No triplets found for `nums[i] = -4`.

---

### Iteration i = 1, nums[i] = -1

- `nums[1] = -1`, not greater than 0.
- `i > 0` but `nums[1] != nums[0]` (−1 ≠ −4) → no skip.

Set up two pointers:

```python
left = 2    # nums[left] = -1
right = 5   # nums[right] = 2
```

**While left < right:**

- `total = -1 + (-1) + 2 = 0` → found a triplet!
  - Append `[-1, -1, 2]` to result.
  - Skip duplicates for left:
    - `nums[left] = nums[2] = -1`, `nums[left+1] = nums[3] = 0` → not equal, no skip.
  - Skip duplicates for right:
    - `nums[right] = nums[5] = 2`, `nums[right-1] = nums[4] = 1` → not equal, no skip.
  - Move both inward:

    ```python
    left = 3    # nums[left] = 0
    right = 4   # nums[right] = 1
    ```

- `total = -1 + 0 + 1 = 0` → found a triplet!
  - Append `[-1, 0, 1]` to result.
  - No duplicates to skip on either side.
  - Move both inward:

    ```python
    left = 4
    right = 3   # left >= right, exit while loop
    ```

Triplets found for `nums[i] = -1`: `[-1, -1, 2]` and `[-1, 0, 1]`.

---

### Iteration i = 2, nums[i] = -1

- `i > 0` and `nums[2] == nums[1]` (−1 == −1) → **skip this iteration** to avoid duplicate triplets.

```python
if i > 0 and nums[i] == nums[i - 1]:
    continue
```

This is the duplicate-skipping logic for the fixed element.

---

### Iteration i = 3, nums[i] = 0

- `nums[3] = 0`, not greater than 0, so continue.

Set up two pointers:

```python
left = 4    # nums[left] = 1
right = 5   # nums[right] = 2
```

- `total = 0 + 1 + 2 = 3 > 0` → need smaller sum → `right -= 1`

  ```python
  right = 4   # left >= right, exit while loop
  ```

No triplets found.

---

### Iteration i = 4, nums[i] = 1

- `nums[4] = 1 > 0` → **break** out of the outer loop.

```python
if nums[i] > 0:
    break
```

If the fixed element itself is positive, there is no way for the triplet to sum to zero since the array is sorted and everything to the right is even larger.

---

### Final result

```python
result = [[-1, -1, 2], [-1, 0, 1]]
```

---

## Why the three duplicate-skipping rules work

There are three places duplicates are handled:

**Rule 1 – Skip duplicate fixed element (outer loop):**

```python
if i > 0 and nums[i] == nums[i - 1]:
    continue
```

If the same value was already used as the fixed element in the previous iteration, all triplets starting with it were already found. Skip it.

**Rule 2 – Skip duplicates after finding a triplet (left pointer):**

```python
while left < right and nums[left] == nums[left + 1]:
    left += 1
```

After recording a triplet, if the next left value is the same, it would produce an identical triplet. Advance `left` past all duplicates.

**Rule 3 – Skip duplicates after finding a triplet (right pointer):**

```python
while left < right and nums[right] == nums[right - 1]:
    right -= 1
```

Same logic for the right pointer.

---

## Complexity

### Brute Force

| Approach | Time | Space | Notes |
|---------|------|-------|-------|
| Brute Force | O(n³) | O(k) for result set | Three nested loops, every combination checked |

### Optimal Sort + Two Pointers

| Approach | Time | Space | Notes |
|---------|------|-------|-------|
| Sort + Two Pointers | O(n²) | O(1) extra | Sort is O(n log n), two-pointer scan is O(n) per fixed element |

The outer loop runs `n` times and each two-pointer scan runs in O(n), giving O(n²) total. This is optimal for this problem.

---

## One-line takeaway

Sort the array, fix one element at a time with the outer loop, then use two pointers to find pairs summing to the negative of the fixed element, skipping duplicates at every step to ensure unique triplets.