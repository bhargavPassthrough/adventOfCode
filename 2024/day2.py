DAY = 2
with open(f'day{DAY}_input.txt') as f:
    data = f.read().splitlines()

def is_within_range(a,b):
    return abs(a-b) <= 3 and a != b


def is_safe(row):
    n = len(row)
    if n == 1:
        return True
    incr = row[1] > row[0]
    for i in range(1,n):
        if (row[i] > row[i-1]) != incr:
            return False
        if not is_within_range(row[i],row[i-1]):
            return False
    return True



def is_safe2(row):
    n = len(row)
    for i in range(n):
        if is_safe(row[:i]+row[i+1:]):
            return True
    return False
    

#Part 2
safe = 0
for row in data:
    print(row, len(list(map(int,row.split()))))
    safe+=is_safe2(list(map(int,row.split())))
print("# of safe rows:", safe)

