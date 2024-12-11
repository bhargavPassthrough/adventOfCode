
DAY = 10
with open(f'2024/day{DAY}_input.txt') as f:
    LINES = f.read().splitlines()

ROWS = len(LINES)
COLS = len(LINES[0])

DIRECTIONS = [
    (0,1), # right
    (0,-1), # left
    (1,0), # down
    (-1,0), # up
]

def dfs1(row,col,score):
    current = LINES[row][col]
    for dx,dy in DIRECTIONS:
        r,c = row+dx,col+dy
        if r < 0 or r >= ROWS or c < 0 or c >= COLS:
            continue
        next = LINES[r][c]

        if ord(current) - ord(next) == 1:
            if not score[row][col].issubset(score[r][c]):
                score[r][c].update(score[row][col])
                dfs1(r,c,score)

def dfs2(row,col,score,path):
    current = LINES[row][col]

    if current == '0':
        for r,c in path:
            score[r][c] += 1
    
    for dx,dy in DIRECTIONS:
        r,c = row+dx,col+dy
        if r < 0 or r >= ROWS or c < 0 or c >= COLS:
            continue
        next = LINES[r][c]

        if ord(current) - ord(next) == 1:
            dfs2(r,c,score,path+[(r,c)])
            
            
        
        

def part1():
    score = []
    zeros = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(set())
            if LINES[r][c] == '0':
                zeros.append((r,c))
        score.append(row)

    for r in range(ROWS):
        for c in range(COLS):
            if LINES[r][c] == '9':
                score[r][c].add((r,c))
                dfs1(r,c,score)

    total = 0
    for r,c in zeros:
        total += len(score[r][c])
    return total

                

def part2():
    score = []
    zeros = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(0)
            if LINES[r][c] == '0':
                zeros.append((r,c))
        score.append(row)

    for r in range(ROWS):
        for c in range(COLS):
            if LINES[r][c] == '9':
                score[r][c] = 1
                dfs2(r,c,score,[(r,c)])

    total = 0
    for r,c in zeros:
        total += score[r][c]
    return total
    

print(part1())
print(part2())