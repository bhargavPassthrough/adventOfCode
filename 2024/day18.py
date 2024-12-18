from heapq import heappush,heappop
DAY = 18
with open(f'2024/day{DAY}_input.txt') as f:
    LINES = f.read().splitlines()

N = 70 + 1

DIRECTIONS = [
    (0,-1), #up
    (0,1), #down
    (-1,0), #left
    (1,0), #right
]

def within_range(x,y):
    return x>=0 and y>=0 and x<N and y<N

def min_steps(grid,dp):
    pq = []
    heappush(pq,(0,0,0))
    
    while pq:
        dist,x,y = heappop(pq)
        if dp[y][x] > dist:
            dp[y][x] = dist
            for dx,dy in DIRECTIONS:
                nx,ny = dx+x,dy+y
                if within_range(nx,ny) and grid[ny][nx] and dp[ny][nx] >= 1+dist:
                    heappush(pq,(dist+1,nx,ny))
    return dp[N-1][N-1]




def part1():
    grid = []
    dp = []
    for _ in range(N):
        grid.append([True]*N)
        dp.append([float('inf')]*N)
    
    for byte in range(1024):
        x,y = map(int,LINES[byte].split(','))
        grid[y][x] = False
    
    return min_steps(grid,dp)



def walls(grid):
    c = 0
    for row in grid:
        for col in row:
            if not col:
                c+=1
    return c

def part2():
    grid = []
    dp = []
    for _ in range(N):
        grid.append([True]*N)
        dp.append([float('inf')]*N)
    
    for byte in range(len(LINES)):
        x,y = map(int,LINES[byte].split(','))
        grid[y][x] = False
        dp = []
        for _ in range(N):
            dp.append([float('inf')]*N)
        steps = min_steps(grid,dp)
        if steps == float('inf'):
            return LINES[byte]
    
    

print(part1())

print(part2())