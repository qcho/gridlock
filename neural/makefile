.PHONY: install uninstall run upgrade test
install:
	virtualenv env --python=python3
	env/bin/pip install -r requirements.txt
uninstall:
	rm -r env
upgrade: requirements.txt
	env/bin/pip install --upgrade
	rm requirements.txt
	env/bin/pip freeze > requirements.txt
run:
	env/bin/python src/main.py
test:
	env/bin/pytest src/ising.py
doc:
	pdflatex informe/informe.tex
