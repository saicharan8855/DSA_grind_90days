# Container With Most Water – Brute Force vs Two Pointers

## What’s the problem asking?

You’re given an array `height` where `height[i]` represents the height of a vertical line at position `i`.  
Pick any two lines; together with the x-axis, they form a container.  
You need to find **the maximum amount of water** this container can store.

Key idea:

- The area (water) between lines at `i` and `j` is:
  - `height = min(height[i], height[j])`  (limited by the shorter line)
  - `width = j - i`
  - `area = height * width`

Example:

- `height = [1,8,6,2,5,4,8,3,7]`
- One optimal pair is at indices 1 and 8 (values 8 and 7):
  - height = 7
  - width = 8 - 1 = 7
  - area = 7 × 7 = 49

Answer: `49`.

---

## Approach 1 – Brute Force (Check All Pairs)

### Intuition

Try every possible pair of lines:

- For each `i`
  - For each `j > i`
    - Compute the area between `i` and `j`
    - Track the maximum area seen so far

We directly apply the area formula for each pair.

### Code

```python
def max_area_brute(height):
    max_water = 0
    n = len(height)

    for i in range(n):
        for j in range(i + 1, n):
            # Water level limited by shorter line
            h = min(height[i], height[j])
            # Width is the distance between lines
            w = j - i
            area = h * w
            max_water = max(max_water, area)

    return max_water
```

### Step-by-step example

Let:

```python
height =[1][2][3][4][5][6][7][8]
```

- i = 0, j = 1:
  - h = min(1, 8) = 1
  - w = 1 - 0 = 1
  - area = 1 × 1 = 1
  - max_water = 1
- i = 0, j = 2:
  - h = min(1, 6) = 1
  - w = 2
  - area = 1 × 2 = 2
  - max_water = 2
- ...
- i = 1, j = 8:
  - h = min(8, 7) = 7
  - w = 8 - 1 = 7
  - area = 7 × 7 = 49
  - max_water = 49

Eventually, every pair is checked, and `max_water` ends up as `49`.

### Complexity

- Time: **O(n²)** (two nested loops over `height`).
- Space: **O(1)** extra.

Works, but too slow for large `n`.

---

## Approach 2 – Optimal Two-Pointer Strategy

### Core intuition

The brute force is slow because it checks all pairs blindly.  
We need a way to **skip** many pairs without missing the maximum.

Observation:

- Area is `min(height[i], height[j]) * (j - i)`.
- For a fixed pair `(i, j)`, if we want to potentially find a bigger area:
  - We need **larger width** or **greater minimum height**.
- If we move the taller line inward, the width shrinks and the minimum height cannot increase (since the smaller side hasn’t changed).
- But if we move the **shorter line** inward, we might find a **taller line** that increases the minimum height and compensate for the reduced width.

So the greedy rule:

- Start with two pointers at the ends (`left = 0`, `right = n-1`).
- At each step:
  - Compute area between `left` and `right`.
  - Move the pointer on the **shorter** line inward:
    - If `height[left] < height[right]` → `left += 1`
    - Else → `right -= 1`

This way, we only move the pointer that could possibly lead to a higher `min(height[left], height[right])`.

### Code

```python
def maxArea(self, height):
    left = 0
    right = len(height) - 1
    maximum_area = 0

    while left < right:
        distance = right - left 
        minimum_height = min(height[left], height[right])
        area = distance * minimum_height

        if area > maximum_area:
            maximum_area = area
        
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return maximum_area
```

---

## Step-by-step walkthrough

Again use:

```python
height =[2][3][4][5][6][7][8][1]
```

### Initial state

- `left = 0`, `right = 8`
- `height[left] = 1`, `height[right] = 7`
- `distance = 8 - 0 = 8`
- `minimum_height = min(1, 7) = 1`
- `area = 8 × 1 = 8`
- `maximum_area = 8`

Now decide which pointer to move:

- `height[left] < height[right]` → 1 < 7 → move `left`:

```python
left = 1
```

### Next iteration

- `left = 1`, `right = 8`
- `height[left] = 8`, `height[right] = 7`
- `distance = 7`
- `minimum_height = min(8, 7) = 7`
- `area = 7 × 7 = 49`
- `maximum_area = 49`

Now move the **shorter** side:

- `height[left] = 8`, `height[right] = 7`
- shorter is `height[right]` → move `right`:

```python
right = 7
```

### Another iteration (just one more)

- `left = 1`, `right = 7`
- `height[left] = 8`, `height[right] = 3`
- `distance = 6`
- `minimum_height = 3`
- `area = 6 × 3 = 18`
- `maximum_area` stays `49`

`height[right]` is shorter (3 < 8) → `right -= 1`.

The loop continues shrinking the window, always moving the shorter side, updating `maximum_area` when a larger area is found. No configuration can beat the `49` found earlier.

When `left >= right`, the loop ends and `maximum_area` is returned.

---

## Why moving the shorter pointer makes sense

Consider two lines at positions `i` and `j`:

- Current area = `min(h[i], h[j]) * (j - i)`

Suppose `h[i] <= h[j]` (left side is shorter).  
If you move `right` inward:

- The width `j - i` decreases.
- The minimum height remains at most `h[i]` (since the shorter line is still the same or smaller).
- So the area cannot become larger than the best you could get by moving `left`.

But if you move `left` (the shorter line) inward:

- Width decreases.
- However, you might find a taller line on the left side, increasing the minimum height enough to get a larger area.

Thus, to explore potentially better containers, always move the pointer on the **shorter** line.

---

## Complexity comparison

### Brute Force

- Time: **O(n²)** (all pairs).
- Space: **O(1)**.

### Two Pointers

- Time: **O(n)** (single pass, each pointer moves inward at most n steps).
- Space: **O(1)**.

The two-pointer approach is the optimal solution for this problem.

---

## One-line takeaway

Start with the widest container (two ends), compute the area, and always move the pointer on the shorter line inward; this simple rule, applied while tracking the maximum area, finds the container with most water in O(n) time.