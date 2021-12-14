ScaleDict = {
    "00":"1",
    "01":"2",
    "10":"4",
    "11":"8"
}
IndexDict = {
    "000":("eax","rax"),
    "001":("ecx","rcx"),
    "010":("edx","rdx"),
    "011":("ebx","rbx"),
    "100":("illegal","illegal"),
    "101":("ebp","rbp"),
    "110":("esi","rsi"),
    "111":("edi","rdi")
}
BaseDict = {
    "000":("eax","rax"),
    "001":("ecx","rcx"),
    "010":("edx","rdx"),
    "011":("ebx","rbx"),
    "100":("esp","rsp"),
    "101":("ebp","rbp"),
    "110":("esi","rsi"),
    "111":("edi","rdi")
}
RegDict = {
    "000":("al","ax","eax","rax"),
    "001":("cl","cx","ecx","rcx"),
    "010":("dl","dx","edx","rdx"),
    "011":("bl","bx","ebx","rbx"),
    "100":("ah","sp","esp","rsp"),
    "101":("ch","bp","ebp","rbp"),
    "110":("dh","si","esi","rsi"),
    "111":("bh","di","edi","rdi")
}
Reg64Dict = {
    "0000":("al","ax","eax","rax"),
    "0001":("cl","cx","ecx","rcx"),
    "0010":("dl","dx","edx","rdx"),
    "0011":("bl","bx","ebx","rbx"),
    "0100":("ah","sp","esp","rsp"),
    "0101":("ch","bp","ebp","rbp"),
    "0110":("dh","si","esi","rsi"),
    "0111":("bh","di","edi","rdi"),

    "1000":("r8b","r8w","r8d","r8"),
    "1001":("r9b","r9w","r9d","r9"),
    "1010":("r10b","r10w","r10d","r10"),
    "1011":("r11b","r11w","r11d","r11"),
    "1100":("r12b","r12w","r12d","r12"),
    "1101":("r13b","r13w","r13d","r13"),
    "1110":("r14b","r14w","r14d","r14"),
    "1111":("r15b","r15w","r15d","r15")
}

def make_binary(hexcode):
    ans = ""
    for i in hexcode:
        ans += convert(i)
    return ans
def convert(hexcode):
    if(hexcode == "0"):
        return "0000"
    if(hexcode == "1"):
        return "0001"
    if(hexcode == "2"):
        return "0010"
    if(hexcode == "3"):
        return "0011"
    if(hexcode == "4"):
        return "0100"
    if(hexcode == "5"):
        return "0101"
    if(hexcode == "6"):
        return "0110"
    if(hexcode == "7"):
        return "0111"
    if(hexcode == "8"):
        return "1000"
    if(hexcode == "9"):
        return "1001"
    if(hexcode == "a"):
        return "1010"
    if(hexcode == "b"):
        return "1011"
    if(hexcode == "c"):
        return "1100"
    if(hexcode == "d"):
        return "1101"
    if(hexcode == "e"):
        return "1110"
    if(hexcode == "f"):
        return "1111"
def make_reverse(displacement): 
    ans = ""
    for i in range(0, len(displacement), 2):
        ans = displacement[i : i + 2] + ans
    while(len(ans) > 1 and ans[0] == "0"):
        ans = ans[1:]
    return ans

def not_zero(displacement):
    if(len(displacement) == 0):
        return False
    for i in displacement:
        if(i!= "0" and i != "x"):
            return True
    if(len(displacement) == 10):
        return True
    return False
inp = input()
inpt = make_binary(inp)
if(inpt == "11111001"):
    print("stc")
    exit()
if(inpt == "11111000"):
    print("clc")
    exit()
if(inpt == "11111101"):
    print("std")
    exit()
if(inpt == "11111100"):
    print("cld")
    exit()
if(inpt == "0000111100000101"):
    print("syscall")
    exit()
if(inpt == "11000011"):
    print("ret")
    exit()
#prefix check
prefix66 = False
prefix67 = False
if(inp[:2] == "67"):
    prefix67 = True
    inp = inp[2:]
if(inp[:2] == "66"):
    prefix66 = True
    inp = inp[2:]
