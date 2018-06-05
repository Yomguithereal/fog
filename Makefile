# Variables
SOURCE = fog

# Commands
all: lint test
test: unit
publish: lint test upload clean

clean:
	rm -rf *.egg-info .pytest_cache ./**/**/__pycache__ build dist

lint:
	@echo Linting source code using pep8...
	pycodestyle --ignore E501,E741 $(SOURCE) test
	@echo

unit:
	@echo Running unit tests...
	pytest -s
	@echo

upload:
	python setup.py sdist bdist_wheel
	twine upload dist/*
