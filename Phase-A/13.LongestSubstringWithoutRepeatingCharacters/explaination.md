# Longest Substring Without Repeating Characters – Brute Force vs Sliding Window

## What's the problem asking?

You're given a string `s`.
You need to find the **length** of the longest substring that has **no repeated characters**.

- Substring = continuous block of characters.
- "Without repeating characters" = every character inside that substring is unique.

Examples:

- `s = "abcabcbb"` → longest substring without repeats is `"abc"` → length `3`.
- `s = "bbbbb"` → longest is `"b"` → length `1`.
- `s = "pwwkew"` → longest is `"wke"` or `"kew"` → length `3`.

---

## Approach 1 – Brute Force (Check All Substrings)

### Intuition

Try every possible starting index `i`, and extend forward as long as no character repeats:

1. For each `i` from 0 to n-1:
   - Start with an empty set `seen`.
   - Move `j` from `i` to the end:
     - If `s[j]` not in `seen`, add it and update `max_len`.
     - If `s[j]` already in `seen`, stop extending and break.

### Code

```python
def length_of_longest_substring_brute(s):
    max_len = 0
    n = len(s)

    for i in range(n):
        seen = set()               # fresh set for each starting point
        for j in range(i, n):
            if s[j] in seen:
                break              # duplicate found, stop extending
            seen.add(s[j])
            max_len = max(max_len, j - i + 1)

    return max_len
```

### Step-by-step example

Take:

```python
s = "abcabcbb"
```

- Start i = 0:
  - j = 0: 'a' not in seen → seen = { 'a' }, max_len = 1
  - j = 1: 'b' not in seen → seen = { 'a', 'b' }, max_len = 2
  - j = 2: 'c' not in seen → seen = { 'a', 'b', 'c' }, max_len = 3
  - j = 3: 'a' already in seen → break.

- Start i = 1:
  - j = 1: 'b' → seen = { 'b' }
  - j = 2: 'c' → seen = { 'b', 'c' }
  - j = 3: 'a' → seen = { 'b', 'c', 'a' }, max_len = 3
  - j = 4: 'b' already in seen → break.

- Start i = 2, 3, etc. similarly.

Maximum length found is 3.

### Complexity

- Outer loop over i: up to n.
- Inner loop over j: up to n for each i in worst case.
- Time: **O(n²)**.
- Space: **O(min(n, alphabet))** for the seen set.

Brute force is simple but quadratic.

---

## Approach 2 – Optimal Sliding Window (Two Pointers)

### Intuition

Instead of restarting from scratch for every i, maintain a **sliding window** [left, right] that always represents a substring with **no duplicates**:

- Use a set `window` to store characters currently inside the window.
- Expand `right` one step at a time over the string.
- If adding `s[right]` would cause a duplicate:
  - Move `left` forward, removing `s[left]` from the set, until the duplicate is gone.
- Once `s[right]` is no longer in `window`, add it and update `max_len`.

So the window stretches and shrinks dynamically, always staying valid (no repeats inside).

### Code

```python
def length_of_longest_substring(s):
    window = set()       # characters in current window
    left = 0
    max_len = 0

    for right in range(len(s)):
        # Shrink window from left until duplicate is removed
        while s[right] in window:
            window.remove(s[left])
            left += 1

        # Now s[right] is safe to add
        window.add(s[right])
        max_len = max(max_len, right - left + 1)

    return max_len
```

---

## Step-by-step walkthrough

Use:

```python
s = "abcabcbb"
```

Initialize:

```python
window = set()
left = 0
max_len = 0
```

### right = 0, s[right] = 'a'

- 'a' not in window → skip while loop.
- Add 'a': window = { 'a' }.
- Window: [0, 0] → length = right - left + 1 = 1.
- max_len = 1.

### right = 1, s[right] = 'b'

- 'b' not in window.
- Add 'b': window = { 'a', 'b' }.
- Window: [0, 1] → "ab" → length 2.
- max_len = 2.

### right = 2, s[right] = 'c'

- 'c' not in window.
- Add 'c': window = { 'a', 'b', 'c' }.
- Window: [0, 2] → "abc" → length 3.
- max_len = 3.

### right = 3, s[right] = 'a'

- 'a' IS in window → enter while loop.

  - Iteration 1:
    - s[left] = s[0] = 'a'.
    - window.remove('a') → window = { 'b', 'c' }.
    - left = 1.

- 'a' no longer in window → exit while.

- Add 'a': window = { 'b', 'c', 'a' }.
- Window: [1, 3] → "bca" → length 3.
- max_len stays 3.

### right = 4, s[right] = 'b'

- 'b' IS in window → enter while loop.

  - s[left] = s[1] = 'b'.
  - window.remove('b') → window = { 'c', 'a' }.
  - left = 2.

- 'b' no longer in window → exit while.

- Add 'b': window = { 'c', 'a', 'b' }.
- Window: [2, 4] → "cab" → length 3.
- max_len stays 3.

### right = 5, s[right] = 'c'

- 'c' IS in window → enter while loop.

  - s[left] = s[2] = 'c'.
  - window.remove('c') → window = { 'a', 'b' }.
  - left = 3.

- 'c' no longer in window → exit while.

- Add 'c': window = { 'a', 'b', 'c' }.
- Window: [3, 5] → "abc" → length 3.
- max_len stays 3.

### right = 6, s[right] = 'b'

- 'b' IS in window → enter while loop.

  - s[left] = s[3] = 'a' → remove 'a' → window = { 'b', 'c' }, left = 4.
  - 'b' still in window.
  - s[left] = s[4] = 'b' → remove 'b' → window = { 'c' }, left = 5.

- 'b' no longer in window → exit while.

- Add 'b': window = { 'c', 'b' }.
- Window: [5, 6] → "cb" → length 2.
- max_len stays 3.

### right = 7, s[right] = 'b'

- 'b' IS in window → enter while loop.

  - s[left] = s[5] = 'c' → remove 'c' → window = { 'b' }, left = 6.
  - 'b' still in window.
  - s[left] = s[6] = 'b' → remove 'b' → window = {}, left = 7.

- 'b' no longer in window → exit while.

- Add 'b': window = { 'b' }.
- Window: [7, 7] → "b" → length 1.
- max_len stays 3.

Loop ends. Return max_len = 3.

---

## Why the sliding window is O(n)

- Both pointers `left` and `right` move from 0 to n-1 at most once.
- `left` only ever moves forward, never backward.
- Each character is added to and removed from the set at most once.

Total operations proportional to n:

- Time: **O(n)**.
- Space: **O(min(n, alphabet))** for the window set.

This is dramatically faster than O(n²) for large strings.

---

## Complexity comparison

| Approach | Time | Space | Notes |
|---------|------|-------|-------|
| Brute Force | O(n²) | O(alphabet) | Two nested loops, fresh set per start |
| Sliding Window | O(n) | O(alphabet) | Each char added and removed at most once |

---

## One-line takeaway

Maintain a sliding window with a set of current characters, expand `right` at every step, shrink from `left` whenever a duplicate appears, and track the maximum window size — that gives the length of the longest substring without repeating characters in O(n) time.