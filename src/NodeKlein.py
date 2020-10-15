from enum import Enum

class NodeType(Enum):
    Program             = 0
    Definitions         = 1
    Def                 = 2
    Formals             = 3
    Formal              = 4
    Type                = 5
    Body                = 6
    Print               = 7
    Expr                = 8
    Or                  = 9
    And                 = 10
    LessThan            = 11
    Equal               = 12
    Plus                = 13
    Minus               = 14
    Times               = 15
    Divide              = 16
    Not                 = 17
    Negate              = 18
    If                  = 19
    Id                  = 20
    Actuals             = 21
    Num                 = 22
    Bool                = 23
    FunctCall           = 24
    stopper             = 25

class Node(object):
    pass

class ExprNode(Node):
    pass

class ProgramNode(Node):
    def __init__(self, definitions):
        self.definitions = definitions
        self.type = NodeType.Program
        self.dataType = None

    def getDefinitions(self):
        return self.definitions
    
    def getNodeType(self):
        return self.type
    
    def prettyPrint(self):
        print("Program")
        self.definitions.prettyPrint()

    def __str__(self):
        return str(self.definitions)

class DefinitionsNode(Node):
    def __init__(self, definitions):
        self.definitions = definitions
        self.type = NodeType.Definitions
        self.dataType = None

    def getDefinitions(self):
        return self.definitions
    
    def getNodeType(self):
        return self.type
    
    def prettyPrint(self):
        for funct in reversed(self.definitions):
            print(funct.prettyPrint())

    def __str__(self):
        word = ''
        for funct in self.definitions:
           word += str(funct)
        return word

class DefNode(Node):
    def __init__(self, name, parameters, returnType, body):
        self.name = name
        self.parameters = parameters
        self.returnType = returnType
        self.body = body
        self.type = NodeType.Def
        self.dataType = None

    def getName(self):
        return self.name 
    
    def getParameters(self):
        return self.parameters
    
    def getReturnType(self):
        return self.returnType

    def getBody(self):
        return self.body

    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        result = ("    Name: " + self.name.prettyPrint() + "\n")
        result = result + "    " + self.parameters.prettyPrint() + "\n"
        result = result + "    " + self.returnType.prettyPrint() + "\n"
        result = result + "    " + self.body.prettyPrint() + "\n"
        return result

    def __str__(self):
        return "Function " + str(self.name) + " Parameters: " + str(self.parameters) + " Type " + self.returnType + " Body " + str(self.body)
    
class FormalsNode(Node):
    def __init__(self, formals):
        self.formals = formals
        self.type = NodeType.Formals
        self.dataType = None
 
    def getParameters(self):
        return self.formals
    
    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        myList = []
        for formal in self.formals:
            myList.append(formal.prettyPrint())
        myList.reverse()
        return "Parameters: " + str(myList)

    def __str__(self):
        word = ''
        for arg in self.formals:
           word += str(arg)
        return word
    
class FormalNode(Node):
    def __init__(self, name, dataType):
        self.name = name
        self.type = NodeType.Formal
        self.dataTypeNode = dataType
        self.dataType = None
    
    def getName(self):
        return self.name

    def getDataTypeNode(self):
        return self.dataTypeNode
    
    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        return self.name.prettyPrint() + " " + self.dataTypeNode.prettyPrint()

    def __str__(self):
        return str(self.name) + " : " + str(self.dataType)

class TypeNode(Node):
    def __init__(self, dataType):
        self.dataTypeString = dataType
        self.type = NodeType.Type
        self.dataType = None

    def getDataTypeString(self):
        return self.dataTypeString
    
    def getNodeType(self):
        return self.getNodeType
    
    def isBoolean(self):
        return self.dataTypeString == "boolean"

    def isInteger(self):
        return self.dataTypeString == "integer"

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        return "Type: " + self.dataTypeString

    def __str__(self):
        return self.dataType

class BodyNode(Node):
    def __init__(self, printList, expr):
        self.printList = printList
        self.expr = expr
        self.type = NodeType.Body
        self.dataType = None

    def getPrintStatements(self):
        return self.printList

    def getExpr(self):
        return self.expr

    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        tempList = []
        for printStatement in self.printList:
            tempList.append(printStatement.prettyPrint())
        result = "Body" + "\n"
        result = result + "    " + "    Print Statements: " + str(tempList) + "\n"
        result = result + "    " + "    Body Expr: " + self.expr.prettyPrint() + "\n"
        return result
    
    def __str__(self):
        word = ''
        for statement in self.printList:
           word += str(statement)
        return word + str(self.expr)

class PrintNode(Node):
    def __init__(self, expr):
        self.expr = expr
        self.type = NodeType.Print
        self.dataType = None

    def getExpr(self):
        return self.expr

    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        return self.expr.prettyPrint()

    def __str__(self):
        return "Print " + str(self.expr)

class OrNode(ExprNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.type = NodeType.Or
        self.dataType = None

    def getLeftOp(self):
        return self.left
    
    def getRightOp(self):
        return self.right

    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self): 
        return "(" + self.left.prettyPrint() + " or " + self.right.prettyPrint() + ")"

    def __str__(self):
        return str(self.left) + " or " + str(self.right)

