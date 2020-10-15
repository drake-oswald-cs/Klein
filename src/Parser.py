from enum import Enum
from TokenKlein import Token, TokenType
from Scanner import *
from NodeKlein import *

class NonTerminal(Enum):
    PROGRAM                     = 0
    DEFINITIONS                 = 1
    DEF                         = 2
    FORMALS                     = 3
    NONEMPTYFORMALS             = 4
    NONEMPTYFORMALS_TAIL        = 5
    FORMAL                      = 6
    BODY                        = 7
    TYPE                        = 8
    EXPR                        = 9
    EXPR_TAIL                   = 10
    SIMPLE_EXPR                 = 11
    SIMPLE_EXPR_TAIL            = 12
    TERM                        = 13
    TERM_TAIL                   = 14
    FACTOR                      = 15
    FACTOR_TAIL                 = 16
    ACTUALS                     = 17
    NONEMPTYACTUALS             = 18
    NONEMPTYACT_TAIL            = 19
    LITERAL                     = 20
    PRINT_STATEMENT             = 21

class SemanticActions(Enum):
    makeProgram                 = 0
    makeDefinitions             = 1
    makeDef                     = 2
    makeFormals                 = 3
    makeFormal                  = 4
    makeType                    = 5
    makeBody                    = 6
    makePrint                   = 7
    makeExpr                    = 8
    makeOr                      = 9
    makeAnd                     = 10
    makeLess                    = 11
    makeEq                      = 12
    makePlus                    = 13
    makeMinus                   = 14
    makeTimes                   = 15
    makeDivide                  = 16
    makeNot                     = 17
    makeNegate                  = 18
    makeIf                      = 19
    makeFunctCall               = 20
    makeActuals                 = 21
    makeId                      = 22
    makeNum                     = 23
    makeBool                    = 24
    stopper                     = 25



