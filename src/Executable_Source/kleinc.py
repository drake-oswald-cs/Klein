#!/usr/bin/env python3

from enum import Enum
from TokenKlein import Token, TokenType
from Scanner import *
from NodeKlein import *
from Parser import *
from TypeChecker import *
from CodeGenerator import *

from sys import argv

try:
    kleinProgram = argv[1]
except:
    print("No Klein program given")
    raise SystemExit(0)


try:
    if ".kln" not in kleinProgram:
        kleinProgram += ".kln"
    file = open(kleinProgram, 'r')
    program = file.read()
except:
    print("No Klein Program with name: " + str(kleinProgram))
    raise SystemExit(0)

try:
    scanner = Scanner(program)
    scanner.scan(program)
    parser = Parser(scanner)
    programNode = parser.parse()
    symbolTable, ast = typeCheck(programNode)
    newFile = kleinProgram[:-4] + ".tm"
#    newFile = "test.tm"
    codeGen = CodeGenerator(ast, symbolTable, newFile)
    codeGen.GenerateTM()
except TypeError as err:
    print(err)
        
except ValueError as err:
    print(err)