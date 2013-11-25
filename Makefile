.PHONY: docs build test coverage build_rpm

ifndef VTENV_OPTS
VTENV_OPTS = "--no-site-packages"
endif

buildout: bin/buildout
	bin/buildout

demo: bin/buildout
	bin/buildout install site1 site2

status:
	bin/supervisorctl status

bin/python:
	virtualenv $(VTENV_OPTS) .

bin/buildout: bin/python
	bin/python bootstrap.py
