DAY = 11
with open(f'2024/day{DAY}_input.txt') as f:
    LINE = list(f.read().split())


def split_stone(stone):
    mid = len(stone)//2
    left = str(int(stone[:mid]))
    right = str(int(stone[mid:]))
    return left,right


def blink(stone,num_blinks,dp):
    
    if stone in dp[num_blinks]:
        return dp[num_blinks][stone]
    if num_blinks == 0:
        return 1
    
    if stone == '0':
        stones = blink('1',num_blinks-1,dp)
    
    elif len(stone)%2 == 0:
        left,right = split_stone(stone)
        stones = blink(left,num_blinks-1,dp) + \
                 blink(right,num_blinks-1,dp)
    else:
        stones = blink(str(int(stone)*2024),num_blinks-1,dp)
    
    dp[num_blinks][stone] = stones
    return stones


def get_stones(num_blinks,stones):
    dp = [dict() for blink in range(num_blinks+1)]
    return sum(blink(stone,num_blinks,dp) for stone in stones)

def part1():
    return get_stones(25,LINE)

def part2():
    return get_stones(75,LINE)

print(part1())
print(part2())