from NodeKlein import *
from TypeChecker import *
from genThreeAddress import *

class CodeGenerator:
    def __init__(self, ast, symbolTable,outputFile):
        self.ast = ast
        self.symbolTable = symbolTable
        self.branchList = []
        self.tableIndex = TableIndex()
        self.outFile = open(outputFile, "w")
        self.registerTable = {("1") : "",("2") : "", ("3") : "", ("4") : ""}
        self.lastRegister = 3 
        self.currentFunction = ""
        self.labelDict = {}
        self.gotoList = []
        self.ifStatements = []
        self.argNum = 0
        self.previousRegTables = []

    def GenerateTM(self):
        threeAddress, self.symbolTable = genThreeAddress(self.ast,self.symbolTable)
        lineNumber = 0
        lineNumber = self.GenerateProlog(lineNumber)
        lineNumber = self.generateProgramBody(lineNumber,threeAddress)
        self.GenerateBranches()
        self.genIfStatements()
        self.generateGoto()
        return

    def GenerateProlog(self, lineNumber):
        numArgs = len(self.symbolTable["main"][self.tableIndex.paramDict()])
        numTemp = len(self.symbolTable["main"][self.tableIndex.tempDict()])
        self.makeHeader("Prolog")
        self.makeRM(lineNumber, "LDC", "4", "6", "7", "Calculate Return Address")
        self.makeRM(lineNumber + 1, "ST", "4", str(numArgs+1), "6", "Store Return Address on the Stack Frame")
        self.makeRM(lineNumber + 2, "LDC", "5", str(numArgs+2), "0", "Set New Status")
        self.makeRM(lineNumber + 3, "ST", "5", "0", "5", "Store Current Status")
        self.makeRM(lineNumber + 4, "LDA", "6", str(6 + numTemp), "5", "Set New Top Pointer")
        self.branchList.append([lineNumber + 5, "main"])
        self.makeRM(lineNumber + 6, "LD", "4", "0", "0", "Load Returned Value")
        self.makeRO(lineNumber + 7, "OUT", "4", "0", "0", "Print Returned Value")
        self.makeRO(lineNumber + 8, "HALT", "0", "0", "0", "End Program")
        return lineNumber + 9

    def generateProgramBody(self, lineNumber, threeAddress):
        index = 0
        while index < len(threeAddress):
            address = threeAddress[index]
            if self.getOp(address) == op.ENTRY:
                lineNumber,index = self.genFunction(lineNumber,threeAddress,index)
            else:
                raise TypeError("Error Occured While Generating Function")
        return lineNumber

    def genFunction(self,lineNumber,threeAddress,index):
        functionName = self.getResult(threeAddress[index])
        self.currentFunction = functionName
        self.symbolTable[functionName][self.tableIndex.lineNumber()] = lineNumber
        self.makeHeader(functionName)
        lineNumber = self.StoreRegisters(lineNumber)
        operation = self.getOp(threeAddress[index])
        while operation != op.EXIT:
            index += 1
            line = threeAddress[index]
            operation = self.getOp(line)
            lineNumber = self.genLine(lineNumber,line)
        index += 1
        lineNumber = self.LoadRegisters(lineNumber)
        numArgs = len(self.symbolTable[functionName][self.tableIndex.paramDict()])
        numTemp = len(self.symbolTable[functionName][self.tableIndex.tempDict()])
        self.makeRM(lineNumber, "LDA", "6", str(-(3 + numArgs)), "5", "Set Top Pointer Back")
        self.makeRM(lineNumber + 1, "LD", "5", "0", "5", "Set Status Pointer Back")
        self.makeRM(lineNumber + 2, "LD", "7", str(numArgs + 2), "6", "Jump Back To Wherever Called From")
        return lineNumber + 3,index

    def genLine(self, lineNumber, line):
        operation = self.getOp(line)
        if operation == op.ID:
            identifier = self.getArg1(line)
            paramDict = self.symbolTable[self.currentFunction][self.tableIndex.paramDict()]
            order = paramDict[identifier][1]
            numArgs = len(paramDict)
            distance = order - numArgs -1
            result = self.getResult(line)
            register,lineNumber = self.getRegister(result,lineNumber)
            self.makeRM(lineNumber, "LD", register, str(distance), "5", "Load Arg {} into reg {}".format(order,register))
            return lineNumber + 1
        elif operation == op.NUM:
            result = self.getResult(line)
            register,lineNumber = self.getRegister(result,lineNumber)
            num = self.getArg1(line)
            self.makeRM(lineNumber, "LDC", register, str(num), "0", "Loading Number {} into register {}".format(num,register))
            return lineNumber + 1
        elif operation == op.BOOL:
            result = self.getResult(line)
            register,lineNumber = self.getRegister(result,lineNumber)
            boolean = self.getArg1(line)
            if boolean == "true":
                boolean = "1"
            else:
                boolean = "0"
            self.makeRM(lineNumber, "LDC", register, boolean, "0", "Loading Boolean {} into register {}".format(boolean,register))
            return lineNumber + 1
        elif operation == op.PLUS:
            lineNumber = self.genBinaryIntExpr(lineNumber, line, "ADD")
            return lineNumber
        elif operation == op.MINUS:
            lineNumber = self.genBinaryIntExpr(lineNumber, line, "SUB")
            return lineNumber
        elif operation == op.MULT:
            lineNumber = self.genBinaryIntExpr(lineNumber, line, "MUL")
            return lineNumber
        elif operation == op.DIVIDE:
            lineNumber = self.genBinaryIntExpr(lineNumber, line, "DIV")
            return lineNumber
        elif operation == op.RETURN:
            numCallingArgs = len(self.symbolTable[self.currentFunction][self.tableIndex.paramDict()])
            result = self.getResult(line)
            register, lineNumber = self.searchRegister(result,lineNumber)
            self.makeRM(lineNumber, "ST", register, str(-(numCallingArgs+2)), "5", "Store Return Value")
            return lineNumber + 1
        elif operation == op.EXIT:
            return lineNumber
        elif operation == op.EQUAL:
            lineNumber = self.genBinaryBoolExpr(lineNumber, line, "JEQ")
            return lineNumber
        elif operation == op.LESS:
            lineNumber = self.genBinaryBoolExpr(lineNumber, line, "JLT")
            return lineNumber
        elif operation == op.OR:
            lineNumber = self.genOrExpr(lineNumber, line)
            return lineNumber
        elif operation == op.AND:
            lineNumber = self.genAndExpr(lineNumber, line)
            return lineNumber
        elif operation == op.NEGATE:
            arg1 = self.getArg1(line)
            result = self.getResult(line)
            reg1, lineNumber = self.searchRegister(arg1,lineNumber)
            resultReg,lineNumber = self.getRegister(result, lineNumber)
            self.makeRO(lineNumber, "SUB", resultReg, "0", reg1, "Negating reg {} and storing in reg {}".format(reg1,resultReg)) 
            return lineNumber + 1
        elif operation == op.NOT:
            arg1 = self.getArg1(line)
            result = self.getResult(line)
            reg1, lineNumber = self.searchRegister(arg1,lineNumber)
            resultReg,lineNumber = self.getRegister(result, lineNumber)
            self.makeRM(lineNumber, "JEQ", reg1, "2","7", "Checking if boolean exprssion is true")
            self.makeRM(lineNumber + 1, "LDC", resultReg, "0", "0", "Load False into reg {}".format(resultReg))
            self.makeRM(lineNumber + 2, "LDA", "7", "1", "7", "Jump over True")
            self.makeRM(lineNumber + 3, "LDC", resultReg, "1", "0", "Load True into reg {}".format(resultReg))
            return lineNumber + 4
        elif operation == op.PRINT:
            result = self.getResult(line)
            resultReg,lineNumber = self.searchRegister(result, lineNumber)
            self.makeRO(lineNumber, "OUT", resultReg, "0", "0", "Print value in reg {}".format(resultReg))
            return lineNumber + 1
        elif operation == op.LABEL:
            label = self.getResult(line)
            self.labelDict[label] = lineNumber
            return lineNumber
        elif operation == op.GOTO:
            label = self.getResult(line)
            self.gotoList.append([label, lineNumber])
            return lineNumber + 1
        elif operation == op.IF_NOT:
            lineNumber = self.genIfExpr(line, lineNumber)
            return lineNumber
        elif operation == op.PARAM:
            arg = self.getResult(line)
            reg, lineNumber = self.searchRegister(arg,lineNumber)
            memLocation = str(self.argNum + 2)
            self.makeRM(lineNumber, "ST", reg, memLocation, "6", "Store Arg {} at memLocation {}".format(reg,memLocation))
            self.argNum += 1
            return lineNumber + 1
        elif operation == op.CALL:
            lineNumber = self.genFunctionCall(line, lineNumber)
            return lineNumber
        elif operation == op.STORE:
            temp = self.getResult(line)
            keyList = []
            for key in self.registerTable:
                if self.registerTable[key] == temp:
                    keyList.append(key)
            aKey = keyList[0]
            self.registerTable[aKey] = ""
            tempDict = self.symbolTable[self.currentFunction][self.tableIndex.tempDict()]
            order = tempDict[temp]
            memLocation = order - len(tempDict)
            self.makeRM(lineNumber, "ST", aKey, memLocation, "6", 
            "Store Previous register {} contents {} in mem Location {}".format(aKey,temp,str(memLocation)))
            return lineNumber + 1
        elif operation == op.LOAD:
            temp = self.getResult(line)
            resultReg,lineNumber = self.getRegister(temp, lineNumber)
            tempDict = self.symbolTable[self.currentFunction][self.tableIndex.tempDict()]
            order = tempDict[temp]
            memLocation = order - len(tempDict)
            self.makeRM(lineNumber, "LD", resultReg, memLocation, "6","Loading {} into reg {}".format(temp,resultReg))
            return lineNumber + 1
        elif operation == op.SETARG:
            argNum = self.getResult(line)
            memLocation = argNum + 1
            temp = self.getArg1(line)
            reg, lineNumber = self.searchRegister(temp,lineNumber)
            self.makeRM(lineNumber, "ST", reg, str(-(memLocation)), "5", 
            "Store {} in arg Location {} from status pointer".format(temp,str(-(memLocation))))
            return lineNumber + 1


    def genFunctionCall(self, line, lineNumber):
        self.argNum = 0
        function = self.getArg1(line)
        numCalledArgs = len(self.symbolTable[function][self.tableIndex.paramDict()])
        numTemp = len(self.symbolTable[function][self.tableIndex.tempDict()])
        if self.registerTable["4"] == "":
            self.makeRM(lineNumber, "LDA", "4", "5", "7", "Calculate Return Address")
            self.makeRM(lineNumber + 1, "ST", "4", str(numCalledArgs+2), "6", "Store Return Address on the Stack Frame")
            self.makeRM(lineNumber + 2, "ST", "5", str(numCalledArgs+3), "6", "Store Current Status")
            self.makeRM(lineNumber + 3, "LDA", "5", str(numCalledArgs+3), "6", "Set New Status")
            self.makeRM(lineNumber + 4, "LDA", "6", str(6+numTemp), "5", "Set New Top Pointer")
            self.branchList.append([lineNumber + 5, function])
            result = self.getResult(line)       
            reg, lineNumber = self.searchRegister(result,lineNumber + 6)
        else:
            temp = self.registerTable["4"]
            tempDict = self.symbolTable[self.currentFunction][self.tableIndex.tempDict()]
            order = tempDict[temp]
            memLocation = order - len(tempDict)
            self.makeRM(lineNumber, "ST", "4", memLocation, "6", 
            "Store Previous register {} contents {} in mem Location {}".format("4",temp,str(memLocation)))
            self.makeRM(lineNumber + 1, "LDA", "4", "6", "7", "Calculate Return Address")
            self.makeRM(lineNumber + 2, "ST", "4", str(numCalledArgs+2), "6", "Store Return Address on the Stack Frame")
            self.makeRM(lineNumber + 3, "LD", "4", str(memLocation), "6", "Restoring tempVariable {} into register {}".format(temp, "4"))
            self.makeRM(lineNumber + 4, "ST", "5", str(numCalledArgs+3), "6", "Store Current Status")
            self.makeRM(lineNumber + 5, "LDA", "5", str(numCalledArgs+3), "6", "Set New Status")
            self.makeRM(lineNumber + 6, "LDA", "6", str(6+numTemp), "5", "Set New Top Pointer")
            self.branchList.append([lineNumber + 7, function])
            result = self.getResult(line)       
            reg, lineNumber = self.searchRegister(result,lineNumber + 8)
        self.makeRM(lineNumber, "LD", reg, "1", "6", "Load Returned Value")
        return lineNumber + 1



    def genIfExpr(self, line, lineNumber):
        label = self.getResult(line)
        ifTest = self.getArg1(line)
        self.ifStatements.append([ifTest, label, lineNumber,self.currentFunction,self.registerTable])
        return lineNumber + 3


    def genBinaryBoolExpr(self, lineNumber, line, operation):
        arg1 = self.getArg1(line)
        arg2 = self.getArg2(line)
        result = self.getResult(line)
        reg1, lineNumber = self.searchRegister(arg1,lineNumber)
        reg2, lineNumber = self.searchRegister(arg2,lineNumber)
        resultReg,lineNumber = self.getRegister(result, lineNumber)
        self.makeRO(lineNumber, "SUB", resultReg, reg1, reg2, "Subtracting reg {} and reg {}".format(reg1,reg2))
        self.makeRM(lineNumber + 1, operation, resultReg, "2","7", "Checking if boolean exprssion is true")
        self.makeRM(lineNumber + 2, "LDC", resultReg, "0", "0", "Load False into reg {}".format(resultReg))
        self.makeRM(lineNumber + 3, "LDA", "7", "1", "7", "Jump over True")
        self.makeRM(lineNumber + 4, "LDC", resultReg, "1", "0", "Load True into reg {}".format(resultReg))
        return lineNumber + 5

    def genOrExpr(self, lineNumber, line):
        arg1 = self.getArg1(line)
        arg2 = self.getArg2(line)
        result = self.getResult(line)
        reg1, lineNumber = self.searchRegister(arg1,lineNumber)
        reg2, lineNumber = self.searchRegister(arg2,lineNumber)
        resultReg,lineNumber = self.getRegister(result, lineNumber)
        self.makeRO(lineNumber, "ADD", resultReg, reg1, reg2, "Adding reg {} and reg {}".format(reg1,reg2))
        self.makeRM(lineNumber + 1, "JGT", resultReg, "2","7", "Checking if boolean exprssion is true")
        self.makeRM(lineNumber + 2, "LDC", resultReg, "0", "0", "Load False into reg {}".format(resultReg))
        self.makeRM(lineNumber + 3, "LDA", "7", "1", "7", "Jump over True")
        self.makeRM(lineNumber + 4, "LDC", resultReg, "1", "0", "Load True into reg {}".format(resultReg))
        return lineNumber + 5

    def genAndExpr(self, lineNumber, line):
        arg1 = self.getArg1(line)
        arg2 = self.getArg2(line)
        result = self.getResult(line)
        reg1, lineNumber = self.searchRegister(arg1,lineNumber)
        reg2, lineNumber = self.searchRegister(arg2,lineNumber)
        resultReg,lineNumber = self.getRegister(result, lineNumber)
        self.makeRO(lineNumber, "ADD", resultReg, reg1, reg2, "Adding reg {} and reg {}".format(reg1,reg2))
        self.makeRM(lineNumber + 1, "LDA", resultReg, "-2", resultReg, "Subtract 2 from reg {}".format(resultReg))
        self.makeRM(lineNumber + 2, "JEQ", resultReg, "2","7", "Checking if boolean exprssion is true")
        self.makeRM(lineNumber + 3, "LDC", resultReg, "0", "0", "Load False into reg {}".format(resultReg))
        self.makeRM(lineNumber + 4, "LDA", "7", "1", "7", "Jump over True")
        self.makeRM(lineNumber + 5, "LDC", resultReg, "1", "0", "Load True into reg {}".format(resultReg))
        return lineNumber + 6

    def genBinaryIntExpr(self,lineNumber,line, operation):
        arg1 = self.getArg1(line)
        arg2 = self.getArg2(line)
        result = self.getResult(line)
        reg1, lineNumber = self.searchRegister(arg1,lineNumber)
        reg2, lineNumber = self.searchRegister(arg2,lineNumber)
        resultReg,lineNumber = self.getRegister(result, lineNumber)
        self.makeRO(lineNumber, operation, resultReg, reg1, reg2, "Compute Operation {} on reg {} and reg {}".format(operation,reg1,reg2))
        return lineNumber + 1


    def GenerateBranches(self):
        self.makeHeader("Branches")
        for branch in self.branchList:
            dest = self.symbolTable[branch[1]][self.tableIndex.lineNumber()]
            self.makeRM(branch[0], "LDC", "7", str(dest), "0", "Jumping to {}".format(branch[1])) 

    def generateGoto(self):
        self.makeHeader("GoTo")
        for goto in self.gotoList:
            label = goto[0]
            lineNumber = goto[1]
            dest = self.labelDict[label] 
            self.makeRM(lineNumber, "LDC", "7", str(dest), "0", "Go to {}".format(label))  

    def genIfStatements(self):
        self.makeHeader("If Conditions")
        for statement in self.ifStatements:
            ifTest = statement[0]
            label = statement[1]
            lineNumber = statement[2]
            function = statement[3]
            regTable = statement[4]
            dest = self.labelDict[label]
            register = ((self.lastRegister + 1) % 4) + 1
            self.lastRegister = register
            # Store contents of the register
            previousTemp = regTable[str(register)]
            if previousTemp == "":
                self.makeRM(lineNumber, "LDC", "0", "0", "0","loading constant zero to ensure lineNumbers line up")
                regTable[str(register)] = ifTest
                tempDict = self.symbolTable[function][self.tableIndex.tempDict()]
                order = tempDict[ifTest]
                memLocation = order - len(tempDict)
                self.makeRM(lineNumber + 1, "LD", register, str(memLocation), "6", "Restoring tempVariable {} into register {}".format(ifTest, register))
                self.makeRM(lineNumber + 2, "JEQ", register, dest,"0", "Jumping to {} if reg {} is false".format(dest,register))
            else:
                tempDict = self.symbolTable[function][self.tableIndex.tempDict()]
                order = tempDict[previousTemp]
                memLocation = order - len(tempDict)
                self.makeRM(lineNumber, "ST", register, str(memLocation), "6", 
                "Store Previous register {} contents {} in mem Location {}".format(register,previousTemp,str(memLocation)))
                regTable[str(register)] = ifTest
                order = tempDict[ifTest]
                memLocation = order - len(tempDict)
                self.makeRM(lineNumber + 1, "LD", register, str(memLocation), "6", "Restoring tempVariable {} into register {}".format(ifTest, register))
                self.makeRM(lineNumber + 2, "JEQ", register, dest,"0", "Jumping to {} if reg {} is false".format(dest,register))


    def LoadRegisters(self, lineNumber):
        self.makeRM(lineNumber, "LD", "1", "1", "5", "Restoring Previous R1") 
        self.makeRM(lineNumber + 1, "LD", "2", "2", "5", "Restoring Previous R2")
        self.makeRM(lineNumber + 2, "LD", "3", "3", "5", "Restoring Previous R3")
        self.makeRM(lineNumber + 3, "LD", "4", "4", "5", "Restoring Previous R4")
        self.makeRM(lineNumber + 4, "LD", "6", "6", "5", "Restoring Previous R6")
        self.makeRM(lineNumber + 5, "LD", "5", "5", "5", "Restoring Previous R5")
        self.registerTable = self.previousRegTables.pop()               
        return lineNumber + 6


    def StoreRegisters(self, lineNumber):
        self.previousRegTables.append(self.registerTable)
        self.makeRM(lineNumber, "ST", "1", "1", "5", "Store Previous R1")
        self.makeRM(lineNumber + 1, "ST", "2", "2", "5", "Store Previous R2")
        self.makeRM(lineNumber + 2, "ST", "3", "3", "5", "Store Previous R3")
        self.makeRM(lineNumber + 3, "ST", "4", "4", "5", "Store Previous R4")
        self.makeRM(lineNumber + 4, "ST", "5", "5", "5", "Store Previous R5")
        self.makeRM(lineNumber + 5, "ST", "6", "6", "5", "Store Previous R6")
        self.registerTable = {("1") : "",("2") : "", ("3") : "", ("4") : ""}
        return lineNumber + 6



    def makeRO(self, lineNumber, op, r1, r2, r3, comment):
        opcode = "{}:        {} {},{},{}      {} {}\n"
        self.outFile.write(opcode.format(lineNumber, op, r1, r2, r3, ";", comment))
    
    def makeRM(self, lineNumber, op, r1, offset, r2, comment):
        opcode = "{}:        {} {},{}({})     {} {}\n"
        self.outFile.write(opcode.format(lineNumber, op, r1, offset, r2, ";", comment))

    def makeHeader(self, name):
        string = "*\n* {}\n*\n"
        self.outFile.write(string.format(name))

    def getOp(self, address):
        return address[0]

    def getArg1(self, address):
        return address[1]

    def getArg2(self, address):
        return address[2]

    def getResult(self, address):
        return address[3]

    def getRegister(self, tempVariable, lineNumber):
        for key in self.registerTable:
            if self.registerTable[key] == "":
                self.registerTable[key] = tempVariable
                return key, lineNumber
        # No Open Register
        register = ((self.lastRegister + 1) % 4) + 1
        self.lastRegister = register
        # Store contents of the register
        previousTemp = self.registerTable[str(register)]
        tempDict = self.symbolTable[self.currentFunction][self.tableIndex.tempDict()]
        order = tempDict[previousTemp]
        memLocation = order - len(tempDict)
        self.makeRM(lineNumber, "ST", register, str(memLocation), "6", 
        "Store Previous register {} contents {} in mem Location {}".format(register,previousTemp,str(memLocation)))
        self.registerTable[str(register)] = tempVariable
        return register, lineNumber + 1

    def searchRegister(self, tempVariable, lineNumber):
        for key in self.registerTable:
            if self.registerTable[key] == tempVariable:
                return key, lineNumber
        register, lineNumber = self.getRegister(tempVariable, lineNumber)
        tempDict = self.symbolTable[self.currentFunction][self.tableIndex.tempDict()]
        order = tempDict[tempVariable]
        memLocation = order - len(tempDict)
        self.makeRM(lineNumber, "LD", register, str(memLocation), "6", "Restoring tempVariable {} into register {}".format(tempVariable, register))
        return register, lineNumber + 1

    


