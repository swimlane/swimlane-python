.PHONY: local test docs show_docs pythons release

local:
	pip install -e .

test:
	python setup.py test

docs:
	sphinx-apidoc -f -o docs swimlane; cd docs; make html

show_docs:
	open docs/_build/html/index.html

pythons:
	while read v; do pyenv install -s $$v; done < .python-version

release:
	python setup.py sdist bdist_wheel upload
