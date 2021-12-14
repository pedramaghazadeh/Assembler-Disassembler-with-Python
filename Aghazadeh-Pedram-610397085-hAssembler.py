#Dictionaries for Assembler
IndexDict = {
    "eax":"000",
    "ecx":"001",
    "edx":"010",
    "ebx":"011",
    "illegal":"100",
    "ebp":"101",
    "esi":"110",
    "edi":"111",
    "rax":"000",
    "rcx":"001",
    "rdx":"010",
    "rbx":"011",
    "rbp":"101",
    "rsi":"110",
    "rdi":"111"
}
ScaleDict = {
    "1":"00",
    "2":"01",
    "4":"10",
    "8":"11"
}
BaseDict = {
    "eax":"000",
    "ecx":"001",
    "edx":"010",
    "ebx":"011",
    "esp":"100",
    "ebp":"101",
    "esi":"110",
    "edi":"111",
    "rax":"000",
    "rcx":"010",
    "rbx":"011",
    "rdx":"011",
    "rsp":"100",
    "rbp":"101",
    "rsi":"110",
    "rdi":"111"
}
RMDict = {
    "al":"000",
    "ax":"000",
    "eax":"000",
    "cl":"001",
    "cx":"001",
    "ecx":"001",
    "dl":"010",
    "dx":"010",
    "edx":"010",
    "bl":"011",
    "bx":"011",
    "ebx":"011",
    "ah":"100",
    "sp":"100",
    "esp":"100",
    "ch":"101",
    "bp":"101",
    "ebp":"101",
    "dh":"110",
    "si":"110",
    "esi":"110",
    "bh":"111",
    "di":"111",
    "edi":"111",
    "rax":"000",
    "rcx":"001",
    "rdx":"010",
    "rbx":"011",
    "rsp":"100",
    "rbp":"101",
    "rsi":"110",
    "rdi":"111"
}
RegDict = {
    "ax":"000",
    "cx":"001",
    "dx":"010",
    "bx":"011",
    "sp":"100",
    "bp":"101",
    "si":"110",
    "di":"111",

    "al":"000",
    "cl":"001",
    "dl":"010",
    "bl":"011",
    "ah":"100",
    "ch":"101",
    "dh":"110",
    "bh":"111",

    "eax":"000",
    "ecx":"001",
    "edx":"010",
    "ebx":"011",
    "esp":"100",
    "ebp":"101",
    "esi":"110",
    "edi":"111",

    "rax":"000",
    "rcx":"001",
    "rdx":"010",
    "rbx":"011",
    "rsp":"100",
    "rbp":"101",
    "rsi":"110",
    "rdi":"111"
}
Reg64Dict = {
    "rax":"0000",
    "eax":"0000",
    "ax":"0000",
    "al":"0000",
    "rcx":"0001",
    "ecx":"0001",
    "cx":"0001",
    "cl":"0001",
    "rdx":"0010",
    "edx":"0010",
    "dx":"0010",
    "dl":"0010",
    "rbx":"0011",
    "ebx":"0011",
    "bx":"0011",
    "bl":"0011",
    "rsp":"0100",
    "esp":"0100",
    "sp":"0100",
    "ah":"0100",
    "rbp":"0101",
    "ebp":"0101",
    "bp":"0101",
    "ch":"0101",
    "rsi":"0110",
    "esi":"0110",
    "si":"0110",
    "dh":"0110",
    "rdi":"0111",
    "edi":"0111",
    "di":"0111",
    "bh":"0111",
    "r8":"1000",
    "r8d":"1000",
    "r8w":"1000",
    "r8b":"1000",
    "r9":"1001",
    "r9d":"1001",
    "r9w":"1001",
    "r9b":"1001",
    "r10":"1010",
    "r10d":"1010",
    "r10w":"1010",
    "r10b":"1010",
    "r11":"1011",
    "r11d":"1011",
    "r11w":"1011",
    "r11b":"1011",
    "r12":"1100",
    "r12d":"1100",
    "r12w":"1100",
    "r12b":"1100",
    "r13":"1101",
    "r13d":"1101",
    "r13w":"1101",
    "r13b":"1101",
    "r14":"1110",
    "r14d":"1110",
    "r14w":"1110",
    "r14b":"1110",
    "r15":"1111",
    "r15d":"1111",
    "r15w":"1111",
    "r15b":"1111"
}
def operand_type(operand):
    if(len(operand) == 0):
        return "NONE"
    if(operand.find("PTR") != -1):
        return "Memory"
    for i in range(10):
        if(operand[0] == str(i)):
            return "Immediate"
    return "Register"

def register_type(operand):
    if(len(operand) == 0 or operand_type(operand) != "Register"):
        return 0
    if(operand[0] == "r"):
        if(operand[len(operand) - 1] == "d"):
            return 32
        if(operand[len(operand) - 1] == "w"):
            return 16
        if(operand[len(operand) - 1] == "b"):
            return 8
        return 64
    if(len(operand) == 2 and operand[len(operand) - 1] != "l" and operand[len(operand) - 1] != "h"):
        return 16
    if(len(operand) == 2):
        return 8
    return 32

