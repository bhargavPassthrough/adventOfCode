
from enum import Enum
from collections import deque

DAY = 16
with open(f'2024/day{DAY}_input.txt') as f:
    LINES = f.read().splitlines()

ROWS = len(LINES)
COLS = len(LINES)

class Direction(Enum):
    NORTH = (-1,0,'^')
    EAST = (0,1,'>')
    SOUTH = (1,0,'v')
    WEST = (0,-1,'<')

NEXT_POSSIBLE_DIRECTIONS ={
    Direction.NORTH: [Direction.WEST, Direction.EAST],
    Direction.SOUTH: [Direction.WEST, Direction.EAST],
    Direction.EAST: [Direction.NORTH,Direction.SOUTH],
    Direction.WEST: [Direction.NORTH,Direction.SOUTH],
}

START = (0,0)
DESTINATION = (0,0)
GRID = []
for r in range(ROWS):
    row = []
    for c in range(COLS):
        row.append(LINES[r][c])
        if LINES[r][c]=='E':
            DESTINATION=(r,c)
        elif LINES[r][c]=='S':
            START = (r,c)
    GRID.append(row)

def out_of_bounds(r,c):
    return r>=ROWS or c>=COLS or r<0 or c<0

def bfs(best_score=-float('inf')):
    q = deque()
    seen = dict()
    score = 0
    min_score = float('inf')
    min_path = []
    q.append((*START,Direction.EAST,score,[(*START,Direction.EAST)]))
    seen[*START,Direction.EAST] = 0
    best_paths = []
    while q:
        r,c,direction,score,path = q.popleft()
        if (r,c) == DESTINATION and score<=min_score:
            min_score = score
            min_path = path

            if score == best_score:
                best_paths.append(path)
        
        for next_dir in NEXT_POSSIBLE_DIRECTIONS[direction]:
            nr,nc = r+next_dir.value[0] , c+next_dir.value[1]
            if GRID[nr][nc]=='#': #No point in turning or moving forward
                continue
            if score+1000 <= seen.get((r,c,next_dir),float('inf')):
                seen[(r,c,next_dir)] = score + 1000
                q.append((r,c,next_dir,score+1000,path+[(r,c,next_dir)]))

        nr,nc = r+direction.value[0] , c+direction.value[1]
        if not out_of_bounds(nr,nc) and GRID[nr][nc]!='#':
            if score+1 <= seen.get((nr,nc,direction),float('inf')):
                seen[(nr,nc,direction)] = score+1
                q.append((nr,nc,direction,score+1,path+[(nr,nc,direction)]))
    

    return min_path,min_score,best_paths



def part1(path,score):
    global GRID
    for r,c,dir in path:
        GRID[r][c] = dir.value[2]
    
    for r in range(ROWS):
        print(''.join(GRID[r]))
    return score


def part2(path,score):
    global GRID
    _,_,best_paths = bfs(best_score=score)
    seen = set()
    for path in best_paths:
        for x,y,_ in path:
            seen.add((x,y))
            GRID[x][y] = 'O'
    
    for r in range(ROWS):
        print(''.join(GRID[r]))

    return len(seen)


path,score,_ = bfs()
print(part1(path,score))
print(part2(path,score))