from enum import Enum
from dataclasses import dataclass
from typing import Callable
import re

DAY = 17
with open(f'2024/day{DAY}_input.txt') as f:
    LINES = f.read().splitlines()



class Register(Enum):
    A = 0
    B = 1
    C = 2


class RegisterValues:
    def __init__(self,a=0,b=0,c=0):
        self.values = {
            Register.A:a,
            Register.B:b,
            Register.C:c,
        }
    
    def get(self,register):
        return self.values[register]
    def set(self,register,value):
        self.values[register] = value
    
    def __str__(self):
        return f"A:{self.values[Register.A]} , B:{self.values[Register.B]}, C:{self.values[Register.C]}"

REGISTER_VALUES = RegisterValues()



class OperandType(Enum):
    LITERAL = 0
    COMBO = 1

    def get_value(self,operand):
        if self.name == 'LITERAL':
            return operand
        
        return self._get_combo_operand(operand)


    def _get_combo_operand(self,operand):
        match operand:
            case 4:
                return REGISTER_VALUES.get(Register.A)
            case 5:
                return REGISTER_VALUES.get(Register.B)
            case 6:
                return REGISTER_VALUES.get(Register.C)
            case _:
                return operand


@dataclass
class Opcode:
    code: int
    instruction: str
    operand_type: OperandType
    from_register: Register
    to_register: Register

    def adv(self,operand):
        numerator = REGISTER_VALUES.get(self.from_register)
        denominator = 1<<self.operand_type.get_value(operand)
        REGISTER_VALUES.set(self.to_register, numerator//denominator)
    
    def bxl(self,operand):
        a = REGISTER_VALUES.get(self.from_register)
        b = self.operand_type.get_value(operand)
        REGISTER_VALUES.set(self.to_register, a ^ b)
    
    def bst(self,operand):
        value = self.operand_type.get_value(operand) % 8
        REGISTER_VALUES.set(self.to_register, value)

    def jnz(self,operand):
        a = REGISTER_VALUES.get(self.from_register)
        b = self.operand_type.get_value(operand)
        return a != 0,b
    
    def bxc(self,operand):
        b = REGISTER_VALUES.get(Register.B)
        c = REGISTER_VALUES.get(Register.C)
        REGISTER_VALUES.set(self.to_register, b ^ c)
    
    def out(self,operand):
        value = self.operand_type.get_value(operand) % 8
        return value


OPERATIONS = [
    Opcode(
        code = 0,
        instruction = "adv",
        operand_type = OperandType.COMBO,
        from_register=Register.A,
        to_register=Register.A,
        ),
    Opcode(
        code = 1,
        instruction = "bxl",
        operand_type = OperandType.LITERAL,
        from_register=Register.B,
        to_register=Register.B,
        ),
    Opcode(
        code = 2,
        instruction = "bst",
        operand_type = OperandType.COMBO,
        from_register=Register.B,
        to_register=Register.B,
        ),
    Opcode(
        code = 3,
        instruction = "jnz",
        operand_type = OperandType.LITERAL,
        from_register=Register.A,
        to_register=Register.B,
        ),
    Opcode(
        code = 4,
        instruction = "bxc",
        operand_type = OperandType.LITERAL,
        from_register=Register.B,
        to_register=Register.B,
        ),
    Opcode(
        code = 5,
        instruction = "out",
        operand_type = OperandType.COMBO,
        from_register=Register.A,
        to_register=Register.B,
        ),
    Opcode(
        code = 6,
        instruction = "adv",
        operand_type = OperandType.COMBO,
        from_register=Register.A,
        to_register=Register.B,
        ),
    Opcode(
        code = 7,
        instruction = "adv",
        operand_type = OperandType.COMBO,
        from_register=Register.A,
        to_register=Register.C,
        )
]


def part1():
    a = int(re.search('\d+',LINES[0])[0])
    #a = int('4526445133267675',8)
    b = int(re.search('\d+',LINES[1])[0])
    c = int(re.search('\d+',LINES[2])[0])
    REGISTER_VALUES.set(Register.A,a)
    REGISTER_VALUES.set(Register.B,b)
    REGISTER_VALUES.set(Register.C,c)

    program = re.findall('\d+',LINES[4])
    program = list(map(int,program))
    
    output = []
    pointer = 0
    length = len(program)
    
    while pointer < length-1:
        opcode, operand = program[pointer],program[pointer+1]
        operation = OPERATIONS[opcode]
        instruction = getattr(operation,operation.instruction)
        #print(operation.instruction,operand,REGISTER_VALUES)
        match operation.instruction:
            case "jnz":
                jump,to = instruction(operand)
                if jump:
                    pointer = to
                else:
                    pointer+=2
            case "out":
                value = instruction(operand)
                output.append(value) 
                #print(value)
                pointer += 2

            case _:
                instruction(operand)
                pointer += 2
       
    return ','.join([str(x) for x in output])

print(part1())


def is_valid(octal,index,program):
    a = int(''.join(octal),8)
    i = 0
    while a>0 and i<index:
        b = a % 8
        b = b ^ 1
        c = a // 2**b
        b = b ^ 5
        b = b ^ c
        out = b % 8
        if out != int(program[i]):
            return False
        i+=1
        a = a//8
    
    return True

def valid_digit(octal,digit,index,program):
    number = int(''.join(octal[:index]+[str(digit)]),8)
    value = (digit ^ 4 ^ (number//2**(digit^1)) )% 8
    return value == int(program[::-1][index])

def backtrack(octal,index,program):
    if index == len(program):
        return is_valid(octal,index,program)

    for digit in range(8):
        if valid_digit(octal,digit,index,program): 
            octal[index] = str(digit)
            if backtrack(octal,index+1,program):
                return True

    return False


def part2():
    program = re.findall('\d+',LINES[4])
    program = ''.join(list(map(str,program)))
    octal = ['0']*len(program)
    if backtrack(octal,0,program):
        return int(''.join(octal),8)
        
   

print(part2())

