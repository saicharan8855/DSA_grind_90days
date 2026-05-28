# Minimum Window Substring – Brute Force vs Sliding Window

## What’s the problem asking?

You’re given two strings `s` (the source) and `t` (the target).  
Find the **smallest substring of `s`** that contains **all characters of `t`**, including duplicates.

- If such a substring exists → return it.
- If not → return `""`.

Examples:

- `s = "ADOBECODEBANC"`, `t = "ABC"` → minimum window is `"BANC"`.
- `s = "a"`, `t = "a"` → minimum window is `"a"`.
- `s = "a"`, `t = "aa"` → no such window → return `""`.

Think of `t` as a shopping list and `s` as a street of shops; you need the **shortest stretch** of shops where you can buy everything on the list.

---

## Approach 1 – Easy Brute Force (Try All Starts, Expand)

### Intuition

For each starting position `i` in `s`:

1. Start with an empty `current` string.
2. Expand the end index `j` from `i` to the end of `s`, appending `s[j]` to `current`.
3. After each expansion, check if `current` contains all characters of `t` with the right counts.
4. If it does:
   - Update `smallest` if this is the shortest valid window so far.
   - Break for this starting index (no need to extend further; longer will only be worse).

This is a very literal but slow solution.

### Code

```python
def min_window_easy(s, t):

    smallest = ""

    # try every starting position
    for i in range(len(s)):

        current = ""

        # expand window to the right
        for j in range(i, len(s)):

            current += s[j]

            # check if current window is valid
            ok = True

            for ch in t:
                if current.count(ch) < t.count(ch):
                    ok = False
                    break

            # if valid
            if ok:

                # update smallest answer
                if smallest == "" or len(current) < len(smallest):
                    smallest = current

                break

    return smallest
```

### Why it’s slow

For each start `i`:

- Inner loop extends `j` over up to `n` positions.
- For each `(i, j)` window, `current.count(ch)` runs over the window again.

So:

- Number of windows: O(n²)
- Checking counts: up to O(n) per window
- Total: roughly **O(n³)** in the worst case.

This is fine for understanding, but not for big inputs.

---

## Approach 2 – Optimal Sliding Window with Frequency Maps

### Core idea

Instead of checking windows from scratch, maintain:

- A **frequency map** `freq_t` for `t`, telling how many of each character are required.
- A **frequency map** `freq_window` for the current window in `s`.
- Two integers:
  - `have`: how many distinct characters currently meet their required counts.
  - `need`: total distinct characters required (i.e., `len(freq_t)`).

Use a variable-size sliding window `[left, right]`:

1. Expand `right` to include more characters until the window is **valid** (contains all required counts).
2. Once valid, try to **shrink from `left`** to find the smallest valid window.
3. Track the best (shortest) window seen so far.

### Code

```python
def min_window(s, t):
    if not t or not s:
        return ""

    # Frequency map for t
    freq_t = {}
    for ch in t:
        freq_t[ch] = freq_t.get(ch, 0) + 1

    freq_window = {}
    have = 0                        # unique chars meeting required count
    need = len(freq_t)              # total unique chars needed

    left = 0
    min_len = float('inf')
    result = ""

    for right in range(len(s)):
        ch = s[right]
        freq_window[ch] = freq_window.get(ch, 0) + 1

        # Check if this char now meets its required count
        if ch in freq_t and freq_window[ch] == freq_t[ch]:
            have += 1

        # Window is valid — try to shrink from left
        while have == need:
            # Update minimum window
            if (right - left + 1) < min_len:
                min_len = right - left + 1
                result = s[left : right + 1]

            # Remove leftmost character
            left_ch = s[left]
            freq_window[left_ch] -= 1

            # Check if removing it breaks validity
            if left_ch in freq_t and freq_window[left_ch] < freq_t[left_ch]:
                have -= 1

            left += 1

    return result
```

---

## Step-by-step walkthrough

Use the classic example:

```python
s = "ADOBECODEBANC"
t = "ABC"
```

### Step 1 – Build freq_t

```python
freq_t = { 'A':1, 'B':1, 'C':1 }
need = 3
```

`have = 0` initially, because no characters are satisfied yet.

### Step 2 – Slide right pointer

We move `right` from 0 to len(s)-1, updating `freq_window`:

- right = 0, ch = 'A'
  - freq_window = {'A':1}
  - 'A' in freq_t and freq_window['A'] == freq_t['A'] → have = 1
  - have (1) != need (3) → not valid yet.

- right = 1, ch = 'D'
  - freq_window = {'A':1, 'D':1}
  - 'D' not in freq_t → have unchanged.

- right = 2, ch = 'O'
  - freq_window = {'A':1, 'D':1, 'O':1} → have still 1.

- right = 3, ch = 'B'
  - freq_window['B'] = 1
  - 'B' in freq_t, and counts match → have = 2.

- right = 4, ch = 'E'
  - freq_window['E'] = 1 → have still 2.

- right = 5, ch = 'C'
  - freq_window['C'] = 1
  - 'C' in freq_t, and counts match → have = 3.

Now `have == need == 3`, which means the current window `[left, right] = [0, 5]` (substring `"ADOBEC"`) is **valid**.

### Step 3 – Shrink from the left

While `have == need`, we try to minimize the window:

Window `[0, 5]` → `"ADOBEC"`

- Current length = 6, min_len = 6, result = `"ADOBEC"`

Now shrink:

- left = 0, left_ch = `s[0] = 'A'`
  - freq_window['A'] becomes 0
  - 'A' in freq_t and 0 < 1 → `have` decreases to 2.
- left becomes 1.

Now `have` (2) < `need` (3) → window is no longer valid.  
Stop shrinking.

Current best result: `"ADOBEC"`.

### Step 4 – Continue expanding right

Continue sliding `right`:

- right = 6, ch = 'O'
- right = 7, ch = 'D'
- right = 8, ch = 'E'
- right = 9, ch = 'B'
- right = 10, ch = 'A'
- right = 11, ch = 'N'
- right = 12, ch = 'C'

Key point: when `right` reaches 9, 10, 12, the window again becomes valid (contains A, B, C with correct counts).

Eventually, when `right = 12` and left has moved forward correctly, the algorithm finds the smallest valid window `"BANC"`:

- length 4, smaller than previous 6 → update result to `"BANC"`.

---

## Why the sliding window is efficient

Notice how:

- Each character enters the window (at `right`) at most once.
- Each character leaves the window (at `left`) at most once.
- `freq_window` and `freq_t` are updated incrementally.
- `have` and `need` let you quickly test validity without scanning the whole window.

So:

- Time: **O(len(s) + len(t)) ≈ O(n)**  
  (each index visited a constant number of times)
- Space: **O(unique characters)** for the hash maps.

Compared to the brute force idea that re-counts and re-checks many substrings, this is dramatically faster.

---

## One-line takeaway

Use a sliding window with two frequency maps and `have/need` counters: expand `right` until the window covers all of `t`, then shrink from `left` to find the smallest valid window, updating the best result along the way.