Rex = ""
operation = ""
operand1 = ""
operand2 = ""
mod = ""
reg = ""
rm = ""
sib = ""
scale = ""
index = ""
base = ""
ImmediateData = False
Sib = False
single_operand = False
displacement = ""

#2 operands
if(inp[0] == "4"):
    #64 bit or new registers
    Rex = make_binary(inp[1])
    inp = inp[2:]
    RexW = Rex[0]
    RexR = Rex[1]
    RexX = Rex[2]
    RexB = Rex[3]

    OpCode = make_binary(inp[:2])
    inp = inp[2:]
    if(OpCode == "00001111"):
        #OpCode length is 16 instead of 8
        OpCode += make_binary(inp[:2])
        inp = inp[2:]
    D = OpCode[-2]
    W = OpCode[-1]
    OpCode = OpCode[:-2]
    #push and pop are special :((((((
    if(OpCode == "010100" or OpCode == "010101"):
        reg = RexB + OpCode[-1] + D + W
        print("push", Reg64Dict[reg][3])
        exit()
    if(OpCode == "010110" or OpCode == "010111"):
        reg = RexB + OpCode[-1] + D + W
        print("pop", Reg64Dict[reg][3])
        exit()
    if(OpCode == "00001111101111"):
        if(W == "0"):
            operation = "bsf"
        else:
            operation = "bsr"
    mod = make_binary(inp[:2])
    inp = inp[2:]
    reg = mod[2:5]
    rm  = mod[5:]
    mod = mod[:2]
    if(OpCode == "111111" and D == "1" and (reg == "000" or reg == "001")):
        single_operand = True
    if(OpCode == "110100" and D == "0" and (reg == "100" or reg == "101")):
        single_operand = True
    if(OpCode == "111101" and D == "1" and (reg == "010" or reg == "011")):
        single_operand = True
    if(OpCode == "111111" and D == "1" and W == "1" and reg == "100" and RexR == "0"):
        operation = "jmp"
        single_operand = True
    if(OpCode == "111111" and D == "1" and W == "1" and reg == "010" and ((RexX == "0" and RexB == "0") or RexR == "0")):
        operation = "call"
        single_operand = True
    if(OpCode == "111111" and D == "1" and W == "1" and reg == "110"):
        operation = "push"
        single_operand = True
    if(OpCode == "100011" and D == "1" and W == "1" and reg == "000"):
        operation = "pop"
        single_operand = True
    #shl and shr register by immediate
    if(OpCode == "110000" and D == "0" and reg == "100"):
        single_operand = True
        ImmediateData = True
    if(OpCode == "110000" and D == "0" and reg == "101"):
        single_operand = True
        ImmediateData = True
    if(OpCode == "111101" and D == "1" and reg == "101"):
        operation = "imul"
        single_operand = True
    if(OpCode == "111101" and D == "1" and reg == "111"):
        operation = "idiv"
        single_operand = True
    if(OpCode == "100000" and reg == "101"):
        operation = "sub"
        single_operand = True
        ImmediateData = True
    if(single_operand == True):
        #inc or dec
        if(mod == "11"):
            #register 64bit or new
            RexB += rm
            operand1 = Reg64Dict[RexB]
            if(operation == "jmp" or operation == "call" or operation == "push" or operation == "pop"):
                operand1 = operand1[3]
            elif(W == "0"):
                operand1 = operand1[0]
            elif(RexW == "1"):
                operand1 = operand1[3]
            elif(prefix66):
                operand1 = operand1[1]
            else:
                operand1 = operand1[2]
            if(ImmediateData == True):
                operand2 = "0x" + make_reverse(inp)
        else:
            if(rm == "100" and inp != ""):
                #sib
                sib = make_binary(inp[:2])
                inp = inp[2:]
                scale = sib[:2]
                index = sib[2:5]
                base  = sib[5:]

                RexX += index
                RexB += base
                
                if(ImmediateData == True):
                    displacement = "0x" + make_reverse(inp[:-2])
                    inp = inp[-2:]
                else:
                    displacement = "0x" + make_reverse(inp)
                #print(displacement)
                if(scale == "00" and RexX == "0100" and RexB == "0101"):
                    #direct addressing
                    operand2 = displacement
                else:
                    if(prefix67):
                        #32bit address
                        operand2 = Reg64Dict[RexB][2] + "+" + Reg64Dict[RexX][2] + "*" + ScaleDict[scale]
                        if(mod == "00" and Reg64Dict[RexB][2] == "ebp"): #no base
                            operand2 = Reg64Dict[RexX][2] + "*" + ScaleDict[scale]
                    else:
                        #64bit address
                        operand2 = Reg64Dict[RexB][3] + "+" + Reg64Dict[RexX][3] + "*" + ScaleDict[scale]
                        if(mod == "00" and Reg64Dict[RexB][3] == "rbp"):
                            operand2 = Reg64Dict[RexX][3] + "*" + ScaleDict[scale] #no base
                    if(mod != "00" or not_zero(displacement)):
                        if(not_zero(displacement)):
                            operand2 += "+" + displacement
                operand2 = "[" + operand2 + "]"
                if(operation == "jmp" or operation == "call" or operation == "push" or operation == "pop"):
                    operand2 = "QWORD PTR " + operand2
                elif(RexW == "1"):
                    operand2 = "QWORD PTR " + operand2
                elif(W == "0"):
                    operand2 = "BYTE PTR " + operand2
                elif(prefix66):
                    operand2 = "WORD PTR " + operand2
                else:
                    operand2 = "DWORD PTR " + operand2
                operand1 = operand2
            else:
                RexB += rm
                operand1 = Reg64Dict[RexB]
                if(prefix67 == True):
                    operand1 = operand1[2]
                else:
                    operand1 = operand1[3]
                if(operation == "jmp" or operation == "call" or operation == "push" or operation == "pop"):
                    operand1 = "QWORD PTR [" + operand1 + "]"
                elif(W == "0"):
                    operand1 = "BYTE PTR [" + operand1 + "]"
                elif(RexW == "1"):
                    operand1 = "QWORD PTR [" + operand1 + "]"
                elif(prefix66):
                    operand1 = "WORD PTR [" + operand1 + "]"
                else:
                    operand1 = "DWORD PTR [" + operand1 + "]"
        
        if(ImmediateData == True):
                operand2 = "0x" + make_reverse(inp)
    elif(rm == "100" and inp != ""):
        #sib
        sib = make_binary(inp[:2])
        inp = inp[2:]
        scale = sib[:2]
        index = sib[2:5]
        base  = sib[5:]

        RexR += reg
        RexX += index
        RexB += base
        displacement = "0x" + make_reverse(inp)
        operand1 = Reg64Dict[RexR]
        if(scale == "00" and RexX == "0100" and RexB == "0101"):
            #direct addressing
            operand2 = displacement
        else:
            if(prefix67):
                #32bit address
                operand2 = Reg64Dict[RexB][2] + "+" + Reg64Dict[RexX][2] + "*" + ScaleDict[scale]
                if(Reg64Dict[RexX][2] == "esp"):
                    operand2 = Reg64Dict[RexB][2]
                if(mod == "00" and Reg64Dict[RexB][2] == "ebp"): #no base
                    operand2 = Reg64Dict[RexX][2] + "*" + ScaleDict[scale]
            else:
                #64bit address
                operand2 = Reg64Dict[RexB][3] + "+" + Reg64Dict[RexX][3] + "*" + ScaleDict[scale]
                if(Reg64Dict[RexX][3] == "rsp"):
                    operand2 = Reg64Dict[RexB][3]
                if(mod == "00" and Reg64Dict[RexB][3] == "rbp"):
                    operand2 = Reg64Dict[RexX][3] + "*" + ScaleDict[scale] #no base
            if(mod != "00" or not_zero(displacement)):
                if(not_zero(displacement)):
                    operand2 += "+" + displacement
        operand2 = "[" + operand2 + "]"
        if(RexW == "1"):
            operand1 = operand1[3]
            operand2 = "QWORD PTR " + operand2
        elif(W == "0"):
            operand1 = operand1[0]
            operand2 = "BYTE PTR " + operand2
        elif(prefix66):
            operand1 = operand1[1]
            operand2 = "WORD PTR " + operand2
        else:
            operand1 = operand1[2]
            operand2 = "DWORD PTR " + operand2
        if(D == "0"):
            operand1, operand2 = operand2, operand1
    else:
        #no sib
        RexR += reg
        RexB += rm
        
        operand1 = Reg64Dict[RexR]
        operand2 = Reg64Dict[RexB]

        displacement = "0x" + make_reverse(inp)
        if(mod == "11"):
            if(W == "0" and operation != "bsf" and operation != "bsr"):
                operand1 = operand1[0]
                operand2 = operand2[0]
            elif(RexW == "1"):
                operand1 = operand1[3]
                operand2 = operand2[3]
            elif(prefix66):
                operand1 = operand1[1]
                operand2 = operand2[1]
            else:
                operand1 = operand1[2]
                operand2 = operand2[2]
        else:
            if(mod == "00" and RexB == "0101"):    
                #direct memory access
                operand2 = displacement
            else:
                #reg with memory (no sib)
                if(prefix67):
                    operand2 = operand2[2]
                else:
                    operand2 = operand2[3]
                
                if(not_zero(displacement)):
                    operand2 += "+" + displacement
            if(W == "0"):  
                operand1 = operand1[0]
                operand2 = "BYTE PTR [" + operand2 + "]"
            elif(RexW == "1"):
                operand1 = operand1[3]
                operand2 = "QWORD PTR [" + operand2 + "]"
            elif(prefix66):
                operand1 = operand1[1]
                operand2 = "WORD PTR [" + operand2 + "]"
            else:
                operand1 = operand1[2]
                operand2 = "DWORD PTR [" + operand2 + "]"
        if(D == "0"):
                operand1, operand2 = operand2, operand1
            
