.PHONY: local test docs show_docs release

local:
	pip install -e .

test:
	python setup.py test

docs:
	pip install -r requirements/docs.txt
	sphinx-apidoc -f -o docs swimlane; cd docs; make html

show_docs:
	open docs/_build/html/index.html

release:
	python setup.py sdist bdist_wheel upload -r swimlane
