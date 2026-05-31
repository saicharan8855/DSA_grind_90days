# Top K Frequent Elements – Bucket Frequency Approach

## What’s the problem asking?

You’re given an array of integers `nums` and an integer `k`.  
You need to return the **k most frequent elements** in `nums`.

Example:

- `nums = [1,1,1,2,2,3], k = 2`  
  Frequencies: `1 → 3`, `2 → 2`, `3 → 1`  
  Top 2 most frequent → `[1, 2]` (order between them doesn’t matter)

This is similar in spirit to “Top K” problems you see a lot in interviews: count, then pick the most common ones.

---

## The naive approach – sort by frequency

Idea:  
1. Count how many times each number appears.  
2. Sort unique numbers by their frequency in descending order.  
3. Take the first `k`.

### Code

```python
from collections import Counter

def top_k_frequent_naive(nums, k):
    # Step 1: count frequency of each element
    freq = Counter(nums)  # e.g., {1:3, 2:2, 3:1}

    # Step 2: sort unique elements by frequency descending
    sorted_keys = sorted(freq, key=lambda x: freq[x], reverse=True)

    # Step 3: return top k
    return sorted_keys[:k]
```

### Walkthrough on example

Take `nums = [1,1,1,2,2,3], k = 2`.

1. Frequency map:

   ```python
   freq = {1: 3, 2: 2, 3: 1}
   ```

2. Sort keys by frequency:

   ```python
   sorted_keys = sorted(freq, key=lambda x: freq[x], reverse=True)
   # frequencies: 1→3, 2→2, 3→1
   # sorted_keys could be[1][2][3]
   ```

3. Take top `k`:

   ```python
   sorted_keys[:2]  #[2][1]
   ```

### Complexity

- Let `n = len(nums)`, and `m` = number of distinct elements.
- Counting: `O(n)` (one pass to build the `Counter`).
- Sorting unique keys by frequency: `O(m log m)`.
- Overall: **O(n + m log m)** time; **O(m)** extra space for `freq`.

Works fine, but we can do better than `log` factor by avoiding sorting.

---

## The optimal approach – bucket sort by frequency

Key observation:  
- The maximum frequency any element can have is **n** (if all elements are the same).  
- So possible frequencies are `1, 2, ..., n`.  
- Instead of sorting by frequency, we can **bucket** elements by their frequency and then walk the buckets from highest frequency down.

### Core idea

1. Count frequencies (same as before).
2. Create a list of buckets where:
   - `bucket[i]` holds all numbers that appear exactly `i` times.
3. Iterate from the highest bucket index down, collecting elements until `k` elements are found.

This avoids sorting.

### Code

```python
from collections import Counter

def top_k_frequent_optimal(nums, k):
    freq = Counter(nums)  # {1:3, 2:2, 3:1}

    # bucket index = frequency, bucket[i] = list of nums with freq i
    bucket = [[] for _ in range(len(nums) + 1)]

    for num, count in freq.items():
        bucket[count].append(num)

    result = []
    # scan from highest freq bucket down to 1
    for i in range(len(bucket) - 1, 0, -1):
        for num in bucket[i]:
            result.append(num)
            if len(result) == k:
                return result
```

---

## Step-by-step walkthrough of the optimal approach

Use the same example:

```python
nums =[3][1][2]
k = 2
```

### 1) Count frequencies

```python
freq = Counter(nums)
# freq = {1: 3, 2: 2, 3: 1}
```

This tells us:

- `1` appears 3 times  
- `2` appears 2 times  
- `3` appears 1 time

### 2) Initialize buckets

```python
bucket = [[] for _ in range(len(nums) + 1)]
```

- `len(nums) = 6`, so `bucket` has length 7: indices `0` to `6`.
- Initially:

  ```python
  bucket = [[], [], [], [], [], [], []]
  # index 0 unused (no element appears 0 times)
  ```

Each index `i` will hold numbers that appear exactly `i` times.

### 3) Fill the buckets

Loop over `freq.items()`:

```python
for num, count in freq.items():
    bucket[count].append(num)
```

- For `(num=1, count=3)`:
  - `bucket[3].append(1)`
- For `(num=2, count=2)`:
  - `bucket[2].append(2)`
- For `(num=3, count=1)`:
  - `bucket[1].append(3)`

Now buckets look like:

```python
bucket = []
bucket =         # numbers that appear once[1][3]
bucket =         # numbers that appear twice[2]
bucket =         # numbers that appear three times[3][1]
bucket = [][4]
bucket = [][5]
bucket = [][6]
```

This directly groups elements by frequency without sorting.

### 4) Collect from highest frequency down

```python
result = []

for i in range(len(bucket) - 1, 0, -1):
    for num in bucket[i]:
        result.append(num)
        if len(result) == k:
            return result
```

Iterate `i` from 6 down to 1:

- `i = 6`: `bucket[6]` is empty → skip.
- `i = 5`: empty → skip.
- `i = 4`: empty → skip.
- `i = 3`: `bucket[3] = [1]`
  - Append `1` → `result = [1]`
  - `len(result) = 1 < k` → continue.
- `i = 2`: `bucket[2] = [2]`
  - Append `2` → `result = [1, 2]`
  - `len(result) == k` → return `[1, 2]`.

So the top 2 frequent elements are `[1, 2]`.

Order here is determined by scanning from high freq down and the order within each bucket; any valid top `k` order is acceptable for this problem.

---

## Why is this faster?

Let:

- `n = len(nums)`,  
- `m` = number of distinct elements.

### Bucket approach:

- Counting frequencies: `O(n)`.
- Building buckets: we iterate over `m` distinct elements → `O(m)`.
- Scanning buckets: total scan over all buckets is `O(n)` in the worst case (since total number of pushes is `m`, and we early stop when we’ve collected `k`).

Overall: **O(n + m)**, often simplified to **O(n)**.

### Comparison

- Naive (sorting by frequency): `O(n + m log m)` due to sorting.
- Bucket: `O(n)` without any sorting step.

Space:

- `freq` takes `O(m)`.
- `bucket` has size `O(n)` (list of lists).
- Overall extra space: **O(n)**.

---

## One-line takeaway

Count frequencies, bucket numbers by their frequency, then walk the buckets from highest to lowest until you’ve picked `k` numbers—that gives you the top K frequent elements in linear time.

---
