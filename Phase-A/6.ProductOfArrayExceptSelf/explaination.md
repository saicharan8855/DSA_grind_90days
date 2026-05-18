\# Product of Array Except Self – Prefix and Suffix Approach



\## What’s the problem asking?



You’re given an integer array `nums`.

For each index `i`, return a new array where `answer\[i]` is the product of \*\*every element except `nums\[i]`\*\*.



Example:



\- `nums = \[1,2,3,4]` → output = `\[24,12,8,6]`



Why?



\- At index `0`: multiply `2 × 3 × 4 = 24`

\- At index `1`: multiply `1 × 3 × 4 = 12`

\- At index `2`: multiply `1 × 2 × 4 = 8`

\- At index `3`: multiply `1 × 2 × 3 = 6`



So the result becomes `\[24,12,8,6]`.



\---



\## The brute force idea



The most direct idea is simple:

for every index `i`, loop through the whole array again and multiply everything except `nums\[i]`.



\### Brute force code



```python

def product\_except\_self\_brute(nums):

&#x20;   n = len(nums)

&#x20;   result = \[]



&#x20;   # For each position, multiply everything except itself

&#x20;   for i in range(n):

&#x20;       product = 1

&#x20;       for j in range(n):

&#x20;           if i != j:           # skip the current index

&#x20;               product \*= nums\[j]

&#x20;       result.append(product)



&#x20;   return result

```



\### Why brute force is slow



For each element, you scan the entire array again.

That means `n` positions, and for each one another `n` loop, so the time complexity becomes \*\*O(n²)\*\*.



This works, but it is too slow compared to the expected linear-time solution.



\---



\## The key insight behind the optimal approach



Instead of recomputing the full product for every index, split the answer into two parts:



\- \*\*Left product\*\* = product of all elements to the left of index `i`

\- \*\*Right product\*\* = product of all elements to the right of index `i`



Then:



`answer\[i] = left\_product\[i] × right\_product\[i]`



So for `nums = \[1,2,3,4]`:



\- answer\[0] = `1 × (2×3×4)` = `24`

\- answer\[1] = `(1) × (3×4)` = `12`

\- answer\[2] = `(1×2) × (4)` = `8`

\- answer\[3] = `(1×2×3) × 1` = `6`



The beautiful trick is: you do \*\*not\*\* need separate left and right arrays.

You can store left products in the output array first, then multiply by running right products in a second pass, giving O(n) time and O(1) extra space excluding the output array.



\---



\## The optimal code



```python

def productExceptSelf(self, nums):

&#x20;   n = len(nums)

&#x20;   var =  \* n\[1]

&#x20;   

&#x20;   left = 1

&#x20;   for i in range(n):

&#x20;       var\[i] = left

&#x20;       left = left \* nums\[i]



&#x20;   right = 1

&#x20;   for i in range(n-1, -1, -1):

&#x20;       var\[i] = var\[i] \* right

&#x20;       right = right \* nums\[i]



&#x20;   return var

```



\---



\## Step-by-step walkthrough



Take:



```python

nums =\[2]\[3]\[4]\[1]

```



\### Step 1 – Initialize output array



```python

var =  \* n\[1]

```



Initially:



```python

var =\[1]

```



This array will first store left products, then be updated with right products.



\---



\### Step 2 – Left pass



```python

left = 1

for i in range(n):

&#x20;   var\[i] = left

&#x20;   left = left \* nums\[i]

```



Here, `left` means:

product of all elements \*\*before\*\* index `i`.



Walk through it:



\#### i = 0



\- `var\[0] = left = 1`

\- `left = 1 \* nums\[0] = 1 \* 1 = 1`



Now:



```python

var =\[1]

left = 1

```



\#### i = 1



\- `var\[1] = left = 1`

\- `left = 1 \* nums\[1] = 1 \* 2 = 2`



Now:



```python

var =\[1]

left = 2

```



\#### i = 2



\- `var\[2] = left = 2`

\- `left = 2 \* nums\[2] = 2 \* 3 = 6`



Now:



```python

var =\[2]\[1]

left = 6

```



\#### i = 3



\- `var\[3] = left = 6`

\- `left = 6 \* nums\[3] = 6 \* 4 = 24`



Now:



```python

var =\[5]\[2]\[1]

left = 24

```



At this point, `var\[i]` contains the product of everything to the \*\*left\*\* of index `i`.



\---



\## What does `var` mean after the left pass?



| Index | nums\[i] | Product of elements to the left | var\[i] |

|-------|---------|----------------------------------|--------|

| 0 | 1 | none → 1 | 1 |

| 1 | 2 | 1 | 1 |

| 2 | 3 | 1×2 | 2 |

| 3 | 4 | 1×2×3 | 6 |



So after the first loop:



```python

var =\[5]\[2]\[1]

```



\---



\## Step 3 – Right pass



Now multiply each `var\[i]` by the product of elements to the \*\*right\*\* of index `i`.



```python

right = 1

for i in range(n-1, -1, -1):

&#x20;   var\[i] = var\[i] \* right

&#x20;   right = right \* nums\[i]

```



Here, `right` means:

product of all elements \*\*after\*\* index `i`.



Walk through it:



\#### i = 3



\- `var\[3] = 6 \* 1 = 6`

\- `right = 1 \* nums\[3] = 1 \* 4 = 4`



Now:



```python

var =\[2]\[5]\[1]

right = 4

```



\#### i = 2



\- `var\[2] = 2 \* 4 = 8`

\- `right = 4 \* nums\[2] = 4 \* 3 = 12`



Now:



```python

var =\[6]\[5]\[1]

right = 12

```



\#### i = 1



\- `var\[1] = 1 \* 12 = 12`

\- `right = 12 \* nums\[1] = 12 \* 2 = 24`



Now:



```python

var =\[7]\[6]\[5]\[1]

right = 24

```



\#### i = 0



\- `var\[0] = 1 \* 24 = 24`

\- `right = 24 \* nums\[0] = 24 \* 1 = 24`



Final:



```python

var =\[8]\[6]\[7]\[5]

```



That is the required answer.



\---



\## Why does this work?



After the first pass:



\- `var\[i]` stores product of everything on the left.



During the second pass:



\- `right` stores product of everything on the right.

\- Multiplying them gives product of everything except the current element.



So each index becomes:



\- `var\[i] = (left product) × (right product)`



That is exactly what the problem asks for.



\---



\## Why no division?



A tempting idea is:



1\. Multiply all elements into one total product.

2\. For each index, divide total product by `nums\[i]`.



But the LeetCode problem specifically asks for a solution \*\*without division\*\*, and division also becomes tricky when zeros are present.



That’s why the prefix-suffix method is preferred.



\---



\## Complexity



\### Brute force



| Approach | Time | Space | Why |

|---------|------|-------|-----|

| Brute force | O(n²) | O(1) extra, ignoring output | For every index, scan the whole array again |



\### Optimal prefix-suffix approach



| Approach | Time | Space | Why |

|---------|------|-------|-----|

| Prefix + suffix | O(n) | O(1) extra, excluding output array | One left pass and one right pass |



This is why the second solution is considered optimal for this problem.



\---



\## One-line takeaway



Store left products in the answer array, then multiply by running right products in reverse, and each position automatically becomes the product of all elements except itself.