parseTable = {
    (NonTerminal.PROGRAM, "function") : [NonTerminal.DEFINITIONS, SemanticActions.makeProgram],
    (NonTerminal.PROGRAM, TokenType.eof) : [NonTerminal.DEFINITIONS, SemanticActions.makeProgram],
    (NonTerminal.DEFINITIONS, "function") : [NonTerminal.DEF, NonTerminal.DEFINITIONS],
    (NonTerminal.DEFINITIONS, TokenType.eof) : [SemanticActions.makeDefinitions],
    (NonTerminal.DEF, "function") : [Token(TokenType.keyword, "function"),
        Token(TokenType.identifier, ""), SemanticActions.makeId,
        Token(TokenType.punct, "("), NonTerminal.FORMALS, SemanticActions.makeFormals,
        Token(TokenType.punct, ")"), Token(TokenType.punct, ":"), NonTerminal.TYPE,
        NonTerminal.BODY, SemanticActions.makeDef],
    (NonTerminal.FORMALS, ")") : [],
    (NonTerminal.FORMALS, TokenType.identifier) : [NonTerminal.NONEMPTYFORMALS],
    (NonTerminal.NONEMPTYFORMALS, TokenType.identifier) : [NonTerminal.FORMAL,
        SemanticActions.makeFormal, NonTerminal.NONEMPTYFORMALS_TAIL],
    (NonTerminal.NONEMPTYFORMALS_TAIL, ",") : [Token(TokenType.punct, ","),
        NonTerminal.NONEMPTYFORMALS],
    (NonTerminal.NONEMPTYFORMALS_TAIL, ")") : [],
    (NonTerminal.FORMAL, TokenType.identifier) : [Token(TokenType.identifier, ""),
        SemanticActions.makeId,
        Token(TokenType.punct, ":"), NonTerminal.TYPE],
    (NonTerminal.BODY, "-") : [NonTerminal.EXPR, SemanticActions.makeBody],
    (NonTerminal.BODY, "(") : [NonTerminal.EXPR, SemanticActions.makeBody],
    (NonTerminal.BODY, "if") : [NonTerminal.EXPR, SemanticActions.makeBody],
    (NonTerminal.BODY, "not") : [NonTerminal.EXPR, SemanticActions.makeBody],
    (NonTerminal.BODY, "print") : [NonTerminal.PRINT_STATEMENT ,
        NonTerminal.BODY],
    (NonTerminal.BODY, TokenType.number) : [NonTerminal.EXPR, SemanticActions.makeBody],
    (NonTerminal.BODY, TokenType.boolean) : [NonTerminal.EXPR, SemanticActions.makeBody],
    (NonTerminal.BODY, TokenType.identifier) : [NonTerminal.EXPR, SemanticActions.makeBody],
    (NonTerminal.TYPE, "integer") : [Token(TokenType.keyword, "integer"), SemanticActions.makeType],
    (NonTerminal.TYPE, "boolean") : [Token(TokenType.keyword, "boolean"), SemanticActions.makeType],
    (NonTerminal.EXPR, "-") : [NonTerminal.SIMPLE_EXPR, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR, "(") : [NonTerminal.SIMPLE_EXPR, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR, "if") : [NonTerminal.SIMPLE_EXPR, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR, "not") : [NonTerminal.SIMPLE_EXPR, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR, TokenType.number) : [NonTerminal.SIMPLE_EXPR, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR, TokenType.boolean) : [NonTerminal.SIMPLE_EXPR, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR, TokenType.identifier) : [NonTerminal.SIMPLE_EXPR, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR_TAIL, "<") : [Token(TokenType.operator, "<"), NonTerminal.SIMPLE_EXPR,
        SemanticActions.makeLess, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR_TAIL, "=") : [Token(TokenType.operator, "="),  NonTerminal.SIMPLE_EXPR,
        SemanticActions.makeEq, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR_TAIL, "+") : [],
    (NonTerminal.EXPR_TAIL, "-") : [],
    (NonTerminal.EXPR_TAIL, "*") : [],
    (NonTerminal.EXPR_TAIL, "/") : [],
    (NonTerminal.EXPR_TAIL, ",") : [],
    (NonTerminal.EXPR_TAIL, ")") : [],
    (NonTerminal.EXPR_TAIL, "and") : [],
    (NonTerminal.EXPR_TAIL, "function") : [],
    (NonTerminal.EXPR_TAIL, "then") : [],
    (NonTerminal.EXPR_TAIL, "else") : [],
    (NonTerminal.EXPR_TAIL, TokenType.eof) : [],
    (NonTerminal.SIMPLE_EXPR, "-") : [NonTerminal.TERM, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR, "(") : [NonTerminal.TERM, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR, "if") : [NonTerminal.TERM, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR, "not") : [NonTerminal.TERM, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR, TokenType.number) : [NonTerminal.TERM, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR, TokenType.boolean) : [NonTerminal.TERM, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR, TokenType.identifier) : [NonTerminal.TERM, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR_TAIL, "+") : [Token(TokenType.operator, "+"), NonTerminal.TERM,
        SemanticActions.makePlus, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR_TAIL, "-") : [Token(TokenType.operator, "-"), NonTerminal.TERM,
        SemanticActions.makeMinus, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR_TAIL, "or") : [Token(TokenType.keyword, "or"), NonTerminal.TERM,
        SemanticActions.makeOr, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR_TAIL, "<") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, "=") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, "*") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, "/") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, ",") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, ")") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, "and") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, "function") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, "then") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, "else") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, TokenType.eof) : [],
    (NonTerminal.TERM, "-") : [NonTerminal.FACTOR, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM, "(") : [NonTerminal.FACTOR, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM, "if") : [NonTerminal.FACTOR, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM, "not") : [NonTerminal.FACTOR, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM, TokenType.number) : [NonTerminal.FACTOR, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM, TokenType.boolean) : [NonTerminal.FACTOR, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM, TokenType.identifier) : [NonTerminal.FACTOR, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM_TAIL, "*") : [Token(TokenType.operator, "*"), NonTerminal.FACTOR,
        SemanticActions.makeTimes, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM_TAIL, "/") : [Token(TokenType.operator, "/"), NonTerminal.FACTOR,
        SemanticActions.makeDivide, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM_TAIL, "and") : [Token(TokenType.keyword, "and"), NonTerminal.FACTOR,
        SemanticActions.makeAnd, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM_TAIL, "<") : [],
    (NonTerminal.TERM_TAIL, "+") : [],
    (NonTerminal.TERM_TAIL, "-") : [],
    (NonTerminal.TERM_TAIL, ",") : [],
    (NonTerminal.TERM_TAIL, ")") : [],
    (NonTerminal.TERM_TAIL, "=") : [],
    (NonTerminal.TERM_TAIL, "or") : [],
    (NonTerminal.TERM_TAIL, "function") : [],
    (NonTerminal.TERM_TAIL, "then") : [],
    (NonTerminal.TERM_TAIL, "else") : [],
    (NonTerminal.TERM_TAIL, TokenType.eof) : [],
    (NonTerminal.FACTOR, "-") : [Token(TokenType.operator, "-"), NonTerminal.FACTOR,
        SemanticActions.makeNegate],
    (NonTerminal.FACTOR, "not") : [Token(TokenType.keyword, "not"), NonTerminal.FACTOR,
        SemanticActions.makeNot],
    (NonTerminal.FACTOR, "(") : [Token(TokenType.punct, "("), NonTerminal.EXPR,
        Token(TokenType.punct, ")") ],
    (NonTerminal.FACTOR, "if") : [Token(TokenType.keyword, "if"), NonTerminal.EXPR,
        Token(TokenType.keyword, "then"), NonTerminal.EXPR, Token(TokenType.keyword,
        "else"), NonTerminal.EXPR, SemanticActions.makeIf],
    (NonTerminal.FACTOR, TokenType.number) : [NonTerminal.LITERAL],
    (NonTerminal.FACTOR, TokenType.boolean) : [NonTerminal.LITERAL],
    (NonTerminal.FACTOR, TokenType.identifier) : [Token(TokenType.identifier,""),
        SemanticActions.makeId, NonTerminal.FACTOR_TAIL],
    (NonTerminal.FACTOR_TAIL, "(") : [Token(TokenType.punct, "("), SemanticActions.stopper, NonTerminal.ACTUALS,
        SemanticActions.makeActuals, Token(TokenType.punct, ")"), SemanticActions.makeFunctCall],
    (NonTerminal.FACTOR_TAIL, "<") : [],
    (NonTerminal.FACTOR_TAIL, "=") : [],
    (NonTerminal.FACTOR_TAIL, "+") : [],
    (NonTerminal.FACTOR_TAIL, "-") : [],
    (NonTerminal.FACTOR_TAIL, "*") : [],
    (NonTerminal.FACTOR_TAIL, "/") : [],
    (NonTerminal.FACTOR_TAIL, ",") : [],
    (NonTerminal.FACTOR_TAIL, ")") : [],
    (NonTerminal.FACTOR_TAIL, "and") : [],
    (NonTerminal.FACTOR_TAIL, "or") : [],
    (NonTerminal.FACTOR_TAIL, "function") : [],
    (NonTerminal.FACTOR_TAIL, "then") : [],
    (NonTerminal.FACTOR_TAIL, "else") : [],
    (NonTerminal.FACTOR_TAIL, TokenType.eof) : [],
    (NonTerminal.ACTUALS, "-") : [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, "(") : [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, "if") : [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, "not") : [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, TokenType.number) : [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, TokenType.boolean) : [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, TokenType.identifier) : [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACTUALS, "-") : [NonTerminal.EXPR, NonTerminal.NONEMPTYACT_TAIL],
    (NonTerminal.NONEMPTYACTUALS, "(") : [NonTerminal.EXPR, NonTerminal.NONEMPTYACT_TAIL],
    (NonTerminal.NONEMPTYACTUALS, "if") : [NonTerminal.EXPR, NonTerminal.NONEMPTYACT_TAIL],
    (NonTerminal.NONEMPTYACTUALS, "not") : [NonTerminal.EXPR, NonTerminal.NONEMPTYACT_TAIL],
    (NonTerminal.NONEMPTYACTUALS, TokenType.number) : [NonTerminal.EXPR, NonTerminal.NONEMPTYACT_TAIL],
    (NonTerminal.NONEMPTYACTUALS, TokenType.boolean) : [NonTerminal.EXPR, NonTerminal.NONEMPTYACT_TAIL],
    (NonTerminal.NONEMPTYACTUALS, TokenType.identifier) : [NonTerminal.EXPR,
        NonTerminal.NONEMPTYACT_TAIL],
    (NonTerminal.NONEMPTYACT_TAIL, ",") : [Token(TokenType.punct, ","),
        NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACT_TAIL, ")") : [],
    (NonTerminal.LITERAL, TokenType.number) : [Token(TokenType.number, 0), SemanticActions.makeNum],
    (NonTerminal.LITERAL, TokenType.boolean) : [Token(TokenType.boolean, "true"),
        SemanticActions.makeBool],
    (NonTerminal.PRINT_STATEMENT, "print") : [Token(TokenType.identifier,"print"),
        Token(TokenType.punct, "("), NonTerminal.EXPR, SemanticActions.makePrint, Token(TokenType.punct, ")")]
}







