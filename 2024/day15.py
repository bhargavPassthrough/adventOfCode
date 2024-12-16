
from collections import deque
DAY = 15
with open(f'2024/day{DAY}_input.txt') as f:
    LINES = f.read().splitlines()


DIRECTION_MAP = {
    '<' : (0,-1),
    '>' : (0,1),
    '^' : (-1,0),
    'v' : (1,0),
}




def move_robot(robot,grid,direction):
    direction = DIRECTION_MAP[direction]
    cur_row,cur_col = robot
    next_row,next_col = cur_row + direction[0], cur_col + direction[1]
    if grid[next_row][next_col] == '#':
        return robot
    elif grid[next_row][next_col] == '.':
        grid[next_row][next_col] = '@'
        grid[cur_row][cur_col] = '.'
        return (next_row,next_col)
    else:
        boxes_to_move = []
        r,c = next_row, next_col
        while grid[r][c] == 'O':
            nr,nc = r + direction[0],c+direction[1]
            if grid[nr][nc]!='#':
                boxes_to_move.append((r,c))
            else:
                boxes_to_move = []
            r,c = nr,nc
        moved = False
        for box in boxes_to_move:
            moved = True
            r,c = box
            nr,nc = r + direction[0],c+direction[1]
            grid[nr][nc] = 'O'
        if moved:
            grid[cur_row][cur_col] = '.'
            grid[next_row][next_col] = '@'
            return (next_row,next_col)
    
    return robot

def find_other_bracket(r,c,grid):
    if grid[r][c]=='[':
            return r,c+1
    elif grid[r][c] == ']':
        return r,c-1
    
def move_robot2(robot,grid,dir_char):
    direction = DIRECTION_MAP[dir_char]
    cur_row,cur_col = robot
    next_row,next_col = cur_row + direction[0], cur_col + direction[1]
    if grid[next_row][next_col] == '#':
        return robot
    elif grid[next_row][next_col] == '.':
        grid[next_row][next_col] = '@'
        grid[cur_row][cur_col] = '.'
        return (next_row,next_col)
    else:
        boxes_to_move = []
        r,c = next_row, next_col
        one_half = (r,c,grid[r][c])
        
        
        boxes_to_process = deque()
        boxes_to_process.append((one_half))
        next_box_pos = set()
        while boxes_to_process:
            one_half= boxes_to_process.popleft()
            r,c = one_half[0],one_half[1]
            if grid[r][c] == ']':
                other_half = (r,c-1,'[')
            else:
                other_half = (r,c+1,']')
            nr1,nc1 = one_half[0] + direction[0],one_half[1]+direction[1]
            nr2,nc2 = other_half[0] + direction[0],other_half[1]+direction[1]
            
            if grid[nr1][nc1] == '#' or grid[nr2][nc2] == '#':
                return robot
    
            boxes_to_move.extend([one_half,other_half])
            next_box_pos.add((nr1,nc1))
            next_box_pos.add((nr2,nc2))
            if grid[nr1][nc1] in '[]' and (nr1,nc1) not in [(one_half[0],one_half[1]),(other_half[0],other_half[1])]:
                boxes_to_process.append((nr1,nc1,grid[nr1][nc1]))

            if grid[nr2][nc2] in '[]' and (nr2,nc2) not in [(one_half[0],one_half[1]),(other_half[0],other_half[1])]:
                boxes_to_process.append((nr2,nc2,grid[nr2][nc2]))


        
    
        for br,bc,box in boxes_to_move:
            moved = True
            nr,nc = br + direction[0],bc+direction[1]
            grid[nr][nc] = box
            if (br,bc) not in next_box_pos:
                grid[br][bc]='.'
        
        
        if moved:
            grid[cur_row][cur_col] = '.'
            grid[next_row][next_col] = '@'
            return (next_row,next_col)
    
    return robot
    
    


def part1():
    i = 0
    grid = []
    robot = None
    while i < len(LINES):
        row = []
        line = LINES[i]
        
        if len(line) <2:
            break
        for col,char in enumerate(line):
            row.append(char)
            if char == '@':
                robot = (i,col)
        grid.append(row)
        i+=1
       

    ROWS = len(grid)
    COLS = len(grid[0])

    while i<len(LINES):
        line = LINES[i]
        i+=1
        for char in line:
            robot = move_robot(robot,grid,char)
    
    gps = 0
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == 'O':
                gps+= 100*row + col

    for row in range(ROWS):
        print(''.join(grid[row]))
    return gps


def part2():
    i = 0
    grid = []
    robot = None
    while i < len(LINES):
        row = []
        line = LINES[i]
        
        if len(line) <2:
            break
        for col,char in enumerate(line):
            if char == '#':
                row.extend(['#','#'])
            elif char == '@':
                row.extend(['@','.'])
                robot = (i,col*2)
            elif char == 'O':
                row.extend(['[',']'])
            else:
                row.extend(['.','.'])
        grid.append(row)
        i+=1
       

    ROWS = len(grid)
    COLS = len(grid[0])

    while i<len(LINES):
        line = LINES[i]
        i+=1
        for char in line:
            robot = move_robot2(robot,grid,char)
        
        
        
        
        
    
    gps = 0
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == '[':
                gps+= 100*row + col
    
    for row in range(ROWS):
            print(''.join(grid[row]))

    
    return gps




print(part1())
print(part2())