def memory_type(operand):
    if(operand.find("PTR") == -1):
        return -1
    if(operand.find("BYTE") != -1):
        return 8
    if(operand.find("DWORD") != -1):
        return 32
    if(operand.find("QWORD") != -1):
        return 64
    if(operand.find("WORD") != -1):
        return 16
    return 0
    

def get_sib(operand):
    if(operand_type(operand) != "Memory"):
        return -1
    ind = operand.find("PTR")
    operand = operand[ind + 4 :]
    base = ""
    index = ""
    scale = ""
    displacement = ""
    if(operand.find("*") != -1):
        ind = operand.find("*") - 1
        while(operand[ind] != '[' and operand[ind] != '+'):
            index += operand[ind]
            ind -=1
        index = index[::-1]

        ind = 1 + operand.find("*")
        while(operand[ind] != ']' and operand[ind] != '+'):
            scale += operand[ind]
            ind += 1
        ind = operand.find("*")
        plus = operand.find("+")
        if(plus != -1):
            if(plus < ind):
                #base found
                base = operand[1:plus]
                plus = operand.find("+", plus + 1, len(operand) - 1)
                if(plus != -1):
                    displacement = operand[plus + 3 : len(operand) - 1]
            else:
                #no base but displacement
                displacement = operand[plus + 3 : len(operand) - 1]
    else:
        ind = operand.find("+")
        if(ind == -1):
            if(operand[2] != "x"):
                #only base
                base = operand[1 : len(operand) - 1]
            else:
                #only displacement
                displacement = operand[3 : len(operand) - 1]
        else:
            #base and displacement
            base = operand[1 : ind]
            if(operand[ind+1] == "0"):
                displacement = operand[ind + 3 : len(operand) - 1]
            else:
                scale = "1"
                ind += 1
                while(ind<len(operand) and operand[ind] != "]" and operand[ind] != "+"):
                    index += operand[ind]
                    ind += 1
                if(operand[ind] == "+"):
                    displacement = operand[ind + 3 : len(operand) - 1]
    if(len(displacement) > 2):
        displacement = ("0" * (8-len(displacement))) + displacement
    return (base, index, scale, displacement)

def make_reverse(str):
    ans = ""
    ind = len(str) - 2
    while(ind >= 0):
        ans += str[ind]
        ans += str[ind + 1]
        ind -= 2
    return ans


def make_hex(str):
    ind = 0
    ans = ""
    while(len(str) % 8 != 0):
        str = "0" + str
    while(ind < len(str)):
        tmp_str = str[ind: ind + 4]
        if(tmp_str == "0000"):
            ans += "0"
        if(tmp_str == "0001"):
            ans += "1"
        if(tmp_str == "0010"):
            ans += "2"
        if(tmp_str == "0011"):
            ans += "3"
        if(tmp_str == "0100"):
            ans += "4"
        if(tmp_str == "0101"):
            ans += "5"
        if(tmp_str == "0110"):
            ans += "6"
        if(tmp_str == "0111"):
            ans += "7"
        if(tmp_str == "1000"):
            ans += "8"
        if(tmp_str == "1001"):
            ans += "9"
        if(tmp_str == "1010"):
            ans += "a"
        if(tmp_str == "1011"):
            ans += "b"
        if(tmp_str == "1100"):
            ans += "c"
        if(tmp_str == "1101"):
            ans += "d"
        if(tmp_str == "1110"):
            ans += "e"
        if(tmp_str == "1111"):
            ans += "f"
        ind += 4
    return ans

def is_new(operand):
    if(operand_type(operand) == "Register" and operand.find("r") != -1):
        return True
    return False


def not_all_zero(displacement):
    for i in displacement:
        if(i != "0"):
            return True
    return False

def old_register(reg):
    if(len(reg) == 0):
        return False
    if(reg.find("r8") != -1):
        return False
    if(reg.find("r9") != -1):
        return False
    if(reg.find("r10") != -1):
        return False
    if(reg.find("r11") != -1):
        return False
    if(reg.find("r12") != -1):
        return False
    if(reg.find("r13") != -1):
        return False
    if(reg.find("r14") != -1):
        return False
    if(reg.find("r15") != -1):
        return False
    return True

inp = input()
i = 0
operation = ""
operand1 = ""
operand2 = ""
OpCode = ""
RegOp = ""
while(i<len(inp) and inp[i] != " " ):
    operation += inp[i]
    i += 1
while(i<len(inp) and inp[i] == " "):
    i += 1
while(i<len(inp) and inp[i] != ","):
    operand1 += inp[i]
    i +=1
if(i<len(inp) and inp[i] == ","):
    #2 operands
    i += 1
    while(inp[i] == " "):
        i += 1
    while(i < len(inp)):
        operand2 += inp[i]
        i += 1
if(operation == "stc"):
    answer = make_hex("11111001")
    print(answer)
    #for i in range(0, len(answer), 2):
    #    print(answer[i : i + 2], end = " ")
    exit()
