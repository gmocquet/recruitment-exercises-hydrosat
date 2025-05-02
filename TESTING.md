# Testing Guidelines

This document outlines the testing strategy and guidelines for our project.

## Testing Framework

We use [pytest](https://docs.pytest.org/en/stable/) as our primary testing framework. It is a powerful tool that supports simple unit tests as well as complex functional testing.

## Test Structure

- **Tests**: Located in the `tests/` directory.

## Writing Tests

- **Naming Conventions**: Test files should be named `test_<module>.py`. Test functions should be named `test_<functionality>`.
- **Arrange-Act-Assert Pattern**: Follow this pattern to structure your tests:
  - **Arrange**: Set up the conditions for the test.
  - **Act**: Execute the functionality being tested.
  - **Assert**: Verify that the outcome is as expected.

## Running Tests

To run all tests, use the following command:

```bash
pytest tests
```

To run a specific test file or function, use:

```bash
pytest tests/path/to/test_file.py
pytest tests/path/to/test_file.py::test_function
```
