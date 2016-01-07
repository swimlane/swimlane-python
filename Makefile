.PHONY: local test docs show_docs pythons

local:
	pip install -e .

test:
	@cd tests; PYTHONPATH=.. py.test --tb=short

docs:
	sphinx-apidoc -f -o docs swimlane; cd docs; make html

show_docs:
	open docs/_build/html/index.html

pythons:
	while read v; do pyenv install -s $$v; done < .python-version