def top(stack):
    return stack[-1]

def pop(stack):
    return stack.pop()

def pushRule(rule, stack):
    for element in reversed(rule):
        stack.append(element)

def push(stack, node):
    stack.append(node)



class Parser:

    def __init__(self, scanner):
      self.scanner = scanner

    def parse(self):
        parseStack = []
        semanticStack = []
        lastValue = ""
        pushRule( [ NonTerminal.PROGRAM, Token(TokenType.eof) ], parseStack)
        while parseStack:
#            print("Parse Stack: " + str(parseStack))
            tos = top(parseStack) 
            if isinstance(tos, Token):
                token = self.scanner.next()
                # Checking if values are the same. Used punctuations, operators, and keywords
                if needValueCheck(tos):
                    if tos.value() == token.value():
                        pop(parseStack)
                    else:
                        errorMessage = 'Error line {}: Expected  {}  but received {}'
                        raise TypeError(errorMessage.format(token.getLineNumber(), tos.value(), token.value()))
                # Checking if an identifier is print. Used in the print-statement rule.
                elif token.value() == "print":
                    if tos.value() == token.value():
                        pop(parseStack)
                    else:
                        errorMessage = 'Error line {}: Expected  {}  but received {}'
                        raise TypeError(errorMessage.format(token.getLineNumber(), tos.value(), token.value()))
                # Checking if tokenTypes are the same. Used for Numbers, EOF, Booleans, and identifiers that are not print.
                elif tos.getTokenType() == token.getTokenType():
                    pop(parseStack)
                else:
                    errorMessage = 'Error line {}: Expected  {}  but received {}'
                    raise TypeError(errorMessage.format(token.getLineNumber(), tos.getTokenType(), token.getTokenType()))
                lastValue = token.value()

            elif isinstance(tos, NonTerminal):
                token = self.scanner.peek()
                if needValueCheck(token):
                    rule = parseTable.get((tos, token.value()))
                elif token.value() == "print":
                    rule = parseTable.get((tos, "print"))
                else:
                    rule = parseTable.get((tos,token.getTokenType()))

                if rule is not None:
                    pop(parseStack)
                    pushRule(rule, parseStack)
                else:
                    errorMessage = 'Error line {}: {} cannot be expanded on by {}'
                    raise TypeError(errorMessage.format(token.getLineNumber(), tos, token))
            elif isinstance(tos, SemanticActions):
                pop(parseStack)

                semanticStack = semanticAction(tos, semanticStack, lastValue)

            else:
                errorMessage = 'invalid item on stack: {}'
                raise TypeError(errorMessage.format(tos))

        # Checking if there is more tokens after the program was completed.
        if not token.isEof():
            errorMessage = 'Error: unexpected token at end: {}'
            raise TypeError(errorMessage.format(token))

        if len(semanticStack) != 1:
            errorMessage = 'Error: too many nodes left on the semantic stack: {}'
            raise TypeError(errorMessage.format(semanticStack))

        programNode = semanticStack[0]
        return programNode

