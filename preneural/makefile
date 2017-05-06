.PHONY: install uninstall run upgrade test
envname := env
UNAME_S := $(shell uname -s)
install:
	python3 -m venv $(envname)
	$(envname)/bin/pip install -r requirements.txt
uninstall:
	rm -r $(envname)
upgrade: requirements.txt
	$(envname)/bin/pip install --upgrade
	rm requirements.txt
	$(envname)/bin/pip freeze > requirements.txt
run:
	$(envname)/bin/python src/main.py
test:
	$(envname)/bin/pytest src/ising.py
doc:
	pdflatex informe/informe.tex
