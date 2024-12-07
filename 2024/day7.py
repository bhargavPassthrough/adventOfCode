DAY = 7
with open(f'2024/day{DAY}_input.txt') as f:
    lines = f.read().splitlines()

OPERATORS = {
    '+':lambda a,b: a+b,
    '*': lambda a,b: a*b,
}

DEFAULT_VALUES={
    '+': 0,
    '*':1,
    '||':0,
}



def valid(value,nums,current_index,length,current_value=None):
    if current_index == length:
        return current_value == value
    
    if current_value and current_value > value:
        return False
    
    is_valid = False
    for operator,operation in OPERATORS.items():
        if not current_value:
            current_value = DEFAULT_VALUES[operator]
        val = operation(current_value,nums[current_index])
        is_valid = is_valid or valid(value,nums,current_index+1,length,val) 
        if is_valid:
            return True
    
    return is_valid
    

def part1():
    total = 0
    for line in lines:
        value , *rest = line.split(': ')
        value = int(value)
        nums = list(map(int,rest[0].split()))
        if valid(value,nums,0,len(nums)):
            total += value
    return total

def part2():
    global OPERATORS
    OPERATORS['||'] = lambda a,b: int(str(a)+str(b))
    return part1()

print(part1())  
print(part2())