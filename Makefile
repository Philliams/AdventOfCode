env_file ?= ./env.yaml
env_name ?= aoc

env: 
	conda env remove -n ${env_name} # remove pre-existing conda env
	conda create --name ${env_name} python=3.10 # create new blank conda env

deps:
	python -m pip install flake8 pre-commit pytest # install some dependencies for linting and testing
	pip install -r ./dependencies/requirements.txt # install project dependencies

test:
	python -m pytest --cov=src unittests/ # run pytest + code coverage

lint:
	pre-commit run --all # lint the code

run: # convenience for easily running a file
	cd src/aoc2022 && python ./day3.py

doc:
	cd ./docs && sphinx-build -b html ./source ./build