
#ANTLR := $(shell which antlr)
ANTLR := /usr/local/Cellar/antlr/4.5.3/antlr-4.5.3-complete.jar
GRAMMAR_DIR := ../ordt/parse/grammars/
SYSTEM_RDL_G4 := $(GRAMMAR_DIR)/SystemRDL.g4
OUTPUT_DIR := system_rdl/

all: grammar

grammar: $(SYSTEM_RDL_G4)
	mkdir -p $(OUTPUT_DIR)
	$(ANTLR) -lib $(GRAMMAR_DIR) -o $(OUTPUT_DIR) -Dlanguage=Python3 -Xexact-output-dir $<

.PHONY: grammar

