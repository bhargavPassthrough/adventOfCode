import re
from functools import reduce
DAY = 14
with open(f'2024/day{DAY}_input.txt') as f:
    LINES = f.read().splitlines()


HEIGHT = 103
WIDTH = 101

class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def __add__(self,vector):
        return Vector(self.x+vector.x , self.y+vector.y)
    
    def __mul__(self,scalar):
        return Vector(self.x*scalar,self.y*scalar)

    def __str__(self):
        return str((self.x,self.y))

    def __repr__(self):
        return str((self.x,self.y))

    def __mod__(self,vector):
        return Vector(self.x%vector.x, self.y%vector.y)
    
    def __eq__(self,vector):
        return self.x == vector.x and self.y == vector.y

    
class Robot:
    def __init__(self,pos,vel):
        self.pos = Vector(*pos)
        self.vel = Vector(*vel)
        self.initial_pos = Vector(*pos)

    
    def turn(self,seconds):
        self.pos = (self.vel*seconds + self.pos) % Vector(WIDTH,HEIGHT)
    
    def get_quadrant(self):
        mid_x = WIDTH // 2
        mid_y = HEIGHT // 2

        #Exactly in the middle, no quadrant
        if self.pos.y == mid_y or self.pos.x == mid_x:
            return 0
        
        #1st Quadrant
        if self.pos.x < mid_x and self.pos.y < mid_y:
            return 1
        
        #2nd Quadrant
        if self.pos.x > mid_x and self.pos.y < mid_y:
            return 2
        
        #3rd Quadrant
        if self.pos.x > mid_x and self.pos.y > mid_y:
            return 3
        
        #4th Quadrant
        if self.pos.x < mid_x and self.pos.y > mid_y:
            return 4

        return 0

ROBOTS = []
for line in LINES:
    numbers = list(map(int,re.findall('-*\d+',line)))
    robot = Robot(pos=numbers[:2],vel=numbers[2:])
    ROBOTS.append(robot)

def part1():
    seconds = 100
    robots_per_quadrant = [0,0,0,0,0]
    for robot in ROBOTS:
        robot.turn(seconds)
        robots_per_quadrant[robot.get_quadrant()]+=1
    
    return reduce(lambda a,b: a*b,robots_per_quadrant[1:],1)


def get_stem_length(grid):
    max_length = 0
    max_col = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] == '#':
                length = 0
                for ty in range(0,y):
                    if grid[ty][x] == '#':
                        length+=1
                    else:
                        break
                for ty in range(y,HEIGHT):
                    if grid[ty][x] == '#':
                        length+=1
                    else:
                        break
                if length > max_length:
                    max_length = length
                    max_col = x
    return max_length,max_col

                

def part2():
    for seconds in range(217,1000000):
        for robot in ROBOTS:
            robot.pos = robot.initial_pos
            robot.turn(seconds)

        grid = []
        for y in range(HEIGHT):
            grid.append(['.']*WIDTH)
        
        for robot in ROBOTS:
            grid[robot.pos.y][robot.pos.x] = '#'
        
        stem_length,stem_col = get_stem_length(grid)
        print(seconds,stem_length,stem_col)
        if stem_length > 10:
            print(seconds)
            for y in range(HEIGHT):
                print(''.join(grid[y]))
            break
            
        
        
        

    

print(part1())
print(part2())