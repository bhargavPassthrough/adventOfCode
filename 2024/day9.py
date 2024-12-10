DAY = 9
with open(f'2024/day{DAY}_input.txt') as f:
    LINE = f.read()


def get_sum_of_range(a,b):
    return b*(b+1)//2 - a*(a-1)//2

class Node:
    def __init__(self,size,id,is_free=False):
        self.size = int(size)
        self.is_free = is_free
        self.next = None
        self.prev = None
        self.id = id
    
    def __str__(self):
        if self.is_free:
            return self.size*'.'

        return str(self.id)*self.size

class DLL:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
    
    def __str__(self):
        temp = self.head
        string = ''
        while temp:
            string += str(temp)
            temp = temp.next
        return string
    
    def insert(self,node):
        if self.head == None:
            self.head = node
            self.tail = node
            self.head.next = self.tail
            self.tail.prev = self.head
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        self.length += 1

    def insert_left(self,node_to_insert,existing_node):
        if existing_node == self.head:
            self.head = node_to_insert
            self.head.next = existing_node
        else:
            existing_node.prev.next = node_to_insert
        
        node_to_insert.next = existing_node
        existing_node.prev = node_to_insert
    
  

    def make_list(self,disk_map):
       for i,size in enumerate(disk_map):
           is_free = i%2 == 1
           node = Node(size,i//2,is_free)
           self.insert(node)
    
    
    def fill_free_space1(self):
        if not self.head:
            return

        left = self.head
        right = self.tail
        while left and right and left.id<right.id:
            if left and (not left.is_free or left.size==0):
                left = left.next
                continue
            if right and (right.is_free or right.size==0):
                right = right.prev
                continue
           
            if left.size == right.size:
                right.is_free = True
                left.is_free = False
                left.id = right.id
                left = left.next
                right = right.prev
            

            elif left.size > right.size:
                self.insert_left(Node(right.size,right.id,False),left)
                left.size -= right.size
                right.is_free = True
                right = right.prev
            
            else:
                right.size-=left.size
                left.id = right.id
                left.is_free = False
                left = left.next
               


    


    
    def fill_free_space2(self):
        if not self.head:
            return
        
        left = self.head
        while left and left.id < self.length:
            if left and (not left.is_free or left.size==0):
                left = left.next
                continue
            
            right = self.tail
            while right and right.id > left.id:
                if right and (right.is_free or right.size==0):
                    right = right.prev
                    continue
                
                if left.size == right.size:
                    right.is_free = True
                    left.is_free = False
                    left.id = right.id
                    left = left.next
                    break
                
                elif left.size > right.size:
                    self.insert_left(Node(right.size,right.id,False),left)
                    left.size -= right.size
                    right.is_free = True
                
                else:
                    right = right.prev
            
            if right.id <= left.id: #This free space is not fillable
                left = left.next

            
    
    def checksum(self):
        total = 0
        temp = self.head
        position_sum = 0
        current_pos = 0
        prev_pos = 0
        while temp:
            current_pos += temp.size
            if not temp.is_free:
                position_sum = get_sum_of_range(prev_pos,current_pos-1)
                total += position_sum*(temp.id)
            prev_pos = current_pos
            
            temp = temp.next
        return total
    



def part1():
    dll = DLL()
    dll.make_list(LINE)
    dll.fill_free_space1()
    return dll.checksum()

def part2():
    dll = DLL()
    dll.make_list(LINE)
    dll.fill_free_space2()
    return dll.checksum()



print(part1())
print(part2())
