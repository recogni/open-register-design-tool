#!/usr/bin/env python

""" Usage:
    
    $ python3.7 grammar_to_struct.py <path/to/file.rdl>

    This will simply store and emit the JSON variants of all encountered:
    a. ENUMS
    b. FIELDSTRUCTS (nested with)
        b1. Fields
        b2. Explicit fields of other types

    TODO: ???
"""
import sys
sys.path.append("system_rdl")

from antlr4 import *
from system_rdl.SystemRDLLexer import SystemRDLLexer
from system_rdl.SystemRDLParser import SystemRDLParser
from system_rdl.SystemRDLListener import SystemRDLListener

################################################################################

def panic(msg):
    print("Fatal error: ", msg)
    sys.exit(1)

def warn(msg):
    print("Warning: ", msg)

################################################################################

#
#   Context constants
#

CTXT_CLEAR                       = 0x00
CTXT_IN_COMPONENT_FIELD_STRUCT   = 0x01
CTXT_IN_COMPONENT_FIELD          = 0x02
CTXT_IN_COMPONENT_FIELD_EXPLICIT = 0x04

CTXT_IN_ENUM                     = 0x10
CTXT_IN_ENUM_ENTRY               = 0x20

CTXT_IN_COMPONENT = CTXT_IN_COMPONENT_FIELD | CTXT_IN_COMPONENT_FIELD_STRUCT | CTXT_IN_COMPONENT_FIELD_EXPLICIT

################################################################################

#
#   Context primitives
#

def new_enum():
    return {
        "id": None,
        "width": 0,
        "values": [],
    }

def new_enum_entry():
    return {
        "name": None,
        "value": None,
        "desc": None,
    }

def new_struct():
    return {
        "id": None,
        "desc": None,
        "fields": [],
    }

def new_field():
    return {
        "id": None,
        "desc": None,
        "type": None
    }

################################################################################

#
#   Custom listener for tree walking
#

class CustomListener(SystemRDLListener):
    
    # Keep track of when we are in an enum, struct or other fields.
    context = 0

    enums = []
    structs = []

    # Current enums, structs and fields
    _enum = None 
    _enum_entry = None
    _struct = None
    _field = None

    #
    #   Ctors
    #
    def __init__(self):
        super(CustomListener, self).__init__()

    #
    #   Enter ID processing - typically how we find id / RDL types.
    #
    def enterId(self, ctx:SystemRDLParser.StrContext):
        """ We just got an ID, this must belong to the active:
            a. enums, enum entries
            b. struct   -or-
            c. field | custom field
        """
        value = ctx.getText()
        if self.context & CTXT_IN_ENUM_ENTRY:
            self._enum_entry["name"] = value
        elif self.context & CTXT_IN_ENUM:
            self._enum["id"] = value
        # Fields always need to be checked before field structs as they share
        # the namespace under the `component`.
        elif self.context & CTXT_IN_COMPONENT_FIELD:
            self._field["id"] = value
        elif self.context & CTXT_IN_COMPONENT_FIELD_EXPLICIT:
            self._field["type"] = value
        elif self.context & CTXT_IN_COMPONENT_FIELD_STRUCT:
            self._struct["id"] = value
        else:
            warn("unimplemented ID type for enterId")

    #
    #   Enumeration object builder
    #

    def enterEnum_def(self, ctx:SystemRDLParser.StrContext):
        if self.context != CTXT_CLEAR:
            panic("found new enum def when processing enum or struct")
        self.context |= CTXT_IN_ENUM
        self._enum = new_enum()

    def enterEnum_entry(self, ctx:SystemRDLParser.StrContext):
        if not self.context & CTXT_IN_ENUM:
            panic("found enum entry in non enum body")
        self.context |= CTXT_IN_ENUM_ENTRY
        self._enum_entry = new_enum_entry()

    def exitEnum_entry(self, ctx:SystemRDLParser.StrContext):
        if not self.context & CTXT_IN_ENUM_ENTRY:
            panic("found enum exit in non enum body")
        self._enum["values"].append(self._enum_entry)
        self._enum_entry = None
        self.context &= ~CTXT_IN_ENUM_ENTRY  

    def exitEnum_def(self, ctx:SystemRDLParser.StrContext):
        if self.context != CTXT_IN_ENUM:
            panic("found enum exit not in enum body")
        self.enums.append(self._enum)
        self._enum = None
        self.context &= ~CTXT_IN_ENUM

    #
    #   Component object builder [struct, field etc]
    #

    def enterComponent_def(self, ctx:SystemRDLParser.StrContext):
        node = ctx.getChild(0).getText()
        if node == "fieldstruct":
            if self.context & CTXT_IN_COMPONENT_FIELD_STRUCT:
                panic("found feildstruct inside another fieldstruct")
            self.context |= CTXT_IN_COMPONENT_FIELD_STRUCT;
            self._struct = new_struct()
        elif node == "field":
            if self.context & CTXT_IN_COMPONENT_FIELD:
                panic("found field within another field")
            self.context |= CTXT_IN_COMPONENT_FIELD
            self._field = new_field()
        else:
            warn("unimplemented component enter for %s" % (node))

    def exitComponent_def(self, ctx:SystemRDLParser.StrContext):
        node = ctx.getChild(0).getText()
        if node == "fieldstruct":
            if not self.context & CTXT_IN_COMPONENT_FIELD_STRUCT:
                panic("found fs exit not inside fs body")
            self.structs.append(self._struct)
            self._struct = None 
            self.context &= ~CTXT_IN_COMPONENT_FIELD_STRUCT
        elif node == "field":
            if not self.context & CTXT_IN_COMPONENT_FIELD:
                panic("found field exit not in field body")
            self._struct["fields"].append(self._field)
            self._field = None
            self.context &= ~CTXT_IN_COMPONENT_FIELD
        else:
            warn("unimplemented component exit for %s" % (node))

    def enterExplicit_component_inst(self, ctx:SystemRDLParser.StrContext):
        if not self.context & CTXT_IN_COMPONENT_FIELD_STRUCT:
            panic("found explicit component in non field struct")
        if self.context & CTXT_IN_COMPONENT_FIELD:
            panic("found explicit field within another field body")
        if self.context & CTXT_IN_COMPONENT_FIELD_EXPLICIT:
            panic("found explicit field within another field body")
        self.context |= CTXT_IN_COMPONENT_FIELD_EXPLICIT
        self._field = new_field()

    def enterComponent_inst_elem(self, ctx:SystemRDLParser.StrContext):
        if self.context & (CTXT_IN_COMPONENT_FIELD_EXPLICIT | CTXT_IN_COMPONENT_FIELD):
            self._field["id"] = ctx.getText()
        else:
            warn("found inst element in non explicit field %s" % (ctx.getText()))            
        
    def exitExplicit_component_inst(self, ctx:SystemRDLParser.StrContext):
        if self.context & CTXT_IN_COMPONENT_FIELD_EXPLICIT:
            self._struct["fields"].append(self._field)
            self._field = None
            self.context &= ~CTXT_IN_COMPONENT_FIELD_EXPLICIT
        else:
            panic("explicit component closed from another component")


    #
    #   Other helpers
    # 

    def dump_parsed(self):
        print("Enums:")
        for e in self.enums:
            print(e)
        print("Structs:")
        for s in self.structs:
            print(s)

################################################################################

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = SystemRDLLexer(input_stream)

    stream = CommonTokenStream(lexer)
    parser = SystemRDLParser(stream)
    tree = parser.root()

    printer = CustomListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

    printer.dump_parsed()
 

if __name__ == '__main__':
    main(sys.argv)
    