# Variables
SOURCE = fog

# Commands
all: lint test
test: unit
publish: lint test upload clean

clean:
	rm -rf *.egg-info .pytest_cache .ipynb_checkpoints ./**/__pycache__ ./**/**/__pycache__ build dist

lint:
	@echo Linting source code using pep8...
	pycodestyle --ignore E501,E722,E731,E741,W503,W504 $(SOURCE) test
	@echo

unit:
	@echo Running unit tests...
	PYTHONHASHSEED=0 && pytest -s
	@echo

upload:
	python setup.py sdist bdist_wheel
	twine upload dist/*
