# Longest Repeating Character Replacement – Brute Force vs Sliding Window

## What's the problem asking?

You're given a string `s` and an integer `k`.
You can replace **at most k characters** in any substring with any letter you want.
Find the **length of the longest substring** you can get that contains only one distinct character after those replacements.

Examples:

- `s = "AABABBA"`, `k = 1` → Answer: `4`
  - Window "AABA": most frequent is 'A' (3 times), replacements needed = 4 - 3 = 1 = k → valid.
- `s = "ABAB"`, `k = 2` → Answer: `4`
  - Replace both 'B's → "AAAA", or both 'A's → "BBBB". Entire string is valid.

---

## The key formula

For any window [i, j] of length window_size:

- Find the most frequent character in that window → call its count `max_freq`.
- All other characters need to be replaced: `replacements_needed = window_size - max_freq`.
- The window is **valid** if `replacements_needed <= k`.

So the goal is: find the longest window where `window_size - max_freq <= k`.

This single formula drives both approaches.

---

## Approach 1 – Brute Force (All Starting Points)

### Intuition

Try every possible starting index `i`.
From there, extend `j` forward one step at a time, maintaining a frequency map of characters in the current window.
At each step:

1. Compute max_freq (most frequent character count in the window).
2. Compute replacements_needed = window_size - max_freq.
3. If replacements_needed <= k → window is valid → update max_len.
4. Else → window is invalid → break and try next starting point.

### Code

```python
def character_replacement_brute(s, k):
    max_len = 0
    n = len(s)

    for i in range(n):
        freq = {}                          # fresh count for each start
        for j in range(i, n):
            # Add current character to frequency map
            freq[s[j]] = freq.get(s[j], 0) + 1

            max_freq = max(freq.values())  # most frequent char count
            window_size = j - i + 1
            replacements_needed = window_size - max_freq

            if replacements_needed <= k:
                max_len = max(max_len, window_size)
            else:
                break                      # no point extending further

    return max_len
```

### Step-by-step example

Take:

```python
s = "AABABBA"
k = 1
```

- i = 0 (start at 'A'):
  - j = 0: freq = { 'A':1 }, max_freq = 1, window = 1, replacements = 0 <= 1 → valid, max_len = 1.
  - j = 1: freq = { 'A':2 }, max_freq = 2, window = 2, replacements = 0 <= 1 → valid, max_len = 2.
  - j = 2: freq = { 'A':2, 'B':1 }, max_freq = 2, window = 3, replacements = 1 <= 1 → valid, max_len = 3.
  - j = 3: freq = { 'A':3, 'B':1 }, max_freq = 3, window = 4, replacements = 1 <= 1 → valid, max_len = 4.
  - j = 4: freq = { 'A':3, 'B':2 }, max_freq = 3, window = 5, replacements = 2 > 1 → invalid → break.

- i = 1 (start at 'A'):
  - Similar process... max window from here is at most 4, so max_len stays 4.

... and so on for all starting points.

Final answer: max_len = 4.

### Complexity

- Outer loop: O(n) starting indices.
- Inner loop: up to O(n) for each starting index.
- max(freq.values()) inside inner loop: O(26) for uppercase letters = O(1).
- Time: **O(n²)**.
- Space: **O(1)** (frequency map has at most 26 keys).

---

## Approach 2 – Optimal Sliding Window

### Intuition

The brute force restarts the frequency map for every starting index, doing redundant work.
Instead, use a sliding window that maintains a running frequency map:

- Expand the window by moving `right` forward one step at a time.
- Track `max_freq` = the highest frequency of any character seen so far in the window.
- Check if the window is valid: `window_size - max_freq <= k`.
  - If valid: window is fine, update max_len.
  - If invalid: shrink the window by moving `left` one step forward.

Key trick: you only shrink by exactly 1 when invalid, and you never shrink below the best window size seen so far. This means `max_len` only ever grows or stays the same.

### Code

```python
def character_replacement(s, k):
    freq = {}
    max_freq = 0       # highest frequency of any char in window
    left = 0
    max_len = 0

    for right in range(len(s)):
        # Add new character to window
        freq[s[right]] = freq.get(s[right], 0) + 1

        # Update max frequency seen in this window
        max_freq = max(max_freq, freq[s[right]])

        window_size = right - left + 1

        # Check if window is invalid (needs more than k replacements)
        if window_size - max_freq > k:
            # Shrink window from left by 1
            freq[s[left]] -= 1
            left += 1

        # Window is always max_len or max_len+1, update result
        max_len = max(max_len, right - left + 1)

    return max_len
```

