#!/usr/bin/env python

import sys
sys.path.append("system_rdl")

from antlr4 import *
from system_rdl import SystemRDLLexer
from system_rdl import SystemRDLParser
 
def main(argv):
    input_stream = FileStream(argv[1])
    lexer = SystemRDLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SystemRDLParser(stream)
    tree = parser.startRule()
 
if __name__ == '__main__':
    main(sys.argv)