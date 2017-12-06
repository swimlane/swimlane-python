.PHONY: local test docs release build-offline-installer

local:
	pip install -e .

test:
	python setup.py test

docs:
	pip install -r docs/requirements.txt
	cd docs/ && make html

release:
	python setup.py sdist bdist_wheel upload -r swimlane

build-offline-installer:
	python2.7 offline_installer/build_installer.py
