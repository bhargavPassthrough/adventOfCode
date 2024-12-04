DAY = 4
with open(f'2024/day{DAY}_input.txt') as f:
    lines = f.read().splitlines()

directions = [
        (1,0) #right
        ,(0,1), #down
        (-1,0), #left
        (0,-1), #up
        (1,1), #bottom right
        (-1,1), #bottom left
        (-1,-1), #top left
        (1,-1) #top right
        ]
word = 'XMAS'

def check_word(row,col,dx,dy):
    r,c = row,col
    for w in word[1:]:
        r += dy
        c += dx
        if r < 0 or r >= len(lines) or c < 0 or c >= len(lines[0]) or lines[r][c] != w:
            return False
    #print(f"Found {word} at {row},{col} to {r},{c} in direction {dx},{dy}")
    return True

def part1():
    count = 0
    for row in range(len(lines)):
        for col in range(len(lines[0])):
            if lines[row][col] == word[0]:
                for dx,dy in directions:
                    if check_word(row,col,dx,dy):
                        count+=1
                        
    return count



def check_word2(row,col,direction):
    char_map={'S':'M','M':'S'}
    char = lines[row][col]
    return lines[row+1][col-1*direction] =='A' and \
            lines[row+2][col-2*direction] == char_map[char]
    
   

def part2():
    count = 0
    for row in range(len(lines)-2):
        for col in range(len(lines[0])-2):
            if lines[row][col] in 'MS' and lines[row][col+2] in 'MS':
                if check_word2(row,col,-1) and check_word2(row,col+2,1):
                    count+=1
    return count
    
print(part1())
print(part2())