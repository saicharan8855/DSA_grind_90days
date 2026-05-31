# Contains Duplicate – Sorting Approach

## What's the problem even asking?

You're given a list of numbers. Does any number appear more than once?

- `[1, 2, 3, 1]` → Yes, `1` appears twice → return `True`
- `[1, 2, 3, 4]` → All unique → return `False`

Simple to understand. How you solve it is where it gets interesting.

---

## The insight behind this approach

What if you sorted the array first?

If there are duplicates, sorting puts them right next to each other. You stop hunting across the whole array. One pass through adjacent pairs is enough.

```
Before sorting: [3, 1, 2, 1]  ← the two 1s are far apart
After sorting:  [1, 1, 2, 3]  ← now they're neighbors
```

---

## The code

```python
def contains_duplicate(nums):
    nums = sorted(nums)               # bring duplicates together
    for i in range(len(nums) - 1):    # walk through adjacent pairs
        if nums[i] == nums[i + 1]:    # are these two the same?
            return True               # duplicate found
    return False                      # no duplicates
```

---

## Walking through an example

Say `nums = [1, 2, 3, 1]`.

**Step 1 – Sort it:** `[1, 1, 2, 3]`

**Step 2 – Check neighbors:**

| i | nums[i] | nums[i+1] | Equal? |
|---|---------|-----------|--------|
| 0 | 1       | 1         | ✅ Yes! → return True |

We return `True` on the very first comparison. The loop doesn't need to go further.

---

## Why `len(nums) - 1` and not `len(nums)`?

Inside the loop you're accessing `nums[i + 1]`. If `i` reaches the last index, `i + 1` goes out of bounds — `IndexError`.

Stopping at `n-2` still covers the final pair:

```
Array:   [1, 1, 2, 3]
Indices:  0  1  2  3

range(len(nums) - 1) = range(3) → i goes: 0, 1, 2

At i=2: compare nums[2] with nums[3]  ← last pair, safe ✅
```

Nothing is skipped. Every adjacent pair gets checked.

---

## How fast is this?

| What | How fast | Why |
|------|----------|-----|
| Time | O(n log n) | Sorting is the bottleneck |
| Space | O(1) | No extra memory if you use `nums.sort()` |

`sorted(nums)` creates a new sorted list (O(n) space). `nums.sort()` sorts in place (O(1) space). Use the latter if you don't mind modifying the original.

---

## Where does this sit among all approaches?

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute Force | O(n²) | O(1) | Check everything against everything |
| **Sorting (this one)** | **O(n log n)** | **O(1)** | Sort first, one pass |
| Hash Set | O(n) | O(n) | Remember what you've seen |

Faster than brute force, and barely uses memory compared to the hash set approach.

---

## The one-line takeaway

Sort the array → duplicates become neighbors → one pass finds them.
