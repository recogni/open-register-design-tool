
ANTLR := $(shell which antlr)
GRAMMAR_DIR := ../ordt/parse/grammars/
SYSTEM_RDL_G4 := $(GRAMMAR_DIR)/SystemRDL.g4

all:

grammar: $(SYSTEM_RDL_G4)
	mkdir -p system-rdl
	$(ANTLR) -Dlanguage=Python3 -lib $(GRAMMAR_DIR) -o system-rdl \
		-Xexact-output-dir $<

.PHONY: grammar

