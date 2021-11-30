LINTER = flake8
API_DIR = API
DB_DIR = db
REQ_DIR = .
PYDOC = python3 -m pydoc -w
TESTFINDER = nose2
include common.mk

export TEST_MODE = 1

FORCE:

prod: all_tests github

github: FORCE
	- git commit -a
	git push origin master

dev_env: FORCE
	- ./setup.sh MAYS_HOME
	pip install -r $(REQ_DIR)/requirements-dev.txt

all_tests: FORCE
	cd $(API_DIR); make tests
	cd $(DB_DIR); make tests

all_docs: FORCE
	cd $(API_DIR); make docs
	cd $(DB_DIR); make docs
