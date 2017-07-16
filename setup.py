from setuptools import setup, find_packages


def parse_requirements(requirement_file):
    with open(requirement_file) as f:
        return f.readlines()


with open('./README.rst') as f:
    long_description = f.read()


setup(
    name="swimlane",
    author="Swimlane LLC",
    author_email="info@swimlane.com",
    url="https://github.com/swimlane/swimlane-python",
    packages=find_packages(exclude=('tests', 'tests.*')),
    description="Python driver for the Swimlane API",
    long_description=long_description,
    license='AGPLv3',
    install_requires=parse_requirements('./requirements.txt'),
    setup_requires=[
        'setuptools_scm',
        'pytest-runner'
    ],
    use_scm_version=True,
    tests_require=parse_requirements('./test-requirements.txt'),
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)