if(operation == "clc"):
    answer = make_hex("11111000")
    print(answer)
    #for i in range(0, len(answer), 2):
    #    print(answer[i : i + 2], end = " ")
    exit()
if(operation == "std"):
    answer = make_hex("11111101")
    print(answer)
    #for i in range(0, len(answer), 2):
    #    print(answer[i : i + 2], end = " ")
    exit()
if(operation == "cld"):
    answer = make_hex("11111100")
    print(answer)
    #for i in range(0, len(answer), 2):
    #   print(answer[i : i + 2], end = " ")
    exit()
if(operation == "syscall"):
    answer = make_hex("0000111100000101")
    print(answer)
    #for i in range(0, len(answer), 2):
    #    print(answer[i : i + 2], end = " ")
    exit()

#print(operation, operand1, operand2)
#print(operand1, operand_type(operand1), memory_type(operand1), get_sib(operand1))
type1 = operand_type(operand1)
#print(operand2, operand_type(operand2), memory_type(operand2), get_sib(operand2))
type2 = operand_type(operand2)


Immediate = False
if(type2 == "Immediate"):
    Immediate = True
single_operand = True
if(len(operand2) != 0):
    single_operand = False

if(operation == "shl" or operation == "shr"):
    if(operand2 == "1"):
        single_operand = True
        operand2 = ""
        Immediate = False
    if(operand2.find("x") != -1 and int(operand2[2:]) == 1):
        single_operand = True
        operand2 = ""
        Immediate = False

if(operation == "xchg" and type1 == "Memory"):
    type1, type2 = type2, type1
    operand1, operand2 = operand2, operand1
if(operation == "xchg" and type1 == type2):
    operand1, operand2 = operand2, operand1
if(operation == "test" and type2 == "Memory"):
    type1, type2 = type2, type1
    operand1, operand2 = operand2, operand1
if(operation == "bsr" and type1 == type2):
    operand1, operand2 = operand2, operand1
if(operation == "bsf" and type1 == type2):
    operand1, operand2 = operand2, operand1

#Prefix
#Rex
#OpCode
#D
#W
#MOD
#Reg/Op
#R/M
#Scale, Index, Base
#Displacement
#Data
#D 
if(type2 == "Register"):
    D = "0"
else:
    D = "1"
if(single_operand):
    D = "1"
#D=0 then Reg = Operand1 and mod+R/M = Operand2
#D=1 then mod+R/M = Operand1 and Reg = Operand2
#W=0 only if Reg is 8bits in 32&64bit mod
reg1 = max(register_type(operand1), memory_type(operand1))
reg2 = max(register_type(operand2), memory_type(operand2))
#MOD
#print(reg1, reg2)
sib1 = get_sib(operand1)
sib2 = get_sib(operand2)
sib = False
#b,i,s,d
if(sib1 == -1):
    displc1 = 0
else:
    displc1 = len(sib1[3]) * 4
    
if(sib2 == -1):
    displc2 = 0
else:
    displc2 = len(sib2[3]) * 4
#print(displc1, displc2)
mod = "00"
if(displc1 == 8 or displc2 == 8):
    mod = "01"
if(displc1 == 16 or displc2 == 16):
    mod = "10"
if(displc1 == 32 or displc2 == 32):
    mod = "10"

if(type1 == "Register" and type2 == "Register" or (type1 == "Register" and single_operand == True)):
    mod = "11"
OpCode = ""
rm = ""
Sib = ""
displacement = ""
new_register = False
displacement_32 = False
DirectAddress = False
#speical operations
if(operation == "jrcxz"):
    answer = "11100011"
    answer = make_hex(answer)
    answer += operand1
    print(answer)
    #for i in range(0, len(answer), 2):
    #    print(answer[i : i + 2], end = " ")
    exit()
if(operation == "call"):
    if(type1 == "Immediate"):
        answer = make_hex("11101000")
        answer += make_reverse(operand1)
        answer += "00" * (8 - len(operand1))
        print(answer)
    #   for i in range(0, len(answer), 2):
    #      print(answer[i : i + 2], end = " ")
        exit()
if(operation == "ret"):
    if(len(operand1) != 0):
        answer = make_hex("11000010")
        operand1 = str(bin(int(operand1)))[2:]
        operand1 = ("0" * (16 - len(operand1))) + operand1
        operand1 = make_hex(operand1)
        operand1 = make_reverse(operand1)
    #    print(operand1)
        answer += operand1
        print(answer)
     #   for i in range(0, len(answer), 2):
      #      print(answer[i : i + 2], end = " ")
        exit()
    answer = make_hex("11000011")
    print(answer)
    #for i in range(0, len(answer), 2):
       # print(answer[i : i + 2], end = " ")
    exit()

if(is_new(operand1) or is_new(operand2)):
    new_register = True
if(type1 == "Memory" and (is_new(sib1[0]) or is_new(sib1[1]))):
    new_register = True
if(type2 == "Memory" and (is_new(sib2[0]) or is_new(sib2[1]))):
    new_register = True
#2operands with no swap
if(operation == "xor"):
    OpCode = "001100"
if(operation == "adc"):
    OpCode = "000100"
    if(type2 == "Immediate"):
        OpCode = "100000"
