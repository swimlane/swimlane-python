.PHONY: local test docs release build-offline-installer

local:
	pip install -e .

test:
	python setup.py test

docs:
	pip install -r docs/requirements.txt
	cd docs/ && make html

release:
	python3 setup.py sdist bdist_wheel upload -r swimlane

build-offline-installer:
	python3 offline_installer/build_installer.py