class AndNode(ExprNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.type = NodeType.And
        self.dataType = None

    def getLeftOp(self):
        return self.left
    
    def getRightOp(self):
        return self.right

    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        return "(" + self.left.prettyPrint() + " and " + self.right.prettyPrint() + ")"

    def __str__(self):
        return str(self.left) + " and " + str(self.right)

class LessThanNode(ExprNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.type = NodeType.LessThan
        self.dataType = None

    def getLeftOp(self):
        return self.left
    
    def getRightOp(self):
        return self.right

    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        return "(" + self.left.prettyPrint() + " < " + self.right.prettyPrint() + ")"

    def __str__(self):
        return str(self.left) + " < " + str(self.right)

class EqualNode(ExprNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.type = NodeType.Equal
        self.dataType = None

    def getLeftOp(self):
        return self.left
    
    def getRightOp(self):
        return self.right

    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        return "(" + self.left.prettyPrint() + " = " + self.right.prettyPrint() + ")"

    def __str__(self):
        return str(self.left) + " = " + str(self.right)

class PlusNode(ExprNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.type = NodeType.Plus
        self.dataType = None

    def getLeftOp(self):
        return self.left
    
    def getRightOp(self):
        return self.right

    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        return "(" + self.left.prettyPrint() + " + " + self.right.prettyPrint() + ")"

    def __str__(self):
        return str(self.left) + " + " + str(self.right)

class MinusNode(ExprNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.type = NodeType.Minus
        self.dataType = None

    def getLeftOp(self):
        return self.left
    
    def getRightOp(self):
        return self.right

    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        return "(" + self.left.prettyPrint() + " - " + self.right.prettyPrint() + ")"

    def __str__(self):
        return str(self.left) + " - " + str(self.right)

class TimesNode(ExprNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.type = NodeType.Times
        self.dataType = None

    def getLeftOp(self):
        return self.left
    
    def getRightOp(self):
        return self.right

    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        return "(" + self.left.prettyPrint() + " * " + self.right.prettyPrint() + ")"

    def __str__(self):
        return str(self.left) + " * " + str(self.right)

class DivideNode(ExprNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.type = NodeType.Divide
        self.dataType = None

    def getLeftOp(self):
        return self.left
    
    def getRightOp(self):
        return self.right

    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        return "(" + self.left.prettyPrint() + " / " + self.right.prettyPrint() + ")"
    
    def __str__(self):
        return str(self.left) + " / " + str(self.right)

class NotNode(ExprNode):
    def __init__(self, operand):
        self.operand = operand
        self.type = NodeType.Not
        self.dataType = None

    def getOperand(self):
        return self.operand
    
    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        return "(" + "not " + self.operand.prettyPrint() + ")"

    def __str__(self):
        return "not " + str(self.operand)

class NegateNode(ExprNode):
    def __init__(self, operand):
        self.operand = operand
        self.type = NodeType.Negate
        self.dataType = None

    def getOperand(self):
        return self.operand
    
    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        return "(" + "- " + self.operand.prettyPrint() + ")"

    def __str__(self):
        return "- " + str(self.operand)

class IfNode(ExprNode):
    def __init__(self, ifExpr, thenExpr, elseExpr):
        self.ifExpr = ifExpr
        self.thenExpr = thenExpr
        self.elseExpr = elseExpr
        self.type = NodeType.If
        self.dataType = None

    def getIfExpr(self):
        return self.ifExpr
    
    def getThenExpr(self):
        return self.thenExpr

    def getElseExpr(self):
        return self.elseExpr

    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        result =  "If: " + self.ifExpr.prettyPrint() 
        result = result + " Then: " + self.thenExpr.prettyPrint() 
        result = result + " Else: " + self.elseExpr.prettyPrint() 
        return result
    
    def __str__(self):
        return "if " + str(self.ifExpr) + " then " + str(self.thenExpr) + " else " + str(self.elseExpr)


class FunctCallNode(ExprNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.type = NodeType.FunctCall
        self.dataType = None

    def getName(self):
        return self.name

    def getArgs(self):
        return self.args

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def getNodeType(self):
        return self.type

    def prettyPrint(self):
        return "(" + "Name: " + self.name.prettyPrint() + " " + self.args.prettyPrint() + ")"

    def __str__(self):
        return str(self.name) + " " + str(self.args)

class IdentifierNode(ExprNode):
    def __init__(self, value):
        self.value = value
        self.type = NodeType.Id
        self.dataType = None

    def getValue(self):
        return self.value
    
    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def getNodeType(self):
        return self.type

    def prettyPrint(self):
        return self.value

    def __str__(self):
        return self.value

class NumberNode(ExprNode):
    def __init__(self, value):
        self.value = value
        self.type = NodeType.Num
        self.dataType = None

    def getValue(self):
        return self.value
    
    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def getNodeType(self):
        return self.type

    def prettyPrint(self):
        return str(self.value)


class BooleanNode(ExprNode):
    def __init__(self, value):
        self.value = value
        self.type = NodeType.Bool
        self.dataType = None

    def getValue(self):
        return self.value

    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType

    def prettyPrint(self):
        return self.value
    
    def __str__(self):
        return self.value

class ActualsNode(Node):
    def __init__(self, args):
        self.args = args
        self.type = NodeType.Bool
        self.dataType = None

    def getArgs(self):
        return self.args

    def getNodeType(self):
        return self.type

    def getDataType(self):
        return self.dataType

    def setDataType(self, dataType):
        self.dataType = dataType
    
    def prettyPrint(self):
        myList = []
        for expr in self.args:
            myList.append(expr.prettyPrint())
        myList.reverse()
        return "Args: " + str(myList)

    def __str__(self):
        word = ''
        for arg in self.args:
           word += str(arg)
        return word

class StopperNode(Node):
    def __init__(self):
        self.type = NodeType.stopper

    def getNodeType(self):
        return self.type
    
    def prettyPrint(self):
        return "Stopper"