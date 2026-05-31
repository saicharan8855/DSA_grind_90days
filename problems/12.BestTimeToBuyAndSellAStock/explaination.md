# Best Time to Buy and Sell Stock – Brute Force vs One-Pass

## What's the problem asking?

You're given an array `prices` where `prices[i]` is the price of a stock on day `i`.
You want to:

- Choose one day to buy the stock, and
- Choose a later day to sell it,

such that your profit is maximized.
If no profit is possible, return 0.

Example:

- `prices = [7,1,5,3,6,4]`
  - Best is buy at 1 (day 1), sell at 6 (day 4) → profit = 5.
- `prices = [7,6,4,3,1]`
  - Prices only go down → best profit = 0 (don't trade).

---

## Approach 1 – Brute Force (Try All Pairs)

### Intuition

Check every possible pair (i, j) where:

- i = buy day
- j = sell day, and j > i

For each pair:

- Profit = prices[j] - prices[i]
- Track the maximum profit over all pairs.

### Code

```python
def max_profit_brute(prices):
    max_profit = 0
    n = len(prices)

    for i in range(n):
        for j in range(i + 1, n):
            profit = prices[j] - prices[i]   # sell on j, buy on i
            max_profit = max(max_profit, profit)

    return max_profit
```

### Step-by-step example

Take:

```python
prices =[1][2][3][4][5][6]
```

Explore pairs:

- Buy at day 0, price 7:
  - Sell at day 1: 1 - 7 = -6 → max_profit = 0
  - Sell at day 2: 5 - 7 = -2 → still 0
- Buy at day 1, price 1:
  - Sell at day 2: 5 - 1 = 4 → max_profit = 4
  - Sell at day 3: 3 - 1 = 2 → still 4
  - Sell at day 4: 6 - 1 = 5 → max_profit = 5
  - Sell at day 5: 4 - 1 = 3 → still 5

After checking all pairs, max_profit = 5.

### Complexity

- Two nested loops over n prices.
- Time: **O(n²)**.
- Space: **O(1)** extra.

This is too slow for large input sizes.

---

## Approach 2 – Optimal One-Pass (Track Min Buy and Best Profit)

### Intuition

Instead of checking all pairs, scan the array once and keep track of:

- The lowest price seen so far (best day to buy up to now).
- The maximum profit you could get if you sold today.

For each price as you move left to right:

1. If price is less than min_price → update min_price (found a cheaper buy day).
2. Otherwise → compute potential profit: price - min_price.
   - If this profit is better than max_profit → update max_profit (good sell day).

You never look back with nested loops; you only keep two running values.

### Code

```python
def max_profit(prices):
    min_price = float('inf')   # lowest buy price seen so far
    max_profit = 0             # best profit seen so far

    for price in prices:
        if price < min_price:
            min_price = price          # found a cheaper buy day
        elif price - min_price > max_profit:
            max_profit = price - min_price  # found a better sell day

    return max_profit
```

---

## Step-by-step walkthrough

Use:

```python
prices =[2][3][4][5][6][1]
```

Initialize:

```python
min_price = inf
max_profit = 0
```

### Day 0, price = 7

- price < min_price → update min_price = 7.

State:

- min_price = 7
- max_profit = 0

### Day 1, price = 1

- 1 < 7 → update min_price = 1.

State:

- min_price = 1
- max_profit = 0

### Day 2, price = 5

- 5 < 1? No.
- Profit: 5 - 1 = 4.
- 4 > 0 → update max_profit = 4.

State:

- min_price = 1
- max_profit = 4

### Day 3, price = 3

- 3 < 1? No.
- Profit: 3 - 1 = 2.
- 2 > 4? No → max_profit stays 4.

State:

- min_price = 1
- max_profit = 4

### Day 4, price = 6

- 6 < 1? No.
- Profit: 6 - 1 = 5.
- 5 > 4 → update max_profit = 5.

State:

- min_price = 1
- max_profit = 5

### Day 5, price = 4

- 4 < 1? No.
- Profit: 4 - 1 = 3.
- 3 > 5? No → max_profit stays 5.

End of loop: return max_profit = 5.

---

## What happens when prices keep falling?

Take:

```python
prices =[4][5][6][1][2]
```

- Day 0: min_price = 7
- Day 1: 6 < 7 → min_price = 6
- Day 2: 4 < 6 → min_price = 4
- Day 3: 3 < 4 → min_price = 3
- Day 4: 1 < 3 → min_price = 1

At no point does price - min_price become positive, so max_profit stays 0.
Return 0 (do not trade).

---

## Why this works

Key observation:

- For any sell day j, the best buy day before it is simply the minimum price seen so far up to day j.
- You do not need to check all (i, j) pairs explicitly.
- As you scan left to right, you always know:
  - The cheapest buy price seen so far → min_price.
  - The best profit if you sold right now → price - min_price.

So this one pass implicitly considers all (buy, sell) pairs where buy comes before sell, in linear time.

---

## Complexity comparison

### Brute Force

| What | Value | Why |
|------|-------|-----|
| Time | O(n²) | Two nested loops over prices |
| Space | O(1) | Only tracking max_profit |

### One-Pass Optimal

| What | Value | Why |
|------|-------|-----|
| Time | O(n) | Single loop over prices |
| Space | O(1) | Only two variables: min_price and max_profit |

---

## One-line takeaway

Scan prices once, keep the lowest price seen so far as your buy candidate and compute profit against it at every step, updating max_profit whenever you find a better deal — this gives you the best time to buy and sell stock in O(n) time with O(1) space.