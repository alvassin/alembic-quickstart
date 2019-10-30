PROJECT_NAME ?= $(shell python3 setup.py --name)
PROJECT_VERSION ?= $(shell python3 setup.py --version)

all:
	@echo "make devenv	- Configure dev environment"
	@echo "make sdist	- Build package"
	@echo "make clean	- Remove files created by distutils & dev modules"
	@echo "make test	- Run tests"
	@exit 0


devenv:
	rm -rf env
	python -m venv env
	env/bin/pip install -Ue '.[dev]'

clean:
	rm -fr *.egg-info dist

sdist: clean
	env/bin/python setup.py sdist

test:
	env/bin/pytest
