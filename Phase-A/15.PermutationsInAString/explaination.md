# Permutation in String – Brute Force vs Sliding Window (Frequency Map)

## What’s the problem asking?

You’re given two strings `s1` and `s2`.

You need to check if **any permutation of `s1`** appears as a **substring** in `s2`.

- If yes → return `True`
- If no → return `False`

Examples:

- `s1 = "ab"`, `s2 = "eidbaooo"` → `True`
  - `"ba"` is a permutation of `"ab"`, and `"ba"` appears in `s2`.
- `s1 = "ab"`, `s2 = "eidboaoo"` → `False`
  - No substring of length 2 is `"ab"` or `"ba"`.

So the question is:  
“Does `s2` contain a substring of length `len(s1)` that is just a rearrangement of `s1`?”

---

## Approach 1 – Brute Force with All Permutations

### Intuition

Generate **all permutations of `s1`**, turn them into strings, and store them in a set.  
Then slide a window of length `len(s1)` over `s2`, and for each window substring, simply check if it is in that set.

If any window matches → `True`.  
If no window matches → `False`.

### Code

```python
from itertools import permutations

class Solution(object):
    def PermutationInString(self, s1, s2):
        s1_count = set("".join(p) for p in permutations(s1))
        for i in range(len(s2) - len(s1) + 1):
            if s2[i : i + len(s1)] in s1_count:
                return True
        return False
```

### How it works

1. `permutations(s1)` generates all possible reorderings of characters in `s1`.
2. `"".join(p)` converts each tuple into a string.
3. The set `s1_count` contains all distinct permutations of `s1`.
4. For each substring of `s2` of length `len(s1)`:
   - If that substring is in `s1_count` → it’s a permutation → return `True`.

Example:

```python
s1 = "ab"
s2 = "eidbaooo"

s1_count = { "ab", "ba" }

Windows of length 2 in s2:
"ei", "id", "db", "ba", "ao", "oo"

"ba" is in s1_count → return True
```

### Why this is slow

- Number of permutations of `s1` = `len(s1)!` (factorial).
- For `s1` of length 10, that’s `10! = 3,628,800` permutations.
- This explodes quickly and is not feasible for larger `s1`.

Even though membership check in a set is fast, **building** the set itself is extremely expensive.

---

## Approach 2 – Sliding Window with Frequency Counters

### Intuition

Two strings are permutations of each other **if and only if** they have the **same character frequencies**.

So instead of generating all permutations, compare **frequency maps**:

1. Count characters in `s1` once.
2. Use a sliding window of size `len(s1)` over `s2` and maintain a frequency map for the current window.
3. If at any point the window’s frequency map equals `s1`’s frequency map → the window is a permutation of `s1` → return `True`.

This is much more efficient.

### Code (corrected version)

Your second function has a couple of small issues (`left_char` used before initialization outside the if, and `[s2[i-k]]` as a list instead of a char), so here is a fixed version in the same spirit:

```python
from collections import Counter

def PermutationInString2(self, s1, s2):
    s1_count = Counter(s1)
    window = Counter()
    k = len(s1)

    if len(s2) < k:
        return False

    for i in range(len(s2)):
        # Add current character to the window
        window[s2[i]] += 1

        # Once window size exceeds k, remove the leftmost character
        if i >= k:
            left_char = s2[i - k]
            window[left_char] -= 1
            if window[left_char] == 0:
                del window[left_char]

        # When window size is exactly k, compare counters
        if i + 1 >= k and window == s1_count:
            return True

    return False
```

### Step-by-step walkthrough

Let’s use:

```python
s1 = "ab"
s2 = "eidbaooo"
k = len(s1) = 2
```

1. `s1_count = Counter("ab") = {'a':1, 'b':1}`
2. `window = {}` initially.

Iterate `i` from 0 to len(s2)-1:

#### i = 0, s2[0] = 'e'

- Add 'e': window = {'e':1}
- i + 1 = 1 < k (2) → window size < k → can’t compare yet.

#### i = 1, s2[1] = 'i'

- Add 'i': window = {'e':1, 'i':1}
- i + 1 = 2 = k → window size == k
- Compare: window = {'e':1, 'i':1}, s1_count = {'a':1, 'b':1} → not equal.

#### i = 2, s2[2] = 'd'

- Add 'd': window = {'e':1, 'i':1, 'd':1}
- Now i >= k (2), so shrink from left: left_char = s2[0] = 'e'
  - window['e'] -= 1 → 0 → delete 'e'
  - window = {'i':1, 'd':1}
- i + 1 = 3 ≥ k → compare:
  - {'i':1, 'd':1} vs {'a':1, 'b':1} → not equal.

#### i = 3, s2[3] = 'b'

- Add 'b': window = {'i':1, 'd':1, 'b':1}
- Shrink left: left_char = s2[1] = 'i'
  - window['i'] -= 1 → 0 → delete 'i'
  - window = {'d':1, 'b':1}
- Compare:
  - {'d':1, 'b':1} vs {'a':1, 'b':1} → not equal.

#### i = 4, s2[4] = 'a'

- Add 'a': window = {'d':1, 'b':1, 'a':1}
- Shrink left: left_char = s2[2] = 'd'
  - window['d'] -= 1 → 0 → delete 'd'
  - window = {'b':1, 'a':1}
- Compare:
  - window = {'b':1, 'a':1}
  - s1_count = {'a':1, 'b':1}
  - They are equal (order doesn’t matter in Counter) → return True.

We found a window `"ba"` (indices 3–4) which is a permutation of `"ab"`.

---

## Why this sliding window is efficient

- The window always has size at most `k`.
- For each index `i`, we:
  - Add one character.
  - Possibly subtract one character.
- Each character is added and removed at most once per position.
- Counter equality check is O(26) or O(128) depending on alphabet, effectively constant.

So:

- Time: **O(len(s1) + len(s2)) ≈ O(n)**.
- Space: **O(1)** extra (bounded by alphabet size, plus the frequency maps).

Compared to the factorial blowup from generating all permutations, this is dramatically faster and works for large inputs.

---

## When to use which

- **Permutation + set approach**:
  - Only acceptable for tiny `s1` (like length ≤ 7).
  - Time explodes as `len(s1)!`.

- **Sliding window + Counter (optimal)**:
  - Works efficiently for large strings.
  - The standard pattern for “check if any permutation of s1 is in s2”.

---

## One-line takeaway

Instead of generating all permutations of `s1`, treat the problem as a frequency match: slide a fixed-size window over `s2`, maintain a character frequency Counter, and return `True` if any window’s Counter equals `s1`’s Counter.