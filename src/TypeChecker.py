from Parser import *
from NodeKlein import *
from enum import Enum


class TableIndex():
    def __init__ (self):
        pass
    def dataType(self):
        return 0
    def paramDict(self):
        return 1
    def calls(self):
        return 2
    def calledBy(self):
        return 3
    def returnType(self):
        return 4
    def lineNumber(self):
        return 5
    def tempDict(self):
        return 6
    def tailRecursive(self):
        return 7

class DataType(Enum):
    integer     = 0
    boolean     = 1


class FunctionType():
    def __init__(self, formalsType, returnType):
        self.formalsType = formalsType
        self.returnType = returnType
    
    def getFormalType(self):
        return self.formalsType

    def getReturnType(self):
        return self.returnType

    def __str__(self):
        return "Function(" + str(self.formalsType) + ", " + str(self.returnType) + ")"
class OrType():
    def __init__(self, type1, type2):
        self.type1 = type1
        self.type2 = type2

    def __str__(self):
        return "Type1: " + str(self.type1) + " or Type2: " + str(self.type2)

class tupleType():
    def __init__(self, numOfArgs, listOfArgs):
        self.numOfArgs = numOfArgs
        self.listOfArgs = listOfArgs

    def __str__(self):
        myTuple = (self.numOfArgs, self.listOfArgs)
        return str(myTuple)
    
    def getNum(self):
        return self.numOfArgs

    def getList(self):
        return self.listOfArgs

    def __eq__(self, other):
        if isinstance(other, tupleType):
            return self.getNum() == other.getNum() and self.getList() == other.getList()
        return False

class ErrorType():
    def __init__(self, message):
        self.message = message

    def getError(self):
        return self.message

    def __str__(self):
        return "type error"

# Global Variables
# symbolTable[functionName] = [dataType, paramDict = {}, [functionCalls],[callByFunctions],returnType,lineNumber, tempDict = {}, tail-recursive]
symbolTable = {("print") : [OrType(DataType.integer,DataType.boolean),{"aExpr": "someExpression"},[],[],"No Return Type",0,{},False]}
errorList = []
currentFunctName = ""
tableIndex = TableIndex()


def typeCheck (ast):
    definitionsNode = ast.getDefinitions()
    listOfDefs = definitionsNode.getDefinitions()
    for function in listOfDefs:
        functionNameNode = function.getName()
        functionName = functionNameNode.getValue()

        if functionName in symbolTable:
            errorMessage = "Error: NonUnique function " + functionName + " in program"
            error = ErrorType(errorMessage)
            addError(error)
        else:    
            addToTable(function)

    for function in listOfDefs:
        function = typeCheckFunction(function)
    
    if "main" not in symbolTable:
        errorMessage = "Error: No main function defined in the program"
        error = ErrorType(errorMessage)
        addError(error)

    if len(errorList) != 0:
        output = ""
        for error in errorList:
            message = error.getError()
            output = output + message + "\n"
        raise TypeError(output)
    return symbolTable, ast

def addToTable(functionNode):
    global currentFunctName
    idNode = functionNode.getName()
    functionName = idNode.getValue()
    currentFunctName = functionName
    returnTypeNode = functionNode.getReturnType()
    paramsNode = functionNode.getParameters()
    returnType = typeCheckType(returnTypeNode)
    paramsType = typeCheckParams(paramsNode)

    if functionName in symbolTable:
        errorMessage = "Error: Cannot have more than one function with the name " + functionName
        error = ErrorType(errorMessage)
        addError(error)
    else:
        symbolTable[functionName] = [FunctionType(paramsType.getDataType(),returnType.getDataType()),
            {},[],[],returnType.getDataType(),0,{},False]

        addParams(functionName, paramsNode)


def addParams(functionKey, paramsNode):
    parameterList = paramsNode.getParameters()
    paramDict = symbolTable[functionKey][tableIndex.paramDict()]
    order = 0
    parameterList.reverse()
    for param in parameterList:
        idNode = param.getName()
        typeNode = param.getDataTypeNode()
        idName = idNode.getValue()
        typeValue = typeCheckType(typeNode)
        if idName in paramDict:
            errorMessage = "Error: NonUnique argument " + str(idName) + " in function " + functionKey
            error = ErrorType(errorMessage)
            addError(error)
        else:
            paramDict[idName] = [typeValue.getDataType(),order]
        order += 1
        