if(operation == "add"):
    OpCode = "000000"
    if(type2 == "Immediate"):
        OpCode = "100000"
        if(type1 == "Memory"):
            D = "0"
        else :
            D = "1"
if(operation == "and"):
    OpCode = "001000"
if(operation == "or"):
    OpCode = "000010"
if(operation == "xadd"):
    OpCode = "00001111110000"
if(operation == "mov"):
    OpCode = "100010"
    if(type2 == "Immediate"):
        OpCode = "1011"

if(operation == "sub"):
    OpCode = "001010"
if(operation == "bsf" or operation == "bsr"):
    OpCode = "00001111101111"
    
if(operation == "sbb"):
    OpCode = "000110"
if(operation == "cmp"):
    OpCode = "001110"
if(operation == "test"):
    OpCode = "100001"
if(operation == "imul"):
    OpCode = "00001111101011"
    if(single_operand == True):
        OpCode = "111101"
        D = "1"
        W = "1"
        RegOp = "101"
    else:
        D = "1"
        W = "1"
if(operation == "idiv"):
    if(single_operand == True):
        OpCode = "111101"
        D = "1"
        RegOp = "111"
#2operands with swap
if(operation == "xchg"):  #check these two
    OpCode = "100001"
    D = "1"
if(operation == "test"):
    OpCode = "100001"
    D = "0"
#1operand
if(operation == "inc"):
    OpCode = "111111"
    RegOp = "000"
if(operation == "dec"):
    OpCode = "111111"
    RegOp = "001" 
if(operation == "shl"):
    OpCode = "110000"
    D = "0"
    RegOp = "100"
    if(single_operand == True):
        OpCode = "110100"
    single_operand = True
if(operation == "shr"):
    OpCode = "110000"
    D = "0"
    RegOp = "101"
    if(single_operand == True):
        OpCode = "110100"
    single_operand = True
if(operation == "neg"):
    OpCode = "111101"
    RegOp = "011"
    D = "1"
if(operation == "not"):
    OpCode = "111101"
    RegOp = "010"
    D = "1"
if(operation == "jmp"):
    OpCode = "111111"
    W = "1"
    D = "1"
    RegOp = "100"
if(operation == "call"):
    OpCode = "111111"
    D = "1"
    W = "1"
    RegOp = "010"
no_displacement = False
displacement_8 = False