else:
    OpCode = make_binary(inp[:2])
    inpt == make_binary(inp)
    inp = inp[2:]
    if(OpCode == "00001111"):
        #OpCode length is 16 instead of 8
        OpCode += make_binary(inp[:2])
        inp = inp[2:]
    
        
    D = OpCode[-2]
    W = OpCode[-1]
    OpCode = OpCode[:-2]

    #jmp with displacement
    if(OpCode == "111010" and W == "1"):
        displacement = "0x" + make_reverse(inp)
        print("jmp", displacement)
        exit()
    if(OpCode == "111000" and D == "1" and W == "1"):
        displacement = "0x" + make_reverse(inp)
        print("jrcxz", displacement)
        exit()
    if(OpCode == "111010" and D == "0" and W == "0"):
        displacement = "0x" + make_reverse(inp)
        print("call", displacement)
        exit()
    if(OpCode == "110000" and D == "1" and W == "0"):
        displacement = "0x" + make_reverse(inp)
        print("ret", displacement)
        exit()
    if(OpCode == "011010" and W == "0"):
        displacement = "0x" + make_reverse(inp)
        print("push", displacement)
        exit()
    if(OpCode == "010100" or OpCode == "010101"):
        reg = OpCode[-1] + D + W
        print("push", RegDict[reg][3])
        exit()
    if(OpCode == "010110" or OpCode == "010111"):
        reg = OpCode[-1] + D + W
        print("pop", RegDict[reg][3])
        exit()    
    mod = make_binary(inp[:2])
    inp = inp[2:]
    reg = mod[2:5]
    rm  = mod[5:]
    mod = mod[:2]
    #print(mod, reg, rm)
    if(OpCode == "111111" and D == "1" and (reg == "000" or reg == "001")):
        single_operand = True
    if(OpCode == "110100" and D == "0" and (reg == "100" or reg == "101")):
        single_operand = True
    if(OpCode == "111101" and D == "1" and (reg == "010" or reg == "011")):
        single_operand = True
    
    #shl and shr register by immediate
    if(OpCode == "110000" and D == "0" and reg == "100"):
        single_operand = True
        ImmediateData = True
    if(OpCode == "110000" and D == "0" and reg == "101"):
        single_operand = True
        ImmediateData = True
    if(OpCode == "111101" and D == "1" and reg == "101"):
        operation = "imul"
        single_operand = True
    if(OpCode == "111101" and D == "1" and reg == "111"):
        operation = "idiv"
        single_operand = True
    if(OpCode == "100000" and reg == "101"):
        operation = "sub"
        single_operand = True
        ImmediateData = True
    if(OpCode == "00001111101111"):
        if(W == "0"):
            operation = "bsf"
        else:
            operation = "bsr"

    if(single_operand == True):
        #inc or dec
        if(mod == "11"):
            #register 32bit or less
            operand1 = RegDict[rm]
            if(W == "0"):
                operand1 = operand1[0]
            elif(prefix66):
                operand1 = operand1[1]
            else:
                operand1 = operand1[2]
            if(ImmediateData == True):
                operand2 = "0x" + make_reverse(inp)
        else:
            if(rm == "100" and inp != ""):
                #sib
                sib = make_binary(inp[:2])
                inp = inp[2:]
                scale = sib[:2]
                index = sib[2:5]
                base  = sib[5:]
                if(ImmediateData == True):
                    displacement = "0x" + make_reverse(inp[:-2])
                    inp = inp[-2:]
                else:
                    displacement = "0x" + make_reverse(inp)
                operand1 = RegDict[reg]
                if(scale == "00" and  index == "100" and  base == "101"):
                    #direct addressing
                    operand2 = displacement
                else:
                    if(prefix67):
                        #32bit address
                        operand2 = RegDict[base][2] + "+" + RegDict[index][2] + "*" + ScaleDict[scale]
                        if(mod == "00" and RegDict[base][2] == "ebp"): #no base
                            operand2 = RegDict[index][2] + "*" + ScaleDict[scale]
                    else:
                        #64bit address
                        operand2 = RegDict[base][3] + "+" + RegDict[index][3] + "*" + ScaleDict[scale]
                        if(mod == "00" and RegDict[base][3] == "rbp"): #no base
                            operand2 = RegDict[index][3] + "*" + ScaleDict[scale]
                    
                    if(mod != "00" or not_zero(displacement)):
                        if(not_zero(displacement)):
                            operand2 += "+" + displacement
                operand2 = "[" + operand2 + "]"
                if(W == "0"):
                    operand2 = "BYTE PTR " + operand2
                elif(prefix66):
                    operand2 = "WORD PTR " + operand2
                else:
                    operand2 = "DWORD PTR " + operand2
                operand1 = operand2
            else:
                operand1 = RegDict[rm][2]
                if(W == "0"):
                    operand1 = "BYTE PTR [" + operand1 + "]"
                elif(prefix66):
                    operand1 = "WORD PTR [" + operand1 + "]"
                else:
                    operand1 = "DWORD PTR [" + operand1 + "]"
        
        if(ImmediateData == True):
                operand2 = "0x" + make_reverse(inp)     
    elif(rm == "100" and inp != ""):
        #sib
        sib = make_binary(inp[:2])
        inp = inp[2:]
        scale = sib[:2]
        index = sib[2:5]
        base  = sib[5:]
        displacement = "0x" + make_reverse(inp)
        operand1 = RegDict[reg]
        if(scale == "00" and  index == "100" and  base == "101"):
            #direct addressing
            operand2 = displacement
        else:
            if(prefix67 == True):
                #32bit address
                operand2 = RegDict[base][2] + "+" + RegDict[index][2] + "*" + ScaleDict[scale]
                if(RegDict[index][2] == "esp"):
                    operand2 = RegDict[base][2]
                if(mod == "00" and RegDict[base][2] == "ebp"): #no base
                    operand2 = RegDict[index][2] + "*" + ScaleDict[scale]
            else:#64 bit address
                operand2 = RegDict[base][3] + "+" + RegDict[index][3] + "*" + ScaleDict[scale]
                if(RegDict[index][3] == "rsp"):
                    operand2 = RegDict[base][3]
                if(mod == "00" and RegDict[base][3] == "rbp"): #no base
                    operand2 = RegDict[index][3] + "*" + ScaleDict[scale]
            
            if(mod != "00" or not_zero(displacement)):
                if(not_zero(displacement)):
                    operand2 += "+" + displacement
        operand2 = "[" + operand2 + "]"
        if(W == "0"):
            operand1 = operand1[0]
            operand2 = "BYTE PTR " + operand2
        elif(prefix66):
            operand1 = operand1[1]
            operand2 = "WORD PTR " + operand2
        else:
            operand1 = operand1[2]
            operand2 = "DWORD PTR " + operand2
        if(D == "0"):
            operand1, operand2 = operand2, operand1
    else:
        #no sib
        
        operand1 = RegDict[reg]
        operand2 = RegDict[rm]
        displacement = "0x" + make_reverse(inp)
        if(mod == "11"):
            #2 registers
            if(W == "0"):
                operand1 = operand1[0]
                operand2 = operand2[0]
            elif(prefix66):
                operand1 = operand1[1]
                operand2 = operand2[1]
            else:
                if(prefix67 or OpCode == "100001" or operation == "bsr" or operation == "bsf"):
                    operand1 = operand1[2]
                    operand2 = operand2[2]
                else:
                    operand1 = operand1[3]
                    operand2 = operand2[3]
        else:
            #one register and one memory
            if(rm == "101" and mod == "00"):
                #direct addressing
                operand2 = displacement
            else:
                if(prefix67):
                    operand2 = operand2[2] #address can be 32bits only
                else:
                    operand2 = operand2[3]
                if(not_zero(displacement)):
                    operand2 += "+" + displacement
            if(W == "0"):
                operand1 = operand1[0]
                operand2 = "BYTE PTR [" + operand2 + "]"
            elif(prefix66):
                operand1 = operand1[1]
                operand2 = "WORD PTR [" + operand2 + "]"
            else:
                operand1 = operand1[2]
                operand2 = "DWORD PTR [" + operand2 + "]"
        if(D == "0"):
            operand1, operand2 = operand2, operand1
