.PHONY: local test docs release

local:
	pip install -e .

test:
	python setup.py test

docs:
	pip install -r docs/requirements.txt
	cd docs/ && make html

release:
	python setup.py sdist bdist_wheel upload -r swimlane
