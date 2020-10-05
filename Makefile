# Variables
SOURCE = fog cfog docs

# Commands
all: lint test
test: build-ext unit
publish: clean lint test build-ext upload clean

build-ext:
	@echo Building native extensions...
	find . -name *.pyx | xargs cython && find . -name *.c
	@echo
	python setup.py build_ext --inplace
	@echo

clean:
	rm -rf *.egg-info .pytest_cache .ipynb_checkpoints build dist
	find . -name __pycache__ -type d | xargs rm -rf
	find . -name *.c -type f | xargs rm
	find . -name *.so -type f | xargs rm

deps:
	pip3 install -U pip
	pip3 install -U setuptools
	pip3 install -r requirements.txt

lint:
	@echo Linting source code using pep8...
	pycodestyle --ignore E501,E722,E731,E741,W503,W504 $(SOURCE) test
	@echo Searching for unused imports...
	importchecker $(SOURCE) | grep -v __init__ || true
	@echo

readme:
	python -m docs.build > README.md

unit:
	@echo Running unit tests...
	PYTHONHASHSEED=0 && pytest -s
	@echo

upload:
	python setup.py sdist bdist_wheel
	twine upload dist/*
