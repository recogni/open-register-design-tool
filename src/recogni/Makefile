
#ANTLR := $(shell which antlr)
ANTLR := /usr/local/Cellar/antlr/4.5.3/antlr-4.5.3-complete.jar
GRAMMAR_DIR := ../ordt/parse/grammars/
SYSTEM_RDL_G4 := $(GRAMMAR_DIR)/SystemRDL.g4
OUTPUT_DIR := system_rdl/

all: grammar

grammar: $(SYSTEM_RDL_G4)
	mkdir -p $(OUTPUT_DIR)
	$(ANTLR) -lib $(GRAMMAR_DIR) -o $(OUTPUT_DIR) -Dlanguage=Python3 -Xexact-output-dir $<


BLACK := black
FORMAT_OPTS := --line-length 80
FORMAT_PATHS =  system_rdl/writers/*.py


format-check:
	@$(BLACK) --version >/dev/null 2>&1 || (echo "Errors: black (version 19.3b0 preferred strongly) must be installed and in your shell PATH before pre-commit hooks can be set up (try \"apt-get install -y python3-pip && pip3 install --user black==19.3b0\" or \"brew install pip3 && pip3 install --user black==19.3b0\")." && false)


setup-format: format-check


format:
	$(BLACK) $(FORMAT_OPTS)  $(FORMAT_PATHS)


.PHONY: grammar