if(single_operand):    
    if(reg1 == 64 or new_register):
        #64 bit single operand
        if(operand1.find("DWORD") != -1 or register_type(operand1) != 64):
            rexW = "0"
        else:
            rexW = "1"
        rexR = "0"
        rexX = "0"
        rexB = "0"  
        if(operation == "jmp"):
            rexW = "0"
        if(type1 == "Register"):
            mod = "11"
            rexB = Reg64Dict[operand1][0]
            rm = Reg64Dict[operand1][1:]
            W = "1"
            if((operation == "shr" or operation == "shl") and register_type(operand1) == 8):
                W = "0"
        else:
            W = memory_type(operand1)
            if(W == 8):
                W = "0"
            else :
                W = "1"
            if(sib1[2] != "" or sib1[0] == "rbp" or sib1[0] == "ebp" or sib1[0] == "bp"):
                #scale then use sib
                sib = True
                #scale and no base
                if(sib1[0] == ""):
                    sib1 = ("ebp", sib1[1], sib1[2], sib1[3]) 
                    displacement_32 = True
                    mod = "00"
                    if(sib1[3] == ""):
                        sib1 = (sib1[0], sib1[1], sib1[2], "00")
                elif(sib1[0] == "rbp" or sib1[0] == "ebp" or sib1[0] == "bp"):
                    if(mod != "10"):
                        mod = "01"
                    displacement_32 = False
                    if(sib1[1] == "" and sib1[2] == ""):
                        sib = False
                    if(sib1[3] == ""):
                        sib1 = (sib1[0], sib1[1], sib1[2], "00")
            elif(sib1[0] == "" and sib1[1] == "" and sib1[2] == ""):
                #Direct Addressing
                Sib = "00100101"
                mod = "00"
                sib = True  
                DirectAddress = True
            elif(sib1[0] == "r12" or sib1[0] == "r12d" or
                 sib1[0] == "rsp" or sib1[0] == "esp"):
                #only r12 is present we need to use sib
                sib = True
                sib1 = (sib1[0], "esp", "1", sib1[3])
                if(len(sib1[3]) != 0):
                    displacement_32 = True
            if(sib):
                rm = "100"
            #direct memory access
            if(sib and DirectAddress == False):
                rexX = Reg64Dict[sib1[1]][0]
                rexB = Reg64Dict[sib1[0]][0]
                Sib = ScaleDict[sib1[2]] + Reg64Dict[sib1[1]][1:] + Reg64Dict[sib1[0]][1:]
            elif(DirectAddress == False):
                rexB = Reg64Dict[sib1[0]][0]
                rm = Reg64Dict[sib1[0]][1:]
            displacement = sib1[3]
        prefix = ""
        if(mod == "01" and displacement_32 == True):
            mod = "10"
        if(type1 == "Memory"):
            operand_size = memory_type(operand1)
            address_size = max(register_type(sib1[0]), register_type(sib1[1]))
            if(address_size == 32):
                prefix += "67"
            if(operand_size == 16):
                prefix += "66"
        else:
            operand_size = register_type(operand1)
            if(operand_size == 16):
                prefix += "66"
            
        answer = "0100" + rexW + rexR + rexX + rexB + OpCode + D + W + mod + RegOp + rm 
        #print(OpCode, D, W, mod, RegOp, rm, "\nOpcode,D,W,mod,RegOp,rm**")
        if(operation == "push"):
            if(type1 == "Register"):
                answer = "0100" + rexW + rexR + rexX + rexB + "01010" + rm
            else:
                answer = "0100" + rexW + rexR + rexX + rexB + "11111111" + mod + "110" + rm
        if(operation == "pop"):
            if(type1 == "Register"):
                answer = "0100" + rexW + rexR + rexX + rexB + "01011" + rm
            else:
                answer = "0100" + rexW + rexR + rexX + rexB + "10001111" + mod + "000" + rm
        if(sib):
            answer += Sib
            #print(Sib)
        #print(answer)
        ind = 0
        #while(ind < len(answer)):
        #    print(answer[ind : ind + 4], end=" ")
        #    ind += 4
        #print('\n')
        answer = make_hex(answer)
        displacement = make_reverse(displacement)
        if(displacement_32 == True):
            displacement += "0" * (8 - len(displacement))
        answer = prefix + answer + displacement
        if(Immediate):
            if(len(operand2) == 1 or operand2[1] != "x"):
                if(operand2[0] != "0"):
                    operand2 = make_hex(bin(int(operand2))[2:])
                else:
                    operand2 = make_hex(bin(int(operand2) - 8)[2:])
            else:
                operand2 = operand2[2:]
            if(len(operand2) % 2 != 0):
                operand2 = "0" + operand2
            answer += make_reverse(operand2)

        if((operation == "idiv" or operation == "dec" or operation == "inc" or operation == "imul") and old_register(operand1)):
            answer = answer[2:]
        print(answer)
        exit()
        #for i in range(0, len(answer), 2):
        #    print(answer[i : i + 2], end = " ")
    else:
        #32 bit single operand     
        if(type1 == "Register"):
            mod = "11"
            W = reg1
            rm = RMDict[operand1]
            if(W == 8):
                W = "0"
            else :
                W = "1"
        else:
            W = memory_type(operand1)
            if(W == 8):
                W = "0"
            else :
                W = "1"
            if(sib1[2] != "" or sib1[0] == "ebp" or sib1[0] == "bp"):
                #scale then use sib
                sib = True
                #scale and no base
                if(sib1[0] == ""):
                    sib1 = ("ebp", sib1[1], sib1[2], sib1[3]) 
                    displacement_32 = True
                    mod = "00"
                elif(sib1[0] == "ebp" or sib1[0] == "bp"):
                    if(mod != "10"): #always have displacement 
                        mod = "01"
                    displacement_32 = False
                    if(sib1[3] == ""):
                        sib1 = (sib1[0], sib1[1], sib1[2], "00")
            elif(sib1[0] == "" and sib1[1] == "" and sib1[2] == ""):
                #Direct Addressing
                Sib = "00100101"
                mod = "00"
                sib = True  
                DirectAddress = True
            if(sib):
                rm = "100"
            #direct memory access
            if(sib and DirectAddress == False):
                Sib = ScaleDict[sib1[2]] + IndexDict[sib1[1]] + BaseDict[sib1[0]]
            elif(DirectAddress == False):
                rm = RegDict[sib1[0]]
            displacement = sib1[3]
        prefix = ""
        if(type1 == "Memory"):
            operand_size = memory_type(operand1)
            address_size = max(register_type(sib1[0]), register_type(sib1[1]))
            if(address_size == 32):
                prefix += "67"
            if(operand_size == 16):
                prefix += "66"
        else:
            operand_size = register_type(operand1)
            if(operand_size == 16):
                prefix += "66"
        if(mod == "01"):
            mod = "10"
        answer = OpCode + D + W + mod + RegOp + rm 
        #print(OpCode, D, W, mod, RegOp, rm)
        if(operation == "push"):
            if(type1 == "Register"):
                answer = "01010" + rm
            else:
                answer = "11111111" + mod + "110" + rm
        if(operation == "pop"):
            if(type1 == "Register"):
                answer = "01011" + rm
            else:
                answer = "10001111" + mod + "000" + rm
                if(sib):
                    answer += sib
        if(sib):
            answer += Sib
         #   print(Sib)
        ind = 0
        #while(ind < len(answer)):
        ##    print(answer[ind : ind + 4], end=" ")
        #    ind += 4
        #print('\n')
        answer = make_hex(answer)
        displacement = make_reverse(displacement)
        if(len(displacement) != 0):
            displacement_32 = True
        if(displacement_32 == True):
            displacement += "0" * (8 - len(displacement))
        answer = prefix + answer + displacement
        if(Immediate):
            if(len(operand2) == 1 or operand2[1] != "x"):
                if(operand2[0] != "0"):
                    operand2 = make_hex(bin(int(operand2))[2:])
                else:
                    operand2 = make_hex(bin(int(operand2) - 8)[2:])
            else:
                operand2 = operand2[2:]
            if(len(operand2) % 2 != 0):
                operand2 = "0" + operand2
            answer += make_reverse(operand2)
        print(answer)
        ind = 0
        #for i in range(0, len(answer), 2):
        #    print(answer[i : i + 2], end = " ")


