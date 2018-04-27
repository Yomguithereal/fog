# Variables
SOURCE = fog

# Commands
all: lint test

test: unit

lint:
	@echo Linting source code using pep8...
	pycodestyle --ignore E501 $(SOURCE) test
	@echo

unit:
	@echo Running unit tests...
	python -m pytest -s
	@echo
