# Min Stack – Naive vs Optimized (Two Stacks)

## What’s the problem asking?

You need to design a stack that, in addition to normal operations:

- `push(x)` – push an element
- `pop()` – remove top
- `top()` – get top

also supports:

- `getMin()` – return the **minimum element in the stack**

And all of these should ideally be **O(1)** time per operation.

---

## Approach 1 – Single Stack, `getMin` scans everything

### Intuition

Use a normal stack (e.g. a Python list) to store values.  
To find the minimum, just take `min(self.stack)` whenever `getMin` is called.  
This is easy to write but **slow** for `getMin`.

### Code

```python
class MinStack:

    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append(val)        # add to top

    def pop(self):
        self.stack.pop()              # remove from top

    def top(self):
        return self.stack[-1]         # peek at top

    def getMin(self):
        return min(self.stack)        # scan entire stack — O(n)
```

### How it behaves

- `push`, `pop`, `top` are O(1).
- `getMin` is O(n) because `min(self.stack)` must scan all elements.

Example:

```python
st = MinStack()
st.push(5)       # stack =[1]
st.push(3)       # stack =[2][1]
st.push(7)       # stack =[3][1][2]

st.getMin()      # min() = 3   (O(n))[1][2][3]
st.pop()         # stack =[2][1]
st.getMin()      # min() = 3[1][2]
```

Correct, but not optimal.

---

## Approach 2 – Two Stacks (Main + Min Stack)

### Core idea

Track the current minimum **at each position** of the stack.  
Use:

- `self.stack` – stores the actual values.
- `self.min_stack` – stores the **minimum value so far** (up to that index).

For every push/pop, you update both stacks so that:

- The top of `min_stack` is always the minimum of all values currently in `stack`.

### Code

```python
class MinStack:

    def __init__(self):
        self.stack = []
        self.min_stack = []          # tracks minimum at each stack state

    def push(self, val):
        self.stack.append(val)
        # Push the new minimum: either val itself or current min
        if self.min_stack:
            self.min_stack.append(min(val, self.min_stack[-1]))
        else:
            self.min_stack.append(val)   # first element is trivially the min

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()         # restore previous minimum state

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]    # always O(1)
```

---

## Step-by-step walkthrough

Take a sequence of operations:

```python
st = MinStack()
st.push(5)
st.push(3)
st.push(7)
st.push(2)
```

Track both stacks:

1. `push(5)`
   - `stack = [5]`
   - `min_stack = [5]`  
     (first value is also current min)

2. `push(3)`
   - `stack.append(3)` → `[5, 3]`
   - `min_stack[-1] = 5`, `min(3, 5) = 3` → `min_stack = [5, 3]`
   - Meaning: up to index 0, min is 5; up to index 1, min is 3.

3. `push(7)`
   - `stack = [5, 3, 7]`
   - `min_stack[-1] = 3`, `min(7, 3) = 3` → `min_stack = [5, 3, 3]`
   - Min stays 3; store that again at the same index.

4. `push(2)`
   - `stack = [5, 3, 7, 2]`
   - `min_stack[-1] = 3`, `min(2, 3) = 2` → `min_stack = [5, 3, 3, 2]`

Now:

- `top()` → `stack[-1] = 2`
- `getMin()` → `min_stack[-1] = 2` (O(1))

If we `pop()`:

- `stack.pop()` → stack becomes `[5, 3, 7]`
- `min_stack.pop()` → min_stack becomes `[5, 3, 3]`
- Now `getMin()` → `3` (still correct and O(1))

Notice how `min_stack` always mirrors the length of `stack`.  
At each index `i`, `min_stack[i]` stores the minimum value among `stack[0..i]`.

---

## Why this gives O(1) `getMin`

- Every push and pop updates `min_stack` in O(1).
- The current minimum at any time is just the **top** of `min_stack`.
- No scanning is needed.

Complexities:

- `push`: O(1)
- `pop`: O(1)
- `top`: O(1)
- `getMin`: O(1)
- Space: O(n) (extra min_stack of same length as stack)

---

## One-line takeaway

Store, alongside every pushed value, the minimum value **up to that point** in a parallel stack; then `getMin()` is just peeking at the top of that min-stack in O(1) time.