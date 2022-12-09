# AdventOfCode
This is my repo for AdventOfCode based off my python [ML template repo](https://github.com/Philliams/ml_template). Each day's code is completely separate in it's own module.

The intent of the code is to explore and refine python best practices. Notable, the following concepts are explored in this repo are:
* Property-Based testing using `Hypothesis` library (see `./unittests` directory for test code.)
* Auto-generated documentation from docstrings using `Sphinx`.
* Code coverage report is generated and included as part of the documentation [here](https://philliams.github.io/AdventOfCode/#code-coverage).
* Static analysis and type checking using `MyPy`.
* CD/CI using `github actions` (see `.github/workflows` directory for build pipeline)


To interact with the repo, a makefile is provided with some high-level commands:
* `make env` will create a conda python environment
* `make deps` will install the relevant dependencies from `dependencies\requirements.txt` (remember to activate the environment before installing the dependencies)
* `make test` will run the local unit tests
* `make run` is a convinience command to run the current day's main script
* `make lint` will lint the code using `pre-commit`
* `make doc` will generate local documentation using `sphinx`

Auto-generated documentation is available [here](https://philliams.github.io/AdventOfCode/).