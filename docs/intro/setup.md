# Developing

## Toolchain

* [pyenv](https://github.com/yyuu/pyenv)
    * [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv)
    * [pyenv-virtualenvwrapper](https://github.com/yyuu/pyenv-virtualenvwrapper)
* [virtualenv](https://virtualenv.readthedocs.org/en/latest/)
* [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/)

## Initial Setup
Clone the repository, create a virtualenv, and install the requirements:

```
$ git clone git@github.com:swimlane/swimlane-python.git
$ cd swimlane-python
$ mkvirtualenv <YOUR_ENV_NAME>
$ pip install -r requirements.txt
```

Install `swimlane` locally in edit mode:

```
$ make local
```

Install all supported Pythons:

```
$ make pythons
```

### Tests

Run the tests:

```
$ make test
```

### Tox

Run `tox` as usual - keep in mind that everything in `requirements.txt` will
be installed in each virtualenv that Tox creates.