def typeCheckFunction(functionNode):
    global currentFunctName
    idNode = functionNode.getName()
    functionName = idNode.getValue()
    currentFunctName = functionName
#    print("Type Checking Function: " + currentFunctName)
    returnTypeNode = functionNode.getReturnType()
    paramsNode = functionNode.getParameters()
    bodyNode = functionNode.getBody()

    returnType = typeCheckType(returnTypeNode)
    paramsType = typeCheckParams(paramsNode)
    bodyType = typeCheckBody(bodyNode)
    if returnType.getDataType() == bodyType.getDataType():
        functionNode.setDataType(FunctionType(paramsType.getDataType(), returnType.getDataType()))
    else:
        errorMessage = "Error: For Function " + str(functionName) + " returnType " + str(returnType.getDataType()) \
        + " bodyType " +  str(bodyType.getDataType()) + " do not match"
        error = ErrorType(errorMessage)
        functionNode.setDataType(error) 
        addError(error)

    return functionNode

def typeCheckType(typeNode):
    if typeNode.isInteger():
        typeNode.setDataType(DataType.integer)
    else:
        typeNode.setDataType(DataType.boolean)
    return typeNode

def typeCheckParams(paramsNode):
    paramsList = paramsNode.getParameters()
    typeList = []
    for param in paramsList:
        typeNode = param.getDataTypeNode()
        dataType = typeCheckType(typeNode)
        param.setDataType(dataType.getDataType())
        typeList.append(dataType.getDataType())
    numOfParams = len(paramsList)
    paramType = tupleType(numOfParams, typeList)
    paramsNode.setDataType(paramType)
    return paramsNode

def typeCheckBody(bodyNode):
    if bodyNode.getNodeType() == NodeType.Body:
        printList = bodyNode.getPrintStatements()
        for printNode in printList:
            printNode = typeCheckPrint(printNode)
        if len(printList) != 0:
            symbolTable[currentFunctName][tableIndex.calls()].append("print")
            symbolTable["print"][tableIndex.calledBy()].append(currentFunctName)
        exprNode = bodyNode.getExpr()
        exprNodeType = exprNode.getNodeType()
        if exprNodeType == NodeType.FunctCall:
            nameNode = exprNode.getName()
            functName = nameNode.getValue()
            if functName == currentFunctName:
                symbolTable[currentFunctName][tableIndex.tailRecursive()] = True
        elif exprNodeType == NodeType.If:
            elseNode = exprNode.getElseExpr()
            elseNodeType = elseNode.getNodeType()
            if elseNodeType == NodeType.FunctCall:
                nameNode = elseNode.getName()
                functName = nameNode.getValue()
                if functName == currentFunctName:
                    symbolTable[currentFunctName][tableIndex.tailRecursive()] = True
        bodyType = typeCheckExpr(exprNode)
        bodyNode.setDataType(bodyType.getDataType())
        return bodyNode
    else:
        bodyType = typeCheckExpr(bodyNode)
        bodyNode.setDataType(bodyType.getDataType())
        return bodyNode

def typeCheckPrint(printNode):
    printExpr = printNode.getExpr()
    exprType = typeCheckExpr(printExpr)

    if exprType.getDataType() == DataType.boolean or exprType.getDataType() == DataType.integer \
        or exprType.getDataType() == OrType(DataType.boolean,DataType.integer) or \
        exprType.getDataType() == OrType(DataType.integer,DataType.boolean):
        printNode.setDataType(exprType)
    
    else:
        errorMessage = "Error: In Function " + currentFunctName + " Unexpected DataType " + "in print statement"
        error = ErrorType(errorMessage)
        printNode.setDataType(error) 
        addError(error)
    return printNode

