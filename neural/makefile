envname := venv
root_module := tpe2

install: install_env install_tpe2
.PHONY: install

run:
	$(envname)/bin/$(root_module)
.PHONY: run

reload: uninstall_tpe2 install_tpe2
.PHONY: reload

uninstall:
	rm -r $(envname)
	rm -r $(root_module).egg-info
.PHONY: uninstall

install_env:
	python3 -m venv $(envname)
.PHONY: install_env

install_tpe2:
	$(envname)/bin/pip install --editable .
.PHONY: install_tpe2

uninstall_tpe2:
	$(envname)/bin/pip uninstall --yes $(root_module)
.PHONY: uninstall_tpe2

upgrade:
	$(envname)/bin/pip-compile --upgrade
	$(envname)/bin/pip-sync
.PHONY: upgrade
