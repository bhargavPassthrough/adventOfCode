from collections import deque
from enum import Enum
DAY = 12
with open(f'2024/day{DAY}_input.txt') as f:
    LINES = f.read().splitlines()


ROWS = len(LINES)
COLS = len(LINES[0])
DIRECTIONS = [
    (-1,0), #up
    (1,0), #down
    (0,-1), #left
    (0,1), #right
]



def within_range(row,col):
    return row<ROWS and row>=0 and col<COLS and col>=0


def bfs(grid,row,col,seen):
    q = deque()
    q.append((row,col))
    area = 0
    perimeter = 0
    plant = grid[row][col]
    while q:
        row,col = q.popleft()
        if (row,col) in seen or not within_range(row,col) or grid[row][col]!=plant:
            continue
        seen.add((row,col))
        current_perimeter = 4
        for dr,dc in DIRECTIONS:
            r,c = row+dr,col+dc
            if within_range(r,c) and grid[r][c]==plant:
                q.append((r,c))
                current_perimeter-=1
            
        
        area+=1
        perimeter+=current_perimeter
    
    return area,perimeter

def part1():
    price = 0
    grid = []
    for r in range(ROWS):
        grid.append([LINES[r][c] for c in range(COLS)])
    
    seen = set()
    for r in range(ROWS):
        for c in range(COLS):
            if (r,c) not in seen:
                area,perimeter = bfs(grid,r,c,seen)
                price+=area*perimeter
                
    return price


class Direction(Enum):
    LEFT = (0,-1)
    RIGHT = (0,1)
    UP = (-1,0)
    DOWN = (1,0)


class Plant:
    def __init__(self,char,row,col):
        self.row = row
        self.col = col
        self.char = char
        self.up = None
        self.left = None
        self.down = None
        self.right = None
        self.sides = set()
    
    def __repr__(self):
        return str((self.row,self.col,self.char))


def same_plant(plant,direction,grid):
    dr,dc = direction.value
    r,c = plant.row+dr,plant.col+dc
    if not within_range(r,c):
        return False
    next_plant = grid[r][c]
    return next_plant.char == plant.char


def get_sides(grid,row,col,seen):
    q = deque()
    area = 0
    total_sides = 0
    q.append(grid[row][col])
    
    while q:
        plant = q.popleft()
        
        if not plant or (plant.row,plant.col) in seen:
            continue
        seen.add((plant.row,plant.col))
        
        #up
        if not plant.up and Direction.UP not in plant.sides:
            plant.sides.add(Direction.UP)
            shared = (plant.left and Direction.UP in plant.left.sides) or \
                (plant.right and Direction.UP in plant.right.sides)
            
            if not shared:
                total_sides+=1
        
        #down
        if not plant.down and Direction.DOWN not in plant.sides:
            plant.sides.add(Direction.DOWN)
            shared = (plant.left and Direction.DOWN in plant.left.sides) or \
                (plant.right and Direction.DOWN in plant.right.sides)
            
            if not shared:
                total_sides+=1

        #left
        if not plant.left and Direction.LEFT not in plant.sides:
            plant.sides.add(Direction.LEFT)
            shared = (plant.up and Direction.LEFT in plant.up.sides) or \
                (plant.down and Direction.LEFT in plant.down.sides)
        
            
            if not shared:
                total_sides+=1
            
        #right
        if not plant.right and Direction.RIGHT not in plant.sides:
            plant.sides.add(Direction.RIGHT)
            shared = (plant.up and Direction.RIGHT in plant.up.sides) or \
                (plant.down and Direction.RIGHT in plant.down.sides)
            
            
            if not shared:
                total_sides+=1


        q.extend([plant.up,plant.left,plant.down,plant.right])
        area+=1
    
    return area,total_sides


def part2():
    price = 0
    grid = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            plant = Plant(LINES[r][c],r,c,)
            row.append(plant)
        grid.append(row)
    

    for r in range(ROWS):
        for c in range(COLS):
            plant = grid[r][c]
            if same_plant(plant,Direction.LEFT,grid):
                left = grid[r][c-1]
                plant.left = left
                left.right = plant
            if same_plant(plant,Direction.RIGHT,grid):
                right = grid[r][c+1]
                plant.right = right
                right.left = plant
            if same_plant(plant,Direction.UP,grid):
                up = grid[r-1][c]
                plant.up = up
                up.down = plant
            if same_plant(plant,Direction.DOWN,grid):
                down = grid[r+1][c]
                plant.down = down
                down.up = plant
        
    
    seen = set()
    for r in range(ROWS):
        for c in range(COLS):
            if (r,c) not in seen:
                area, sides = get_sides(grid,r,c,seen)
                price+=area*sides
    
    return price


print(part1())
print(part2())