---

## Step-by-step walkthrough

Use:

```python
s = "AABABBA"
k = 1
```

Initialize:

```python
freq = {}
max_freq = 0
left = 0
max_len = 0
```

### right = 0, s[right] = 'A'

- freq = { 'A': 1 }
- max_freq = max(0, 1) = 1
- window_size = 0 - 0 + 1 = 1
- replacements = 1 - 1 = 0 <= 1 → valid
- max_len = max(0, 1) = 1

### right = 1, s[right] = 'A'

- freq = { 'A': 2 }
- max_freq = max(1, 2) = 2
- window_size = 1 - 0 + 1 = 2
- replacements = 2 - 2 = 0 <= 1 → valid
- max_len = 2

### right = 2, s[right] = 'B'

- freq = { 'A': 2, 'B': 1 }
- max_freq = max(2, 1) = 2
- window_size = 2 - 0 + 1 = 3
- replacements = 3 - 2 = 1 <= 1 → valid
- max_len = 3

### right = 3, s[right] = 'A'

- freq = { 'A': 3, 'B': 1 }
- max_freq = max(2, 3) = 3
- window_size = 3 - 0 + 1 = 4
- replacements = 4 - 3 = 1 <= 1 → valid
- max_len = 4

### right = 4, s[right] = 'B'

- freq = { 'A': 3, 'B': 2 }
- max_freq = max(3, 2) = 3
- window_size = 4 - 0 + 1 = 5
- replacements = 5 - 3 = 2 > 1 → INVALID

Shrink from left:

- freq[s[left]] = freq['A'] -= 1 → freq = { 'A': 2, 'B': 2 }
- left = 1

Now:

- max_len = max(4, 4 - 1 + 1) = max(4, 4) = 4.

Note: max_freq is NOT decreased here. It stays at 3. This is intentional: max_freq is a historical maximum and only needs to increase (explained below).

### right = 5, s[right] = 'B'

- freq = { 'A': 2, 'B': 3 }
- max_freq = max(3, 3) = 3
- window_size = 5 - 1 + 1 = 5
- replacements = 5 - 3 = 2 > 1 → INVALID

Shrink from left:

- freq[s[1]] = freq['A'] -= 1 → freq = { 'A': 1, 'B': 3 }
- left = 2

max_len = max(4, 5 - 2 + 1) = max(4, 4) = 4.

### right = 6, s[right] = 'A'

- freq = { 'A': 2, 'B': 3 }
- max_freq = max(3, 2) = 3
- window_size = 6 - 2 + 1 = 5
- replacements = 5 - 3 = 2 > 1 → INVALID

Shrink from left:

- freq[s[2]] = freq['B'] -= 1 → freq = { 'A': 2, 'B': 2 }
- left = 3

max_len = max(4, 6 - 3 + 1) = max(4, 4) = 4.

Loop ends. Return max_len = 4.

---

## Why max_freq is never decreased

You might notice that after shrinking, max_freq is not recalculated.
This is the key trick that makes the algorithm O(n).

max_freq represents the best window (highest dominant character count) we have seen so far.
We only care about finding a window that is longer than our current max_len.
A longer window must have a higher max_freq than before.
So there is no value in shrinking max_freq: if the window with a higher max_freq is not there anymore, we just stay at the same max_len, not worse.

In other words:

- If max_freq could genuinely increase → the window might grow → we keep trying.
- If max_freq cannot increase → the window size stays the same → max_len does not grow.

This is why the window only ever shifts right as a whole rather than truly shrinking.

---

## Complexity comparison

| Approach | Time | Space | Notes |
|---------|------|-------|-------|
| Brute Force | O(n²) | O(1) | Fresh freq map per start, tries all windows |
| Sliding Window | O(n) | O(1) | Each pointer moves at most n steps, freq map has at most 26 keys |

---

## One-line takeaway

Use a sliding window with a frequency map: expand right, track the highest character frequency in the window, and shrink left by one step whenever the window needs more than k replacements — the window never truly collapses, so max_len only grows.