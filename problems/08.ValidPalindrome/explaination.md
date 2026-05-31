# Valid Palindrome – Two Approaches (Clean + Two Pointers)

## What’s the problem asking?

You’re given a string `s`.

You need to check if it is a **valid palindrome** after:

- Converting all uppercase letters to lowercase.
- Removing all **non-alphanumeric** characters (spaces, commas, punctuation, etc.).

A string is a palindrome if it reads the same forward and backward after this cleaning.

Examples:

- `"A man, a plan, a canal: Panama"` → `true` (valid palindrome)
- `"race a car"` → `false`

---

# Approach 1 – Brute force with cleaned string

## Intuition

1. Build a **cleaned** version of `s`:
   - Keep only letters and digits.
   - Convert them all to lowercase.

2. A string is a palindrome if it is **equal to its reverse**.

3. So just compare the cleaned string with its reversed version.

## Code

```python
def is_palindrome_brute(s):
    # Step 1: Keep only alphanumeric chars, make lowercase
    cleaned = ""
    for ch in s:
        if ch.isalnum():           # isalnum() = is letter or digit
            cleaned += ch.lower()

    # Step 2: Reverse and compare
    return cleaned == cleaned[::-1]
```

## Walking through an example

Take:

```python
s = "A man, a plan, a canal: Panama"
```

## Step 1 – Clean the string

- Iterate over each character:
  - `'A'` → letter → add `'a'`
  - `' '` → space → skip
  - `'m'` → add `'m'`
  - `'a'` → add `'a'`
  - `'n'` → add `'n'`
  - `','` → skip
  - and so on...

Result:

```python
cleaned = "amanaplanacanalpanama"
```

## Step 2 – Reverse and compare

- `cleaned[::-1]` also equals `"amanaplanacanalpanama"`.
- So `cleaned == cleaned[::-1]` → `True`.

## Complexity

- Cleaning string: O(n)
- Reversing string: O(n)
- Total time: **O(n)**
- Space: **O(n)** for the cleaned copy.

This is simple and clear, but uses extra memory proportional to the input size.

---

# Approach 2 – Optimal Two-Pointer Approach

## Intuition

Instead of building a new string, use **two pointers**:

- `left` starts at the beginning.
- `right` starts at the end.

While `left < right`:

1. Skip non-alphanumeric characters on the left.
2. Skip non-alphanumeric characters on the right.
3. Compare lowercase characters at `left` and `right`:
   - If they mismatch → **not** a palindrome → return `False`.
   - If they match → move both pointers inward and continue.

If the loop finishes without mismatches → it **is** a palindrome → return `True`.

## Code

```python
def is_palindrome(s):
    left = 0
    right = len(s) - 1

    while left < right:
        # Skip non-alphanumeric from the left
        if not s[left].isalnum():
            left += 1

        # Skip non-alphanumeric from the right
        elif not s[right].isalnum():
            right -= 1

        else:
            # Both pointers on valid chars — compare them
            if s[left].lower() != s[right].lower():
                return False       # mismatch found

            left += 1
            right -= 1

    return True                    # all characters matched
```

---

# Step-by-step walkthrough (two pointers)

Use the classic example:

```python
s = "A man, a plan, a canal: Panama"
```

## Initial pointers

```python
left = 0                  # 'A'
right = len(s) - 1        # 'a'
```

- `s[left] = 'A'` (alphanumeric)
- `s[right] = 'a'` (alphanumeric)

Compare:

- `'a'` vs `'a'` (after lowercase) → match

Move pointers:

```python
left = 1
right = right - 1
```

## Skipping non-alphanumeric characters

Now at `left = 1`, `s[left] = ' '` (space):

- `not s[left].isalnum()` is `True`
- Move `left` forward:
  - `left = 2` (now `'m'`)

On the right side, if we hit `' '`, `':'`, `','` etc., we similarly move `right` leftwards until it reaches an alphanumeric.

## Continuing the comparisons

The algorithm will compare pairs like:

- `'m'` vs `'m'`
- `'a'` vs `'a'`
- `'n'` vs `'n'`

All after converting to lowercase.

If at any point:

```python
s[left].lower() != s[right].lower()
```

we immediately return `False`.

When `left` meets or passes `right`, all valid characters matched → return `True`.

---

# Why the two-pointer approach is efficient

- We scan each character at most once from either side.
- Skipping non-alphanumerics is still O(n) total because each pointer only moves inward and never backtracks.

So:

- Time: **O(n)**
- Extra space: **O(1)**

This improves on the brute-force approach by avoiding an entire cleaned copy of the string.

---

# Summary – When to use which

## Brute force (clean + reverse)

- Easiest to remember
- Very readable
- Time: O(n)
- Space: O(n)

## Two pointers (optimal)

- Same time complexity: O(n)
- Better space complexity: O(1)
- More memory-efficient
- Uses direct pointer logic with `isalnum()` and `lower()` on the fly

---

# One-line takeaway

You can either clean the string and compare it to its reverse, or more optimally, use two pointers that skip non-alphanumeric characters and compare matching characters in-place to check if the string is a valid palindrome.