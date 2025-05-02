# Project Guidelines

This document outlines the standard guidelines for maintaining and contributing to this project.

## Local Development & Containers

The project emphasizes local development as close to the source code as possible, without relying on containers. You are encouraged to use development modes such as `dagster dev` directly on your machine. Similarly, tests should be run locally using `pytest tests` outside of any containerized environment. This approach makes it easy to leverage debugging tools and provides a faster, more interactive development experience.

When you need to test the application in an environment that closely mirrors production, you can use local Docker or Kubernetes setups. This allows you to build and run the application in containers, ensuring compatibility and reproducibility before deploying to production.

## Package Manager and Python Version

- **Package Manager**: We use `uv` as the sole tool for managing Python packages and virtual environments. This ensures consistency across development environments and simplifies dependency management.
- **Python Version**: The project is built using Python 3.13. Ensure that your development environment is configured to use this version by referencing the `.python-version` file.

## Linter

- **Ruff**: We use `ruff` as our linter to enforce code quality and consistency. Ensure that your code passes all `ruff` checks before submitting a pull request.

## Static Type Checker

- **Mypy**: Static type checking is performed using `mypy`. All code must pass `mypy` checks to ensure type safety and reduce runtime errors.

## Code Style

- **PEP-8**: All code must adhere to PEP-8 standards. This includes proper naming conventions, indentation, and line length. Use tools like `black` to automatically format your code according to PEP-8.

## Contribution Guidelines

- Ensure all new features and bug fixes are covered by tests.
- Write clear and concise commit messages.
- Follow the branching strategy outlined in the `CONTRIBUTING.md` file.

## Additional Tools

- **Black**: Use `black` for code formatting to maintain a consistent style across the codebase.
- **Pre-commit Hooks**: Set up pre-commit hooks to automatically run linters and type checkers before committing code.

By following these guidelines, we ensure a high standard of code quality and maintainability across the project. Thank you for your contributions!
