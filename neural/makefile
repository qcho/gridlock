.PHONY: install uninstall run upgrade test
envname := venv
install:
	virtualenv $(envname) --python=python3
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
