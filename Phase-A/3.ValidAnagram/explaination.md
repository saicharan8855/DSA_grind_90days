# Valid Anagram – Hash Map / Frequency Count Approach

## What's the problem again?

Same LeetCode problem: given two strings `s` and `t`, check if `t` is an anagram of `s`.  
An anagram means: **same characters with the same frequencies, order does not matter**.[web:3][web:4]

- `"anagram"` and `"nagaram"` → same letters, same counts → `True`[web:6][web:9]  
- `"rat"` and `"car"` → mismatch in letters → `False`[web:6][web:9]

---

## The core idea behind this approach

Instead of sorting, **count how many times each character appears.**  

If two strings are anagrams:

- Every character must appear **the same number of times** in both.
- If you **add 1** for each char in `s` and **subtract 1** for each char in `t`,  
  all counts should end up at **zero**.[web:4][web:5][web:9]

So the plan:

1. If lengths differ → immediately not an anagram.  
2. Use a dictionary to track counts:
   - First loop over `s`: increment counts.
   - Second loop over `t`: decrement counts.
3. At the end, if every count is zero → valid anagram.[web:4][web:9]

---

## The code (cleaned up)

```python
class Solution(object): 
    def is_anagram(self, s, t):
        if len(s) != len(t):
            return False
        return sorted(s) == sorted(t)

    """
    Complexity:
    Time  : O(n log n)
    Space : O(1) or O(n) depending on sort implementation
    """

    def is_anagram2(self, s, t):
        if len(s) != len(t):
            return False
        
        char_count = {}

        # count characters from s
        for char in s:
            if char in char_count:
                char_count[char] += 1
            else:
                char_count[char] = 1

        # subtract using characters from t
        for char in t:
            if char in char_count:
                char_count[char] -= 1
            else:
                return False

        # finally, all counts must be zero
        for count in char_count.values():
            if count != 0:
                return False

        return True
```

---

## Step-by-step walkthrough

Take `s = "anagram"`, `t = "nagaram"`.[web:6][web:9]

### 1) Length check

```python
if len(s) != len(t):
    return False
```

- `"anagram"` length = 7  
- `"nagaram"` length = 7  
- Lengths match → continue.

---

### 2) First loop – build the frequency map from `s`

```python
char_count = {}

for char in s:
    if char in char_count:
        char_count[char] += 1
    else:
        char_count[char] = 1
```

Walk through `s = "anagram"`:

- See `'a'` → not in map → `{'a': 1}`
- See `'n'` → `{'a': 1, 'n': 1}`
- See `'a'` again → `{'a': 2, 'n': 1}`
- See `'g'` → `{'a': 2, 'n': 1, 'g': 1}`
- See `'r'` → `{'a': 2, 'n': 1, 'g': 1, 'r': 1}`
- See `'a'` → `{'a': 3, 'n': 1, 'g': 1, 'r': 1}`
- See `'m'` → `{'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1}`

Now `char_count` holds frequencies for `s`.[web:2][web:9]

---

### 3) Second loop – cancel with characters from `t`

```python
for char in t:
    if char in char_count:
        char_count[char] -= 1
    else:
        return False
```

Walk through `t = "nagaram"`:

- `'n'` → exists → `n: 1 → 0`
- `'a'` → exists → `a: 3 → 2`
- `'g'` → exists → `g: 1 → 0`
- `'a'` → `a: 2 → 1`
- `'r'` → `r: 1 → 0`
- `'a'` → `a: 1 → 0`
- `'m'` → `m: 1 → 0`

End state:

```python
{'a': 0, 'n': 0, 'g': 0, 'r': 0, 'm': 0}
```

All counts are zero → so far, looks like a valid anagram.[web:4][web:9]

---

### 4) Final check – verify all counts are zero

```python
for count in char_count.values():
    if count != 0:
        return False

return True
```

Since every `count` is `0`, the function returns `True`.  
If there even **one** character with a non-zero count, that means extra or missing characters → not an anagram.[web:4][web:9]

---

## Failing example with this approach

Take `s = "rat"`, `t = "car"`:

1. Length check: both length 3 → pass.
2. After reading `s = "rat"`:

   ```python
   {'r': 1, 'a': 1, 't': 1}
   ```

3. Process `t = "car"`:
   - `'c'` is **not** in `char_count` → the code hits:

     ```python
     else:
         return False
     ```

   So it immediately returns `False` because there is a character in `t` that never appeared in `s`.[web:9]

---

## Why does this work?

Intuition:

- First loop: treat `s` as **adding** characters into a balance sheet.
- Second loop: treat `t` as **spending/removing** characters from that balance.
- If the two strings perfectly match in character frequencies, the net effect should be **zero for every character**.[web:5][web:9]

Any mismatch shows up as:

- A character appearing in `t` that was never in `s` → early `False` in `else`.
- Or a leftover non-zero value at the end → some character count did not cancel to zero → `False`.

---

## How fast is this?

Let `n` be the length of the strings (they’re the same length when we continue).[web:7][web:10][web:13]

- First loop over `s` → visits `n` characters.
- Second loop over `t` → visits `n` characters.
- Final loop over the dictionary → at most `k` keys, where `k` is the number of distinct characters (for lowercase English letters, `k` ≤ 26).

So:

- **Time Complexity**:  
  - `O(n)` for the two main loops.  
  - `O(k)` for the final check, which is `O(1)` if the alphabet is fixed/limited.  
  - Overall: **O(n)**.[web:7][web:10][web:13]

- **Space Complexity**:  
  - `O(k)` for the `char_count` dictionary; with a fixed alphabet (like lowercase English), this is effectively **O(1)** extra space.[web:7][web:10][web:13]

Compare with your sorting solution:

- Sorting approach: **O(n log n)** time.[web:3][web:10][web:13]
- Hash map approach (this one): **O(n)** time, typically faster for large `n`.[web:4][web:5][web:13]

---

## One-line takeaway

Count chars in `s`, subtract using `t`, and ensure everything cancels back to zero → that’s a clean O(n) anagram check using a hash map.

---

To make this even sharper: can you write **one or two sentences** in your own words explaining why a non-zero value in `char_count` at the end proves the strings are *not* anagrams?