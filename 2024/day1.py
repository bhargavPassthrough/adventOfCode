from collections import Counter

DAY = 1
with open(f'day{DAY}_input.txt') as f:
    ids = f.read().splitlines()

#Part 1
a=[]
b=[]
for line in ids:
    one, two = line.split()
    a.append(int(one))
    b.append(int(two))


distance = 0
for one,two in zip(sorted(a),sorted(b)):
    distance+=abs(one-two)


print(distance)


#Part 2
score = 0
freq = Counter(b)
for number in a:
    score+=number*freq.get(number,0)

print(score)
