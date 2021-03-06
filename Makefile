NAME := nctools

.PHONY: clean clean-test clean-pyc clean-build doc help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

SHAREDIR := /media/sf_VM-Shared
SHAREWORK := ${SHAREDIR}/${NAME}

cp2win:
	rm -rf ${SHAREWORK}/*
	mkdir -p ${SHAREWORK}
	cp -rf doc Makefile ${NAME} setup.py tests example tox.ini ${SHAREWORK}

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '*.pyo' -exec rm -rf {} +
	find . -name '*~' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	flake8 ${NAME} tests

test: ## run tests quickly with the default Python
	python setup.py test

test-all: ## run tests on every Python version with tox
	tox

test-admin: ## run tests on admin tasks
	$(MAKE) -C tests -f admin_task_tests.mak

coverage: ## check code coverage quickly with the default Python
	#coverage run --source ${NAME} -m unittest
	coverage run --source ${NAME} setup.py test
	coverage report -m
	#coverage html
	#$(BROWSER) htmlcov/index.html

doc: ## generate Sphinx HTML docsumentation, including API docs
	rm -f doc/${NAME}.rst
	rm -f doc/modules.rst
	#sphinx-apidocs -o doc/ ${NAME}
	nctools doc/gencmddoc.plx 
	$(MAKE) -C doc clean
	$(MAKE) -C doc html
	$(BROWSER) doc/build/html/index.html

servedoc: doc ## compile the docss watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C doc html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel --universal
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

dev-install: clean ## install the package locally
	python setup.py develop -f https:/test.pypi.org/simple/ -i https://pypi.org/simple/
	#python setup.py develop --user

temp:
	nctools --multiproc 2 \
	    --clone '(["-p", "lon[:], lat[:], pr[0,:,:]@contourf"], ["-p", "lon[:], lat[:], tas[0,:,:]@contourf"]), mode=argument' \
	    -- ncplot tests/data/sresa1b_ncar_ccsm3-example.nc --backend WebAgg  --debug