def typeCheckExpr(expr):
    exprNodeType = expr.getNodeType() 
    if exprNodeType == NodeType.Or:
        exprType = typeCheckBoolExpr(expr)
    elif exprNodeType == NodeType.And:
        exprType = typeCheckBoolExpr(expr)
    elif exprNodeType == NodeType.LessThan:
        exprType = typeCheckCompare(expr)
    elif exprNodeType == NodeType.Equal:
        exprType = typeCheckCompare(expr)
    elif exprNodeType == NodeType.Plus:
        exprType = typeCheckIntExpr(expr)
    elif exprNodeType == NodeType.Minus:
        exprType = typeCheckIntExpr(expr)
    elif exprNodeType == NodeType.Times:
        exprType = typeCheckIntExpr(expr)
    elif exprNodeType == NodeType.Divide:
        exprType = typeCheckIntExpr(expr)
    elif exprNodeType == NodeType.Not:
        exprType = typeCheckNotExpr(expr)
    elif exprNodeType == NodeType.Negate:
        exprType = typeCheckNegate(expr)
    elif exprNodeType == NodeType.If:
        exprType = typeCheckIfExpr(expr)
    elif exprNodeType == NodeType.FunctCall:
        exprType = typeCheckFunctCall(expr)
    elif exprNodeType == NodeType.Id:
        exprType = typeCheckId(expr)
    elif exprNodeType == NodeType.Num:
        exprType = typeCheckNum(expr)
    elif exprNodeType == NodeType.Bool:
        exprType = typeCheckBool(expr)
    else:
        errorMessage = "Error: In Function " + currentFunctName + " Expression " + str(expr) \
        + " is not a valid expression"
        error = ErrorType(errorMessage) 
        addError(error)
        expr.setDataType(error)
        return expr
    expr.setDataType(exprType.getDataType())   
    return expr

def typeCheckBoolExpr(exprNode):
    leftNode = exprNode.getLeftOp()
    rightNode = exprNode.getRightOp()

    leftType = typeCheckExpr(leftNode)
    rightType = typeCheckExpr(rightNode)

    if leftType.getDataType() == DataType.boolean and rightType.getDataType() == DataType.boolean:
        exprNode.setDataType(DataType.boolean)
    else:
        errorMessage = "Error: In Function " + currentFunctName + " Expression " + str(exprNode) \
        + " does not have boolean operands"
        error = ErrorType(errorMessage) 
        addError(error)
        exprNode.setDataType(error)
    return exprNode

def typeCheckCompare(exprNode):
    leftNode = exprNode.getLeftOp()
    rightNode = exprNode.getRightOp()

    leftType = typeCheckExpr(leftNode)
    rightType = typeCheckExpr(rightNode)

    if leftType.getDataType() == DataType.integer and rightType.getDataType() == DataType.integer:
        exprNode.setDataType(DataType.boolean)
    else:
        errorMessage = "Error: In Function " + currentFunctName + " Expression " + str(exprNode) \
        + " does not have Integer operands"
        error = ErrorType(errorMessage) 
        addError(error)
        exprNode.setDataType(error)
    return exprNode

def typeCheckIntExpr(exprNode):
    leftNode = exprNode.getLeftOp()
    rightNode = exprNode.getRightOp()

    leftType = typeCheckExpr(leftNode)
    rightType = typeCheckExpr(rightNode)

    if leftType.getDataType() == DataType.integer and rightType.getDataType() == DataType.integer:
        exprNode.setDataType(DataType.integer)
    else:
        errorMessage = "Error: In Function " + currentFunctName + " Expression " + str(exprNode) \
        + " does not have Integer operands"
        error = ErrorType(errorMessage) 
        addError(error)
        exprNode.setDataType(error)
    return exprNode

def typeCheckNotExpr(exprNode):
    opNode = exprNode.getOperand()

    opType = typeCheckExpr(opNode)

    if opType.getDataType() == DataType.boolean:
        exprNode.setDataType(DataType.boolean)
    else:
        errorMessage = "Error: In Function " + currentFunctName + " Expression " + str(exprNode) \
        + " does not have a boolean operand"
        error = ErrorType(errorMessage) 
        addError(error)
        exprNode.setDataType(error)
    return exprNode

