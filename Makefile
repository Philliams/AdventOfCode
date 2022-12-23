env_file ?= ./env.yaml
env_name ?= aoc

env: 
	conda env remove -n ${env_name} # remove pre-existing conda env
	conda create --name ${env_name} python=3.10 # create new blank conda env

deps:
	python -m pip install flake8 flake8-match pre-commit pytest # install some dependencies for linting and testing
	pip install -r ./dependencies/requirements.txt # install project dependencies

test:
	python -m pytest --cov=src unittests/ --cov-report term --cov-report html:./docs/source/_static # run pytest + code coverage

lint:
	pre-commit run --all # lint the code

run: # convenience for easily running a file
	date
	python -m src.aoc2022.days.day16
	date

doc:
	cd ./docs && sphinx-build -b html ./source ./build