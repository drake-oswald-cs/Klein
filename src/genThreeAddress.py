from enum import Enum
from NodeKlein import *
from TypeChecker import TableIndex

class op(Enum):
    PLUS            = 0
    MINUS           = 1
    MULT            = 2
    DIVIDE          = 3
    AND             = 4
    OR              = 5
    NEGATE          = 6
    LABEL           = 7
    COPY            = 8
    IF_NOT          = 9
    EMPTY           = 10
    RETURN          = 11
    ENTRY           = 12
    EXIT            = 13
    GOTO            = 14
    CALL            = 15
    BEGIN_CALL      = 16
    PARAM           = 17
    RECIEVE         = 18
    PRINT           = 19
    LESS            = 20
    EQUAL           = 21
    NOT             = 22
    ID              = 23
    NUM             = 24
    BOOL            = 25
    STORE           = 26
    LOAD            = 27
    SETARG          = 28

class tempObject():
    def __init__(self, place, code):
        self.place = place
        self.code = code

    def getPlace(self):
        return self.place
    
    def getCode(self):
        return self.code

threeAddress = []
tempCount = 0
labelCount = 0
order = 1
functionName = ""
symbolTable = {}
tableIndex = TableIndex()
startLabel = ""
def genThreeAddress (ast,aSymbolTable):
    global order
    global functionName
    global symbolTable
    symbolTable = aSymbolTable
    definitionsNode = ast.getDefinitions()
    listOfDefs = definitionsNode.getDefinitions()
    for function in listOfDefs:
        functionNameNode = function.getName()
        functionName = functionNameNode.getValue()
        add(op.ENTRY, op.EMPTY, op.EMPTY, functionName)
        bodyNode = function.getBody()
        order = 1
        result = genBody(bodyNode)
        add(op.RETURN, op.EMPTY, op.EMPTY, result)
        add(op.EXIT, op.EMPTY, op.EMPTY, functionName)
    return threeAddress, symbolTable

def genBody(bodyNode):
    global functionName
    global symbolTable
    global startLabel
    if symbolTable[functionName][tableIndex.tailRecursive()] == True:
        startLabel = makeLabel()
        add(op.LABEL, op.EMPTY, op.EMPTY, startLabel)
    printList = bodyNode.getPrintStatements()
    exprNode = bodyNode.getExpr()
    genPrint(printList)
    result = genExpr(exprNode)
    return result

def genPrint(printList):
    for printNode in printList:
        printExpr = printNode.getExpr()
        temp = genExpr(printExpr)
        add(op.PRINT, op.EMPTY, op.EMPTY, temp)

def genExpr(expr, tempVariable = None):
    exprNodeType = expr.getNodeType() 
    if exprNodeType == NodeType.Or:
        temp = genBinaryExpr(expr, op.OR, tempVariable)
    elif exprNodeType == NodeType.And:
        temp = genBinaryExpr(expr, op.AND, tempVariable)
    elif exprNodeType == NodeType.LessThan:
        temp = genBinaryExpr(expr, op.LESS, tempVariable)
    elif exprNodeType == NodeType.Equal:
        temp = genBinaryExpr(expr, op.EQUAL, tempVariable)
    elif exprNodeType == NodeType.Plus:
        temp = genBinaryExpr(expr, op.PLUS, tempVariable)
    elif exprNodeType == NodeType.Minus:
        temp = genBinaryExpr(expr, op.MINUS, tempVariable)
    elif exprNodeType == NodeType.Times:
        temp = genBinaryExpr(expr, op.MULT, tempVariable)
    elif exprNodeType == NodeType.Divide:
        temp = genBinaryExpr(expr, op.DIVIDE, tempVariable)
    elif exprNodeType == NodeType.Not:
        temp = genUnaryExpr(expr, op.NOT, tempVariable)
    elif exprNodeType == NodeType.Negate:
        temp = genUnaryExpr(expr, op.NEGATE, tempVariable)
    elif exprNodeType == NodeType.If:
        temp = genIf(expr, tempVariable)
    elif exprNodeType == NodeType.FunctCall:
        temp = genFunctCall(expr, tempVariable)
    elif exprNodeType == NodeType.Id:
        temp = genID(expr, tempVariable)
    elif exprNodeType == NodeType.Num:
        temp = genNum(expr, tempVariable)
    elif exprNodeType == NodeType.Bool:
        temp = genBool(expr, tempVariable)
    else:
        raise TypeError("Expression Type {} is not valid".format(exprNodeType))
    return temp

def genBinaryExpr(expr, operator, result):
    leftExpr = expr.getLeftOp()
    rightExpr = expr.getRightOp()

    leftPlace = genExpr(leftExpr)
    rightPlace = genExpr(rightExpr)
    if result == None:
        result = makeTemp()

    add(operator, leftPlace, rightPlace, result)
    return result

def genUnaryExpr(expr, operator, result):
    opExpr = expr.getOperand()
    opPlace = genExpr(opExpr)
    if result == None:
        result = makeTemp()

    add(operator, opPlace, op.EMPTY, result)
    return result

