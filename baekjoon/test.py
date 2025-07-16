def count_change(amount, coins):
    if amount == 0:
        print(coins)
        return 1
    if amount < 0 or len(coins) == 0:
        return 0
    return count_change(amount, coins[1:]) + count_change(amount - coins[0], coins) 


print(count_change(4, [1,2,3]))
