import re

DAY = 3
with open(f'day{DAY}_input.txt') as f:
    text = f.read()


def mul(a,b):
    return a*b

# Part 1 
def mul1(text):
    if len(text) < 3 or 'mul' not in text:
        return 0
    lines = re.findall('mul\(\d+,\d+\)',text)
    return sum([eval(line) for line in lines])
print(mul1(text))



#Part 2
def do(text):
    if len(text) < 3 or 'mul' not in text:
        return 0
    text = re.split("do()",text)
    return mul1(''.join(text[1:]))
    

def mul2(text):
    if len(text) < 3 or 'mul' not in text:
        return 0
    text = re.split("don't()",text)
    total =  mul1(text[0])
    for line in text[1:]:
        total += do(line)
    return total

print(mul2(text))


        