def needValueCheck(aToken):
    if aToken.getTokenType() == TokenType.punct or \
    aToken.getTokenType() == TokenType.operator or \
    aToken.getTokenType() == TokenType.keyword:
        return True
    else:
        return False

def testParser(klienProgram):
    file = open(klienProgram, 'r')
    program = file.read()
    demoScanner = Scanner(program)
    demoScanner.scan(program)
    parser = Parser(demoScanner)
    return parser.parse()


def semanticAction(anAction, stack, value = ""):
    if anAction == SemanticActions.makeProgram:
        node = pop(stack)
        newNode = ProgramNode(node)

    elif anAction == SemanticActions.makeDefinitions:
        defList = []
        tos = top(stack)
        while stack:
            tos = top(stack)
            if tos.getNodeType() == NodeType.Def:
                defNode = pop(stack)
                defList.append(defNode)
            else:
                break
        newNode = DefinitionsNode(defList)

    elif anAction == SemanticActions.makeDef:
        body = pop(stack)
        aType = pop(stack)
        formals = pop(stack)
        identifier = pop(stack)
        newNode = DefNode(identifier, formals, aType, body)

    elif anAction == SemanticActions.makeFormals:
        formalsList = []
        tos = top(stack)
        while tos.getNodeType() == NodeType.Formal:
            formalNode = pop(stack)
            formalsList.append(formalNode)
            tos = top(stack)
        newNode = FormalsNode(formalsList)

    elif anAction == SemanticActions.makeFormal:
        aType = pop(stack)
        identifier = pop(stack)
        newNode = FormalNode(identifier, aType)

    elif anAction == SemanticActions.makeType:
        newNode = TypeNode(value)

    elif anAction == SemanticActions.makeBody:
        printList = []
        expr = pop(stack)
        tos = top(stack)
        while tos.getNodeType() == NodeType.Print:
            printNode = pop(stack)
            printList.append(printNode)
            tos = top(stack)
        printList.reverse()
        newNode = BodyNode(printList, expr)

    elif anAction == SemanticActions.makePrint:
        node = pop(stack)
        newNode = PrintNode(node)

    elif anAction == SemanticActions.makeOr:
        right = pop(stack)
        left = pop(stack)
        newNode = OrNode(left, right)

    elif anAction == SemanticActions.makeAnd:
        right = pop(stack)
        left = pop(stack)
        newNode = AndNode(left, right)

    elif anAction == SemanticActions.makeLess:
        right = pop(stack)
        left = pop(stack)
        newNode = LessThanNode(left, right)

    elif anAction == SemanticActions.makeEq:
        right = pop(stack)
        left = pop(stack)
        newNode = EqualNode(left, right)

    elif anAction == SemanticActions.makePlus:
        right = pop(stack)
        left = pop(stack)
        newNode = PlusNode(left, right)

    elif anAction == SemanticActions.makeMinus:
        right = pop(stack)
        left = pop(stack)
        newNode = MinusNode(left, right)

    elif anAction == SemanticActions.makeTimes:
        right = pop(stack)
        left = pop(stack)
        newNode = TimesNode(left, right)

    elif anAction == SemanticActions.makeDivide:
        right = pop(stack)
        left = pop(stack)
        newNode = DivideNode(left, right)

    elif anAction == SemanticActions.makeNot:
        node = pop(stack)
        newNode = NotNode(node)

    elif anAction == SemanticActions.makeNegate:
        node = pop(stack)
        newNode = NegateNode(node)

    elif anAction == SemanticActions.makeIf:
        elseExpr = pop(stack)
        thenExpr = pop(stack)
        ifExpr = pop(stack)
        newNode = IfNode(ifExpr, thenExpr, elseExpr)

    elif anAction == SemanticActions.makeFunctCall:
        actuals = pop(stack)
        identifier = pop(stack)
        newNode = FunctCallNode(identifier, actuals)

    elif anAction == SemanticActions.makeId:
        newNode = IdentifierNode(value)

    elif anAction == SemanticActions.makeActuals:
        actualsList = []
        tos = top(stack)
        while isinstance(tos, ExprNode):
            exprNode = pop(stack)
            actualsList.append(exprNode)
            tos = top(stack)
        if tos.getNodeType() == NodeType.stopper:
            pop(stack)

        newNode = ActualsNode(actualsList)

    elif anAction == SemanticActions.makeNum:
        newNode = NumberNode(str(value))

    elif anAction == SemanticActions.makeBool:
        newNode = BooleanNode(value)

    elif anAction == SemanticActions.stopper:
        newNode = StopperNode()

    else:
        errorMessage = 'Error: semantic action {} not found'
        raise TypeError(errorMessage.format(anAction))

    push(stack, newNode)
    
    return stack
        
if __name__ == '__main__':
    try:
        testParser('klein-programs/sieve.kln')
    except TypeError as err:
        print(err)
        
    except ValueError as err:
        print(err)