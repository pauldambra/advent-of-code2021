# Advent of Code 2021 [![CI](https://github.com/pauldambra/advent-of-code2021/actions/workflows/python-app.yml/badge.svg)](https://github.com/pauldambra/advent-of-code2021/actions/workflows/python-app.yml)

The code is licensed CC share alike but the puzzles are from https://adventofcode.com/

# How did I get started?

* pyenv local 3.10.0
* python3 -m pip install --upgrade pip
* pip3 install virtualenv
* virtualenv -p /Users/pauldambra/.pyenv/shims/python3 env
* pyenv local env ??
* source env/bin/activate
* python -m pip install pip-tools
* pip-compile requirements.in
* pip install -r requirements.txt

# Installing dependencies

* Add them to requirements.in
* `pip-compile requirements.in && pip install -r requirements.txt`