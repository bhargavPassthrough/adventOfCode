from enum import Enum
DAY = 6
with open(f'2024/day{DAY}_input.txt') as f:
    lines = f.read().splitlines()

class Direction(Enum):
    UP = (-1,0)
    RIGHT = (0,1)
    DOWN = (1,0)
    LEFT = (0,-1)



GRID = []
ROWS = len(lines)
COLS = len(lines[0])
NEXT_DIRECTION = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP
}

class Position:
    def __init__(self,r,c):
        self.row = r
        self.col = c
        self.is_wall = False
        self.is_start = False
    
    def move(self,direction:Direction):
        row = self.row + direction.value[0]
        col = self.col + direction.value[1]
        if row >= ROWS or col >= COLS or row<0 or col<0:
            return False
        return GRID[row][col]
    
    def move_back(self,direction:Direction):
        row = self.row - direction.value[0]
        col = self.col - direction.value[1]
        if row >= ROWS or col >= COLS or row<0 or col<0:
            return False
        return GRID[row][col]
    
    def __str__(self):
        return f'({self.row},{self.col})'
    def __repr__(self):
        return f'({self.row},{self.col})'
    
    def __eq__(self,other):
        return self.row == other.row and self.col == other.col
    def __hash__(self):
        return hash((self.row,self.col))

START_POS = (0,0)
for r in range(ROWS):
    row = []
    for c in range(COLS):
        pos = Position(r,c)
        if lines[r][c] == '#':
            pos.is_wall = True
        elif lines[r][c] == '^':
            pos.is_start = True
            START_POS = pos
        row.append(pos)
    GRID.append(row)



def part1():
    current_pos = START_POS
    current_direction = Direction.UP
    covered_cells = set()
    walls = set()


    while current_pos and current_pos.row >=0 and current_pos.row < ROWS and current_pos.col >=0 and current_pos.col < COLS:
        next_pos = current_pos.move(current_direction)
        if not next_pos: # reached beyond the grid
            break
        if next_pos.is_wall:
            if (next_pos,current_direction) in walls:
                print('Loop detected at',next_pos,current_direction)
                return False
            walls.add((next_pos,current_direction))
            next_pos = next_pos.move_back(current_direction)
            current_direction = NEXT_DIRECTION[current_direction]
            continue
        else:
            covered_cells.add(next_pos)
        
     

       
        current_pos = next_pos

    return covered_cells


def part2(candidates):
    count = 0
    for candidate in candidates:
        if candidate.is_start:
            continue
        candidate.is_wall = True
        if not part1():
            print(candidate)
            count += 1
        candidate.is_wall = False
    
    return count
   



covered_cells  = part1()
print(len(covered_cells))
print(part2(covered_cells))


