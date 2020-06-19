# QA-Python-Driver-2.0-Tests

The Python Driver driven test suite.

## Setup

The pip dependencies are defined in the requirements.txt file. If you are wanting to install a specific version of the PyDriver, you will need to do that manually.

```bash
pip install -r requirements.txt
```

## Executing

The test suite allows for overriding the target server and user parameters via the following arguments:

- `--url default="https://localhost"`
- `--user default="admin"`
- `--pass This is the password for the user defined above.`
- `--skipverify This is for allowing the version of PyDriver to not match the version of Swimlane.`

To run a specific test and skip the version verification:

```bash
pytest driver_tests/test_app_adaptor.py --skipverify
```

To run all the tests against 10.20.30.40:

```bash
pytest --url "https://10.20.30.40"
```

## More Info

The apps needed for this testing are automatically added and cleaned up. So there is no need to have preset data.

## Support packages

- python request package: <http://docs.python-requests.org/en/master/user/quickstart/#make-a-request>
- PyDriver documentation: <http://swimlane-python-driver.readthedocs.io/en/latest/#usage>
- pytest documentation: <https://docs.pytest.org/en/latest/contents.html>
