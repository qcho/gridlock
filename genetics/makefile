envname := venv
root_module := tpe3

install: install_env install_tpe3
.PHONY: install

run:
	$(envname)/bin/$(root_module)
.PHONY: run

reload: uninstall_tpe3 install_tpe3
.PHONY: reload

uninstall:
	rm -r $(envname)
	rm -r $(root_module).egg-info
.PHONY: uninstall

install_env:
	python3 -m venv $(envname)
.PHONY: install_env

install_tpe3:
	$(envname)/bin/pip install --editable .[dev]
.PHONY: install_tpe3

uninstall_tpe3:
	$(envname)/bin/pip uninstall --yes $(root_module)
.PHONY: uninstall_tpe3

upgrade:
	$(envname)/bin/pip-compile --upgrade
	$(envname)/bin/pip-sync
.PHONY: upgrade
