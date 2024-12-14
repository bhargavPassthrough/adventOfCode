import re
from collections import deque
DAY = 13
with open(f'2024/day{DAY}_input.txt') as f:
    LINES = f.read().splitlines()

TOKENS_PER_BUTTON = {
    'A': 3,
    'B': 1
}

class Button:
    def __init__(self,char,x,y):
        self.char = char
        self.x = int(x)
        self.y = int(y) 
        self.tokens = TOKENS_PER_BUTTON[self.char]
        self.pushes = 100
    def __str__(self):
        return f"Button{self.char}: X+{self.x}, Y+{self.y}"

class Prize:
    def __init__(self,x,y):
        self.x = int(x)
        self.y = int(y)
    def __str__(self):
        return f"Prize: X={self.x}, Y={self.y}"

class Machine:
    def __init__(self,but_a,but_b,prize):
        self.but_a = Button('A',*but_a)
        self.but_b = Button('B',*but_b)
        self.prize = Prize(*prize)
    
    def __str__(self):
        return f"{self.but_a}\n{self.but_b}\n{self.prize}\n"
    def __repr__(self):
        return f"{self.but_a}\n{self.but_b}\n{self.prize}\n"

MACHINES = []
i = 0
while i < (len(LINES)):
    but_a = re.findall('\d+',LINES[i])
    but_b = re.findall('\d+',LINES[i+1])
    prize = re.findall('\d+',LINES[i+2])
    MACHINES.append(Machine(but_a,but_b,prize))
    i+=4



def bfs(machine):
    q = deque()
    prize = machine.prize
    q.append((prize.x,prize.y,100,100,0))
    but_a = machine.but_a
    but_b = machine.but_b
    seen = set()
    while q:
        x,y,a_pushes,b_pushes,tokens = q.popleft()
        if x == 0 and y == 0:
            return tokens
        if  x<0 or y<0 or a_pushes <=0 or b_pushes<=0:
            continue
        if (x,y,a_pushes,b_pushes) in seen:
            continue
        seen.add((x,y,a_pushes,b_pushes))
        for but,*pushes in [(but_a,a_pushes-1,b_pushes),(but_b,a_pushes,b_pushes-1)]:
            q.append((x-but.x,y-but.y,*pushes,tokens+but.tokens))
    
    return 0

def formula(machine):
    # ax1 + bx2 = x , ay1 + by2 = y
    # a = (x- bx2)/x1 , a = (y - by2)/y1
    # (x- bx2)/x1 == (y - by2)/y1
    # x/x1 - bx2/x1 = y/y1 - by2/y1
    # x/x1 - y/y1 = b(x2/x1 - y2/y1)
    # (xy1 -yx1) /x1y1 = b( (x2y1-y2x1) /x1y1)
    # b = (xy1 - yx1)/x1y1 * x1y1 / (x2y1 - y2x1)
    # b = (xy1 - yx1) / (x2y1 - y2x1)
    # a = (x-bx2)/x1
    x,y = machine.prize.x,machine.prize.y
    x1,y1=machine.but_a.x,machine.but_a.y
    x2,y2 = machine.but_b.x,machine.but_b.y
    b = (x*y1-y*x1)/(x2*y1-y2*x1)
    if int(b)!=b:
        return 0
    a = (x-b*x2)/x1
    if int(a)!=a:
        return 0
    return a*3 + b

def part1():
    tokens = 0
    for machine in MACHINES:
        tokens += bfs(machine)
    return tokens


def part2():
    tokens = 0
    for num,machine in enumerate(MACHINES):
        machine.prize.x+=10000000000000
        machine.prize.y+=10000000000000
        tokens += formula(machine)
    return tokens


print(part1())
print(part2())