# Variables
SOURCE = fog

# Commands
all: lint

# test: test-unittest

lint:
	@echo Linting source code using pep8...
	pycodestyle $(SOURCE)
	@echo