def typeCheckNegate(exprNode):
    opNode = exprNode.getOperand()

    opType = typeCheckExpr(opNode)

    if opType.getDataType() == DataType.integer:
        exprNode.setDataType(DataType.integer)
    else:
        errorMessage = "Error: In Function " + currentFunctName + " Expression " + str(exprNode) \
        + " does not have an Integer operand"
        error = ErrorType(errorMessage) 
        addError(error)
        exprNode.setDataType(error)
    return exprNode

def typeCheckIfExpr(exprNode):
    ifNode = exprNode.getIfExpr()
    thenNode = exprNode.getThenExpr()
    elseNode = exprNode.getElseExpr()

    ifType = typeCheckExpr(ifNode)
    thenType = typeCheckExpr(thenNode)
    elseType = typeCheckExpr(elseNode)

    if ifType.getDataType() == DataType.boolean:
        if thenType.getDataType() == elseType.getDataType():
            exprNode.setDataType(thenType.getDataType())
        else:
            exprNode.setDataType(OrType(thenType.getDataType(), elseType.getDataType()))
    else:
        errorMessage = "Error: In Function " + currentFunctName + " If test case " + str(ifNode) \
        + " does not result in a Boolean"
        error = ErrorType(errorMessage) 
        addError(error)
        exprNode.setDataType(error)
    return exprNode

def typeCheckFunctCall(exprNode):
    nameNode = exprNode.getName()
    argsNode = exprNode.getArgs()
    functName = nameNode.getValue()
    
    if functName in symbolTable:
        nameNode.setDataType(symbolTable[functName][tableIndex.dataType()])
        symbolTable[currentFunctName][tableIndex.calls()].append(functName)
        symbolTable[functName][tableIndex.calledBy()].append(currentFunctName)

    else:
        errorMessage = "Error: Function " + currentFunctName + " calls undefined function " + str(functName)
        error = ErrorType(errorMessage) 
        addError(error)
        nameNode.setDataType(error)
        exprNode.setDataType(error)
        return exprNode
    
    argsType = typeCheckArgs(argsNode)
    functionType = nameNode.getDataType()
    paramsType = functionType.getFormalType()
    returnType = functionType.getReturnType()

    if argsType.getDataType() == paramsType:
        exprNode.setDataType(returnType)
    else:
        errorMessage = "Error: In Function " + currentFunctName + " function call " + functName + \
        " has paramaters that do not match those of the function it is calling" 
        error = ErrorType(errorMessage) 
        addError(error)
        exprNode.setDataType(error)
    return exprNode

def typeCheckId(exprNode):
    idName = exprNode.getValue()
    paramTable = symbolTable[currentFunctName][tableIndex.paramDict()]

    if idName in paramTable:
        exprNode.setDataType(paramTable[idName][0])
    else:
        errorMessage = "Error: Identifier " + idName + " in function " + currentFunctName + " is neither a \
            defined function or in " + currentFunctName + " parameter List"
        error = ErrorType(errorMessage) 
        addError(error)
        exprNode.setDataType(error)
    return exprNode

def typeCheckNum(exprNode):
    exprNode.setDataType(DataType.integer)
    return exprNode

def typeCheckBool(exprNode):
    exprNode.setDataType(DataType.boolean)
    return exprNode

def typeCheckArgs(argNode):
    argList = argNode.getArgs()
    typeList = []
    for arg in argList:
        argType = typeCheckExpr(arg)
        typeList.append(argType.getDataType())
    num = len(typeList) 
    argNode.setDataType(tupleType(num,typeList))
    return argNode

def addError(errorMessage):
    errorList.append(errorMessage)

def printTable(table):
    for function in table:
        dataType = table[function][tableIndex.dataType()]
        paramDict = table[function][tableIndex.paramDict()]
        calls = table[function][tableIndex.calls()]
        calledBy = table[function][tableIndex.calledBy()]
        returnType = table[function][tableIndex.returnType()]
        print("Function: " + function)
        print("    DataType: " + str(dataType))
        print("    Parameters: ")
        if paramDict:
            for param in paramDict:
                print("        Id: " + param + " Type: " + str(paramDict[param][0]))
        else:
            print("        None")
        print("    Calls Function:      " + str(calls))
        print("    Called by Functions: " + str(calledBy))
        print("    ReturnType:          " + str(returnType))
        print()
