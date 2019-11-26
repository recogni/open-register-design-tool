
#ANTLR := $(shell which antlr)
ANTLR := antlr4
GRAMMAR_DIR := ../ordt/parse/grammars/
SYSTEM_RDL_G4 := $(GRAMMAR_DIR)/SystemRDL.g4

all:

grammar: $(SYSTEM_RDL_G4)
	mkdir -p system-rdl
	$(ANTLR) -lib $(GRAMMAR_DIR) -o java -Xexact-output-dir $<

.PHONY: grammar

