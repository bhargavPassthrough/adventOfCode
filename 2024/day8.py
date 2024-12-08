from collections import defaultdict
DAY = 8
with open(f'2024/day{DAY}_input.txt') as f:
    lines = f.read().splitlines()

ROWS = len(lines)
COLS = len(lines[0])

def within_range(pos):
    r,c = pos
    return r>=0 and r<ROWS and c>=0 and c<COLS

def get_antinode_positions(row,col,difference,should_loop=False):
    diff = [difference[0],difference[1]]
    positions = set()
    pos = (row+diff[0],col+diff[1])
    while within_range(pos):
        positions.add(pos)
        if not should_loop:
            return positions
        diff[0]+=difference[0]
        diff[1]+=difference[1]
        pos = (row+diff[0],col+diff[1])
    return positions

class Antenna:
    def __init__(self,row,col,symbol):
        self.row = row 
        self.col = col
        self.symbol = symbol
    def far_enough(self,other):
        return abs(self.row-other.row) and abs(self.col-other.col)
    def get_antinodes(self,other,should_loop=False):
        
        antinodes = set()
        diff1 = (self.row-other.row,self.col-other.col)
        antinodes.update(get_antinode_positions(self.row,self.col,diff1,should_loop))
        
        diff2 = [other.row-self.row,other.col-self.col]
        antinodes.update(get_antinode_positions(other.row,other.col,diff2,should_loop))
       

        return antinodes

    

    
    def __eq__(self,other):
        return (self.row,self.col,self.symbol) == \
            (other.row,other.col,other.symbol)
    def __hash__(self):
        return hash((self.row,self.col,self.symbol))
            
    



def get_antinodes(antenna,antennas,should_loop=False):
    antinodes = set()
    for other_antenna in antennas[antenna.symbol]:
        if antenna.far_enough(other_antenna):
            antinodes.update(antenna.get_antinodes(other_antenna,should_loop))
    return antinodes




def part1(should_loop=False):
    antennas = defaultdict(set)
    antinodes = set()
    for r in range(ROWS):
        for c in range(COLS):
            if lines[r][c].isalnum():
                antenna = Antenna(r,c,lines[r][c])
                antinodes.update(get_antinodes(antenna,antennas,should_loop))
                antennas[antenna.symbol].add(antenna)
                if should_loop:
                    antinodes.add((antenna.row,antenna.col))
    
    return len(antinodes)

def part2():
    return part1(should_loop=True)



print(part1())
print(part2())