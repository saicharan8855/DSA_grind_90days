# Group Anagrams – Frequency-Count (Optimal) Approach

## What’s the problem asking?

You’re given a list of strings and asked to **group all the anagrams together**.  
Each group should contain words that are anagrams of each other.[web:16][web:22]

Example:

- `["eat","tea","tan","ate","nat","bat"]`  
  Possible output (order doesn’t matter):  
  - `["eat","tea","ate"]`  
  - `["tan","nat"]`  
  - `["bat"]`

Same idea as *valid anagram*, but now you must group **many** words at once instead of just checking a pair.

---

## The key insight behind this approach

Anagrams share the **same character frequency pattern**:

- `"eat"` → one `e`, one `a`, one `t`  
- `"tea"` → one `t`, one `e`, one `a`  
- `"ate"` → one `a`, one `t`, one `e`

Order changes, but the **frequency of each letter** stays identical.[web:23][web:26][web:29]

So if you:

1. Build a 26-length frequency array for each string (for `a` to `z`),  
2. Use that frequency array (converted to a tuple) as a **key** in a hash map,

…then all anagrams will automatically end up under the **same key** (same “fingerprint”), and you’ve grouped them.

---

## The optimal code (frequency-count hash key)

```python
from collections import defaultdict

def group_anagrams_optimal(strs):
    anagram_map = defaultdict(list)

    for s in strs:
        count =  * 26  # index 0='a', index 1='b', ..., index 25='z'

        for c in s:
            count[ord(c) - ord('a')] += 1  # map char to index 0–25 via ASCII shift

        key = tuple(count)          # convert list → tuple (lists are NOT hashable)
        anagram_map[key].append(s)  # group under frequency fingerprint

    return list(anagram_map.values())
```

- `anagram_map`: maps a “frequency fingerprint” → list of words.  
- `count`: captures “how many a’s, how many b’s, …, how many z’s”.  
- `key`: tuple version of `count`, used as a dictionary key.[web:24][web:26][web:29]

---

## Walking through an example step-by-step

Take:

```python
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
```

### 1) Initialize the data structure

```python
anagram_map = defaultdict(list)
```

- Empty map initially, but any new key will start with an empty list automatically.[web:22][web:24]

---

### 2) Process `"eat"`

```python
s = "eat"
count =  * 26
```

Now loop over characters:

- See `'e'`:  
  - `ord('e') - ord('a')` → index 4  
  - `count[4] += 1`
- See `'a'`: index 0 → `count[0] += 1`
- See `'t'`: index 19 → `count[19] += 1`

So `count` looks like (showing only non-zero indices conceptually):

- index 0 (`'a'`) → 1  
- index 4 (`'e'`) → 1  
- index 19 (`'t'`) → 1  

Convert this to a key:

```python
key = tuple(count)
anagram_map[key].append("eat")
```

Now `anagram_map` has one entry where that frequency pattern maps to `["eat"]`.[web:23][web:26][web:29]

---

### 3) Process `"tea"`

```python
s = "tea"
count =  * 26
```

Loop over `'t'`, `'e'`, `'a'`:

- `'t'` → index 19 → +1  
- `'e'` → index 4 → +1  
- `'a'` → index 0 → +1  

End result for `count` is **identical** to `"eat"`’s count.  
So `key = tuple(count)` is the same key as before.[web:23][web:29]

Then:

```python
anagram_map[key].append("tea")
```

Now that same key’s group is `["eat", "tea"]`.

---

### 4) Process `"tan"` and `"nat"`

For `"tan"`:

- `'t'` → index 19  
- `'a'` → index 0  
- `'n'` → index 13  

For `"nat"` you get the exact same frequency pattern again.  
So they share another key, and that group becomes `["tan", "nat"]`.

---

### 5) Process `"ate"`

`"ate"` has the same letters as `"eat"` and `"tea"`, so its frequency count matches their key as well.  
The corresponding list becomes `["eat", "tea", "ate"]`.

---

### 6) Process `"bat"`

New pattern:

- `'b'` → index 1  
- `'a'` → index 0  
- `'t'` → index 19  

Different from all previous keys, so `"bat"` starts its own group.[web:26][web:29]

---

### 7) Final result

At the end, `anagram_map`’s values are:

- `["eat", "tea", "ate"]`
- `["tan", "nat"]`
- `["bat"]`

So the function returns:

```python
[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

Order of groups or elements inside groups does not matter.[web:16][web:29]

---

## Why use the frequency-array key instead of sorting?

Sorting-based grouping (`"".join(sorted(s))` as key) is simpler to think about, but sorting each string takes `O(K log K)` per string, where `K` is string length.[web:21][web:22][web:29]

With the frequency array approach:

- For each word:
  - Building the `count` array is `O(K)` (one pass over characters).[web:23][web:26][web:29]
- No per-string sorting step.

So if:

- `n` = number of strings  
- `K` = max length of a string  

Then:

- **Time Complexity**: `O(n * K)` (linear in total characters processed).[web:20][web:26][web:29]  
- **Space Complexity**: `O(n * K)` in the worst case (storing all strings + keys), though the key itself per group is of fixed length 26 for lowercase English.[web:20][web:26][web:29]

This is usually faster than `O(n * K log K)` when `K` is large.

---

## One-line takeaway

Convert each string into a 26-length character-frequency fingerprint, use that fingerprint as a hash map key, and all anagrams automatically fall into the same group.

---

To lock this in: if you had the strings `["abc", "bca", "cab", "abb"]`, how would you describe, in your own words, why the first three end up in one group and `"abb"` in a different one using this frequency-array idea?