elif(reg1 == 64 or reg2 == 64 or new_register):
    #64bit mode
    #MOD
    #W
    #in 64 bit mode, only 32bit diplacement is supported when we have actual displacement
    #8 bit displacement is for when we dont' have actual displacement and bp registers are used
    if(mod == "01" and type1 == "Memory" and sib1[2] == "" and displc1 > 8):
        mod = "10"
    if(mod == "01" and type2 == "Memory" and sib2[2] == "" and displc2 > 8):
        mod = "10"
    if(reg1 == 64 or reg2 == 64):
        rexW = "1"
    else:
        rexW = "0"
    rexR = "1"
    rexX = "0"
    rexB = "1"
    if(D == "0"):
        W = reg2
    else:
        W = reg1
    if(W == 8):
        W = "0"
    else:
        W = "1"
    if(reg1 == 64 or reg2 == 64):
        rexW = "1"
    else:
        rexW = "0"
    #print(reg1, reg2)
    if(D == "0"):
        #operand 2 is register
        rexR = Reg64Dict[operand2][0]
        RegOp = Reg64Dict[operand2][1:]
        if(type1 == "Memory"):
            if(sib1[2] != "" or sib1[0] == "rbp" or sib1[0] == "ebp" or sib1[0] == "bp"):
                #scale then use sib
                sib = True
                #scale and no base
                if(sib1[0] == ""):
                    sib1 = ("ebp", sib1[1], sib1[2], sib1[3]) 
                    displacement_32 = True
                    mod = "00"
                elif(sib1[0] == "rbp" or sib1[0] == "ebp" or sib1[0] == "bp"):
                    if(mod != "10"):  #using 32 bit displacement if case of bp registers
                        mod = "01"
                    displacement_32 = False
                    if(sib1[1] == "" and sib1[2] == ""):
                        sib = False
                    if(sib1[3] == ""):
                        sib1 = (sib1[0], sib1[1], sib1[2], "00")
            elif(sib1[0] == "" and sib1[1] == "" and sib1[2] == ""):
                #Direct Addressing                     rex needs to be done
                displacement_32 = True
                rm = "100"
                sib = True
                Sib = "00100101"
                mod = "00"  
                DirectAddress = True
                rexX = "0"
                rexB = "0"
            elif(sib1[0] == "r12" or sib1[0] == "r12d" or
                 sib1[0] == "rsp" or sib1[0] == "esp"):
                #only r12 is present we need to use sib
                sib = True
                sib2 = (sib1[0], "esp", "1", sib1[3])
            if(sib):
                rm = "100"
            #direct memory access
            if(sib and DirectAddress == False):
                rexX = Reg64Dict[sib1[1]][0]
                rexB = Reg64Dict[sib1[0]][0]
                Sib = ScaleDict[sib1[2]] + Reg64Dict[sib1[1]][1:] + Reg64Dict[sib1[0]][1:]
            elif(DirectAddress == False):
                rexB = Reg64Dict[sib1[0]][0]
                rm = Reg64Dict[sib1[0]][1:]
            displacement = sib1[3]
        else:
            if(type1 == "Immediate"): #must check for immediate
                mod = "00"
                rm = "100"
                sib = True
                Sib = "00100101"
                displacement = sib1[3]
            else:
                rexB = Reg64Dict[operand1][0]
                rm = Reg64Dict[operand1][1:]
    else:
        rexR = Reg64Dict[operand1][0]
        RegOp = Reg64Dict[operand1][1:]
        if(type2 == "Memory"):
            if(sib2[2] != "" or sib2[0] == "rbp" or sib2[0] == "ebp" or sib2[0] == "bp"):
                sib = True
                if(sib2[0] == ""):
                    sib2 = ("ebp", sib2[1], sib2[2], sib2[3]) 
                    displacement_32 = True
                    mod = "00"
                elif(sib2[0] == "rbp" or sib2[0] == "ebp" or sib2[0] == "bp"):
                    if(mod != "10"): 
                        mod = "01"
                    displacement_32 = False
                    if(sib2[1] == "" and sib2[2] == ""):
                        sib = False
                    if(sib2[3] == ""):
                        sib2 = (sib2[0], sib2[1], sib2[2], "00")
            elif(sib2[0] == "" and sib2[1] == "" and sib2[2] == ""):
                #Direct Addressing
                rm = "100"
                sib = True
                Sib = "00100101"
                mod = "00"  
                DirectAddress = True
                displacement_32 = True
                rexX = "0"
                rexB = "0"
            elif(sib2[0] == "r12" or sib2[0] == "r12d" or
                 sib2[0] == "rsp" or sib2[0] == "esp"):
             #only r12 is present we need to use sib
                sib = True
                sib2 = (sib2[0], "esp", "1", sib2[3])
            if(sib):
                rm = "100"
            #direct memory access
            if(sib and DirectAddress == False):
                rexX = Reg64Dict[sib2[1]][0]
                rexB = Reg64Dict[sib2[0]][0]
                Sib = ScaleDict[sib2[2]] + Reg64Dict[sib2[1]][1:] + Reg64Dict[sib2[0]][1:]
            elif(DirectAddress == False):
                rexB = Reg64Dict[sib2[0]][0]
                rm = Reg64Dict[sib2[0]][1:]
            displacement = sib2[3]
        else:
            if(type2 == "Immediate"):
                if(operation == "adc"):
                    rm = RegOp
                    RegOp = "010"
                    mod = "11"
                    rexB = rexR
                    rexR = "1"
                if(operation == "add"):
                    rm = RegOp
                    RegOp = "000"
                    mod = "11"
                    rexB = rexR
                    rexR = "1"
                if(len(operand2) == 2 and (register_type(operand1) == 16 or register_type(operand1) == 32)):
                    s = "1"
                else:
                    s = "0"
                if(operation == "add"):
                    answer = make_hex(OpCode + D + W + mod + RegOp + rm) 
                
                if(operation == "adc"):
                    answer = make_hex(OpCode + s + W + mod + RegOp + rm) 
        
                if(operation == "mov"):
                    answer = make_hex(OpCode + W + RegOp)
                operand2 = operand2[2:]
                operand2 = make_reverse(operand2)
                while(len(operand2) * 4 != max(register_type(operand1), 16)):
                    operand2 = "0" + operand2
                answer += operand2
                print(answer)
                #for i in range(0, len(answer), 2):
                #    print(answer[i : i + 2], end = " ")
                exit()
            else:
                rexB = Reg64Dict[operand2][0]
                rm = Reg64Dict[operand2][1:]
    prefix = ""
    if(type1 == "Memory"):
        operand_size = register_type(operand2)
        address_size = max(register_type(sib1[0]), register_type(sib1[1]))
        if(address_size == 32):
            prefix += "67"
        if(operand_size == 16):
            prefix += "66"
    elif(type2 == "Memory"):
        operand_size = register_type(operand1)
        address_size = max(register_type(sib2[0]), register_type(sib2[1]))
        if(address_size == 32):
            prefix += "67"
        if(operand_size == 16):
            prefix += "66"
    else:
        operand_size = register_type(operand1)
        if(operand_size == 16):
            prefix += "66"
    if(operation == "bsf"):
        W = "0"
        D = "0"
    if(operation == "bsr"):
        W = "1"
        D = "0"

    answer = "0100" + rexW + rexR + rexX + rexB + OpCode + D + W + mod + RegOp + rm 
    #print(OpCode, D, W, mod, RegOp, rm)
    if(sib):
        answer += Sib
      #  print(Sib)
    #print(answer)
    #print(displacement)
    ind = 0
    #while(ind < len(answer)):
     #   print(answer[ind : ind + 4], end=" ")
      #  ind += 4
    #print('\n')
    answer = make_hex(answer)
    if(old_register(operand1) and old_register(operand2) and operand_size <= 32):
        answer = answer[2:]
    displacement = make_reverse(displacement)
    if(displacement_32 == True):
        displacement += "0" * (8 - len(displacement))
    answer = prefix + answer + displacement
    print(answer)
    ind = 0
    #for i in range(0, len(answer), 2):
     #   print(answer[i : i + 2], end = " ")
