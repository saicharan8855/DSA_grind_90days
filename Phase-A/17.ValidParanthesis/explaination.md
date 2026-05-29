# Valid Parentheses – Brute Force vs Stack

## What is the problem?

You’re given a string `s` containing only the characters:

- `'(' , ')' , '[' , ']' , '{' , '}'`

You must check if `s` is a **valid parentheses string**. A string is valid if:

1. Every opening bracket has a matching closing bracket of the **same type**, and  
2. Brackets are closed in the **correct order** (properly nested).

Examples:

- `"()"` → valid  
- `"()[]{}"` → valid  
- `"(]"` → invalid  
- `"([)]"` → invalid  
- `"{[]}"` → valid  

---

## Approach 1 – Brute Force by Repeated Replacement

### Intuition

In any valid expression, parentheses appear in **adjacent matching pairs** at some level:

- `"()"`, `"[]"`, `"{}"`
- More complex ones like `"{[()]}"` can be reduced step by step:
  - `"{[()]}"` → `"{[]}"` (remove `"()"`)  
  - `"{[]}"` → `"{}"` (remove `"[]"`)  
  - `"{}"` → `""` (remove `"{}"`)

So if the string is valid, you can repeatedly remove these adjacent pairs until the string becomes empty.  
If, after removing all possible pairs, the string is **not** empty, it means something is unmatched or mis-ordered.

### Code

```python
def is_valid_brute(s):
    # Keep removing adjacent valid pairs until none remain
    while "()" in s or "[]" in s or "{}" in s:
        s = s.replace("()", "")
        s = s.replace("[]", "")
        s = s.replace("{}", "")

    # If nothing left, all brackets were matched
    return s == ""
```

### How it works step-by-step

Take `s = "{[()]}"`:

1. `"()"` is inside → replace:
   - `"{[()]}"` → `"{[]}"`  
2. `"[]"` is inside → replace:
   - `"{[]}"` → `"{}"`  
3. `"{}"` is inside → replace:
   - `"{}"` → `""`  
4. String is empty → return `True`.

Take `s = "([)]"`:

1. Contains `"()"`? No. `"[]"`? No. `"{}"`? No.  
2. Loop doesn’t change `s`.  
3. `s` is `"([)]"` ≠ `""` → return `False`.

### Complexity

- Each `replace` scan is O(n), and you may repeat it many times.
- Worst-case time is roughly **O(n²)**.
- Space: O(n) due to string copies.

It’s simple to understand but not efficient.

---

## Approach 2 – Optimal Stack-Based Solution

### Intuition

Use a **stack** to keep track of opening brackets.

Key idea:

- When you see an **opening** bracket, push it onto the stack.
- When you see a **closing** bracket:
  - The most recent unmatched opening bracket must be on **top** of the stack.
  - If the stack is empty or top doesn’t match the closing one → invalid.
  - If it matches → pop the stack (pair matched).

At the end:

- If the stack is empty → all brackets are properly matched → valid.
- If not → there are unmatched openings → invalid.

### Code

```python
def is_valid(s):
    # Map each closing bracket to its matching opener
    match = {')': '(', ']': '[', '}': '{'}
    stack = []

    for ch in s:
        if ch in match:
            # It's a closing bracket
            # Check if stack is non-empty and top matches
            if not stack or stack[-1] != match[ch]:
                return False
            stack.pop()              # valid pair found, remove opener
        else:
            stack.append(ch)         # it's an opening bracket, push it

    return len(stack) == 0           # stack must be empty at end
```

### Step-by-step example

Take `s = "{[()]}"`:

- Start: `stack = []`

1. `'{'` → not in `match` → opening → push  
   stack = `['{']`
2. `'['` → opening → push  
   stack = `['{', '[']`
3. `'('` → opening → push  
   stack = `['{', '[', '(']`
4. `')'` → closing  
   - `match[')'] = '('`  
   - top of stack is `'('` → matches → pop  
   stack = `['{', '[']`
5. `']'` → closing  
   - `match[']'] = '['`  
   - top is `'['` → matches → pop  
   stack = `['{']`
6. `'}'` → closing  
   - `match['}'] = '{'`  
   - top is `'{'` → matches → pop  
   stack = `[]`

End: `stack` is empty → return `True`.

Now `s = "([)]"`:

- `stack = []`
- `'('` → push → `['(']`
- `'['` → push → `['(', '[']`
- `')'` → closing, expected `'('`  
  - `match[')'] = '('` but top is `'['` → mismatch → return `False`.

### Complexity

- Single pass over `s`, each char pushed/popped at most once.
- Time: **O(n)**.
- Space: **O(n)** in worst case (all openings).

---

## When to use which

- **Brute force (replace pairs)**:
  - Very easy to code and reason about.
  - Too slow for large strings (O(n²)).

- **Stack approach (recommended)**:
  - Standard interview solution.
  - Linear time, clean logic based on matching last-opened with next-closing.

---

## Quick mental model

Think of opening brackets as **“tasks started”** and closing brackets as **“tasks finished”**:

- A stack represents the current tasks in progress.
- Every time you finish a task (closing bracket), it must be the **most recent** one you started (top of the stack).
- If at the end there are unfinished tasks (stack not empty), or you finish a task that was never started (closing with empty stack), something is wrong → invalid.

If you want, next you can try to walk through the stack algorithm yourself on a custom example like `"{[()()]}"` and explain what happens at each step.