def genIf(expr, result):
    ifNode = expr.getIfExpr()
    thenNode = expr.getThenExpr()
    elseNode = expr.getElseExpr()

    if result == None:
        result = makeTemp()
    elseLabel = makeLabel()
    endIfLabel = makeLabel()
    ifPlace = genExpr(ifNode)
    add(op.STORE, op.EMPTY, op.EMPTY, ifPlace)
    add(op.IF_NOT, ifPlace, op.EMPTY, elseLabel)
    result = genExpr(thenNode, result)
    add(op.STORE, op.EMPTY, op.EMPTY, result)
    add(op.GOTO, op.EMPTY, op.EMPTY, endIfLabel)
    add(op.LABEL, op.EMPTY, op.EMPTY, elseLabel)
    result = genExpr(elseNode, result)
    if symbolTable[functionName][tableIndex.tailRecursive()] == False:
        add(op.STORE, op.EMPTY, op.EMPTY, result)
    add(op.LABEL, op.EMPTY, op.EMPTY, endIfLabel)
    add(op.LOAD, op.EMPTY, op.EMPTY, result)
    return result

def genFunctCall(expr, result):
    nameNode = expr.getName()
    argsNode = expr.getArgs()
    argList = argsNode.getArgs()
    functName = nameNode.getValue()
    argTemps = []
    argList.reverse()
    # Generate code for each arg
    for arg in argList:
        temp = genExpr(arg)
        argTemps.append(temp)
    if symbolTable[functionName][tableIndex.tailRecursive()] == True and functionName == functName:
        count = len(argTemps)
        for arg in argTemps:
            add(op.SETARG, arg, op.EMPTY, count)
            count -= 1
        add(op.GOTO, op.EMPTY, op.EMPTY, startLabel)

        return result
    # Gen PARAM for each arg
    for arg in argTemps:
        add(op.PARAM, op.EMPTY, op.EMPTY, arg)

    if result == None:
        result = makeTemp()

    count = len(argTemps)

    add(op.CALL, functName, count, result)
    return result

def genID(expr, result):
    idValue = expr.getValue()

    if result == None:
        result = makeTemp()
    add(op.ID, idValue, op.EMPTY, result)
    return result

def genNum(expr, result):
    numValue = expr.getValue()

    if result == None:
        result = makeTemp()
    add(op.NUM, numValue, op.EMPTY, result)
    return result

def genBool(expr, result):
    boolValue = expr.getValue()

    if result == None:
        result = makeTemp()
    add(op.BOOL, boolValue, op.EMPTY, result)
    return result

def makeTemp():
    global tempCount
    global order
    global functionName
    global symbolTable
    global tableIndex
    tempDict = symbolTable[functionName][tableIndex.tempDict()]
    temp = "t" + str(tempCount)
    tempDict[temp] = order
    order += 1
    tempCount += 1
    return temp

def makeLabel():
    global labelCount
    label = "L" + str(labelCount)
    labelCount += 1
    return label

def add(operator, arg1, arg2, result):
    threeAddress.append([operator,arg1,arg2,result])

def prettyPrint(addressList):
    for line in addressList:
        operator = line[0]
        arg1 = line[1]
        arg2 = line[2]
        result = line[3]
        if operator == op.AND:
            print("{} := {} AND {}".format(result, arg1, arg2))
        elif operator == op.OR:
            print("{} := {} OR {}".format(result, arg1, arg2))
        elif operator == op.PLUS:
            print("{} := {} + {}".format(result, arg1, arg2))
        elif operator == op.MINUS:
            print("{} := {} - {}".format(result, arg1, arg2))
        elif operator == op.MULT:
            print("{} := {} * {}".format(result, arg1, arg2))
        elif operator == op.DIVIDE:
            print("{} := {} / {}".format(result, arg1, arg2))
        elif operator == op.NEGATE:
            print("{} := - {}".format(result, arg1))
        elif operator == op.NOT:
            print("{} := Not {}".format(result, arg1))
        elif operator == op.LESS:
            print("{} := {} < {}".format(result, arg1, arg2))
        elif operator == op.EQUAL:
            print("{} := {} = {}".format(result, arg1, arg2))
        elif operator == op.ID:
            print("{} := {}".format(result, arg1))
        elif operator == op.NUM:
            print("{} := {}".format(result, arg1))
        elif operator == op.BOOL:
            print("{} := {}".format(result, arg1))
        elif operator == op.ENTRY:
            print("ENTRY {}".format(result))
        elif operator == op.EXIT:
            print("EXIT {}".format(result))
        elif operator == op.RETURN:
            print("RETURN {}".format(result))
        elif operator == op.PRINT:
            print("PRINT {}".format(result))
        elif operator == op.PARAM:
            print("PARAM {}".format(result))
        elif operator == op.CALL:
            print("{} := CALL {} {}".format(result, arg1, arg2))
        elif operator == op.IF_NOT:
            print("IF_NOT {} GOTO {}".format(arg1, result))
        elif operator == op.LABEL:
            print("LABEL {}".format(result))
        elif operator == op.GOTO:
            print("GOTO {}".format(result))
        elif operator == op.STORE:
            print("STORE {}".format(result))
        elif operator == op.LOAD:
            print("LOAD {}".format(result))
        elif operator == op.SETARG:
            print("SET ARG{} = {}".format(result,arg1))
        else:
            raise TypeError("op Type {} is not valid".format(operator))