#special cases
#normal cases
if(OpCode == "100010"):
    operation = "mov"
if(OpCode == "001000"):
    operation = "and"
if(OpCode == "000010"):
    operation = "or"
if(OpCode == "001100"):
    operation = "xor"
if(OpCode == "000100"):
    operation = "adc"
    
if(OpCode == "000000"):
    operation = "add"
if(OpCode == "00001111110000"):
    operation = "xadd"

if(OpCode == "001010"):
    operation = "sub"

if(OpCode == "00001111101111"):
    if(W == "0"):
        operation = "bsf"
    else:
        operation = "bsr"
    operand1, operand2 = operand2, operand1
if(OpCode == "000110"):
    operation = "sbb"

if(OpCode == "001110"):
    operation = "cmp"

if(OpCode == "100001"):
    operation = "test"

if(OpCode == "00001111101011" and D == "1" and W == "1"):
    operation = "imul"

if(OpCode == "111101" and D == "1" and reg == "111"):
    operation = "idiv"

if(OpCode == "100001"):
    if(D == "0"):
        operation = "test"
    else:
        operation = "xchg"
        operand1, operand2 = operand2, operand1
#1operand
if(OpCode == "111111"):
    if(reg == "000"):
        operation = "inc"
    if(reg == "001"):
        operation = "dec"

if(OpCode == "110100"):
    ImmediateData = True
    operand2 = "1"
    if(reg == "100"):
        operation = "shl"
    else:
        operation = "shr"

if(OpCode == "110000" and D == "0" and reg == "100"):
    operation = "shl"
if(OpCode == "110000" and D == "0" and reg == "101"):
    operation = "shr"
    
if(OpCode == "110000"):
    if(reg == "100"):
        operation = "shl"
    else:
        operation = "shr"

if(OpCode == "111101"):
    if(reg == "011"):
        operation = "neg"
    if(reg == "010"):
        operation = "not"

if(displacement == "0x0"):
    if(operand2.find("PTR") != -1):
        operand2 = operand2[:-1] + "+0x0]"
    else:
        operand1 = operand1[:-1] + "+0x0]"

if(single_operand == True):
    if(ImmediateData):
        print("{} {},{}".format(operation, operand1, operand2))
    else:
        print(operation, operand1)

else:
    print("{} {},{}".format(operation, operand1, operand2))