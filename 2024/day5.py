from collections import defaultdict
DAY = 5
with open(f'2024/day{DAY}_input.txt') as f:
    lines = f.read().splitlines()

must_come_before=defaultdict(set)
for i in range(len(lines)):
    if lines[i] == '':
        break
    u,v = map(int,lines[i].split('|'))
    must_come_before[v].add(u)

i+=1
pages=[]
while i < len(lines):
    page = list(map(int,lines[i].split(',')))
    pages.append(page)
    i+=1




def valid(page):
    seen = set()
    for left in page[::-1]:
        for right in seen:
            if right in must_come_before[left]:
                
                return False
        seen.add(left)
    return True

def part1():
    total = 0
    for page in pages:
        if valid(page):
            middle=page[len(page)//2]
            total+=middle
    return total


def top_sort(incoming,outgoing,page_numbers):
    new_page = []
    pages_to_process = len(page_numbers)
    while pages_to_process:
        for num in page_numbers:
            if incoming[num] == 0:
                pages_to_process-=1
                for out in outgoing[num]:
                    incoming[out]-=1
                incoming[num]=-1
                new_page.append(num)
                page_numbers.remove(num)
                break
            
    return new_page

def correct_page(page):
    page_numbers = set(page)
    incoming={p:0 for p in page_numbers}
    outgoing=defaultdict(set)
    for num in page_numbers:
        for before_num in must_come_before[num]:
            if before_num in page_numbers:
                incoming[num]+=1
                outgoing[before_num].add(num)
    
    return top_sort(incoming,outgoing,page_numbers)






def part2():
    total = 0
    for page in pages:
        if not valid(page):
            page = correct_page(page)
            middle=page[len(page)//2]
            total+=middle
    return total
    
print(part1())
print(part2())