else:
    #32 bit
    #MOD
    #W
    if(D == "0"):
        W = reg2
    else:
        W = reg1
    if(W == 8):
        W = "0"
    else:
        W = "1"
    if(D == "0"):
        #operand 2 is register
        RegOp = RegDict[operand2]
        if(type1 == "Memory"):
            if(sib1[2] != "" or sib1[0] == "ebp" or sib1[0] == "bp"):
                #scale then use sib
                sib = True
                #scale and no base
                if(sib1[0] == ""):
                    sib1 = ("ebp", sib1[1], sib1[2], sib1[3]) 
                    displacement_32 = True
                    if(len(sib1[3]) == 0):
                        sib1 = ("ebp", sib1[1], sib1[2], "00") 
                    mod = "00"
                elif(sib1[0] == "ebp" or sib1[0] == "bp"):
                    if(mod != "10"):
                        mod = "01"
                        displacement_32 = False
                        displacement_8 = True
                    else:
                        displacement_32 = True
                    if(sib1[1] == "" and sib1[2] == ""):
                        sib = False
                    if(sib1[3] == ""):
                        sib1 = (sib1[0], sib1[1], sib1[2], "00")
            elif(sib1[0] == "" and sib1[1] == "" and sib1[2] == ""):
                #Direct Addressing
                rm = "100"
                sib = True
                Sib = "00100101"
                mod = "00"  
                DirectAddress = True
            if(sib):
                rm = "100"
            #direct memory access
            if(sib and DirectAddress == False):
                Sib = ScaleDict[sib1[2]] + IndexDict[sib1[1]] + BaseDict[sib1[0]]
            elif(DirectAddress == False):
                rm = RMDict[sib1[[0]]]
            displacement = sib1[3]
            if(sib1[3] == "" and sib1[0] != ""):
                no_displacement = True
        else:
            if(type1 == "Immediate"): #must check for immediate(never happens)
                mod = "00"
                rm = "100"
                sib = True
                Sib = "00100101"
                displacement = sib1[3]
            else:
                rm = RMDict[operand1]
    else:
        RegOp = RegDict[operand1]
        if(type2 == "Memory"):
            if(sib2[2] != "" or sib2[0] == "ebp" or sib2[0] == "bp"):
                sib = True
                if(sib2[0] == ""):
                    sib2 = ("ebp", sib2[1], sib2[2], sib2[3]) 
                    displacement_32 = True
                    if(len(sib2[3]) == 0):
                        sib2 = ("ebp", sib2[1], sib2[2], "00")
                    mod = "00"
                elif(sib2[0] == "ebp" or sib2[0] == "bp"):
                    if(mod != "10"): 
                        mod = "01"
                        displacement_8 = True
                        displacement_32 = False
                    else:
                        displacement_32 = True
                    if(sib2[1] == "" and sib2[2] == ""):
                        sib = False
                    if(sib2[3] == ""):
                        sib2 = (sib2[0], sib2[1], sib2[2], "00")
            elif(sib2[0] == "" and sib2[1] == "" and sib2[2] == ""):
                #Direct Addressing
                rm = "100"
                sib = True
                Sib = "00100101"
                mod = "00"  
                DirectAddress = True
            if(sib):
                rm = "100"
            #direct memory access
            if(sib and DirectAddress == False):
                Sib = ScaleDict[sib2[2]] + IndexDict[sib2[1]] + BaseDict[sib2[0]]
            elif(DirectAddress == False):
                rm = RMDict[sib2[0]]
            displacement = sib2[3]
            if(sib2[3] == "" and sib2[0] != ""):
                no_displacement = True
        else:
            if(type2 == "Immediate"):
                if(operation == "adc"):
                    rm = "010"
                    mod = "11"
                if(operation == "add"):
                    rm = RegOp
                    RegOp = "000"
                    mod = "11"
                if(len(operand2) == 2 and (register_type(operand1) == 16 or register_type(operand1) == 32)):
                    s = "1"
                else:
                    s = "0"
                if(operation == "add"):
                    answer = make_hex(OpCode + D + W + mod + RegOp + rm) 
                
                if(operation == "adc"):
                    answer = make_hex(OpCode + s + W + mod + RegOp + rm) 
        
                if(operation == "mov"):
                    answer = make_hex(OpCode + W + RegOp)
                operand2 = operand2[2:]
                operand2 = make_reverse(operand2)
                while(len(operand2) * 4 != max(register_type(operand1), 16)):
                    operand2 = "0" + operand2
                answer += operand2
                prefix = ""
                operand_size = register_type(operand1)
                if(operand_size == 16):
                    prefix += "66"
                answer = prefix + answer
                print(answer)
                #for i in range(0, len(answer), 2):
                 #   print(answer[i : i + 2], end = " ")
                exit()
            else:
                rm = RMDict[operand2]
    prefix = ""
    if(type1 == "Memory"):
        operand_size = register_type(operand2)
        address_size = max(register_type(sib1[0]), register_type(sib1[1]))
        if(address_size == 32):
            prefix += "67"
        if(operand_size == 16):
            prefix += "66"
    elif(type2 == "Memory"):
        operand_size = register_type(operand1)
        address_size = max(register_type(sib2[0]), register_type(sib2[1]))
        if(address_size == 32 ):
            prefix += "67"
        if(operand_size == 16):
            prefix += "66"
    else:
        operand_size = register_type(operand1)
        if(operand_size == 16):
            prefix += "66"
    if(operation == "bsf"):
        W = "0"
        D = "0"
    if(operation == "bsr"):
        W = "1"
        D = "0"

    answer = OpCode + D + W + mod + RegOp + rm 
    #print(OpCode, D, W, mod, RegOp, rm)
    if(sib):
        answer += Sib
     #   print(Sib)
    #print(answer)
    ind = 0
    #while(ind < len(answer)):
     #   print(answer[ind : ind + 4], end=" ")
      #  ind += 4
    #print('\n')
    answer = make_hex(answer)
    displacement = make_reverse(displacement)
    if(displacement_8 == True):
        displacement += "0" * (2 - len(displacement))
    if(displacement_32 == True):
        displacement += "0" * (8 - len(displacement))
    if(displacement == -1):
        displacement = ""
    answer = prefix + answer
    if(no_displacement == False):
        answer += displacement
    print(answer)
    #for i in range(0, len(answer), 2):
     #   print(answer[i : i + 2], end = " ")
    #Data

#1operand



