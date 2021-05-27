# vigilant-chainsaw

[![wemake-python-styleguide](https://github.com/esemi/vigilant-chainsaw/actions/workflows/linters.yml/badge.svg?branch=master)](https://github.com/esemi/vigilant-chainsaw/actions/workflows/linters.yml)
[![pytest](https://github.com/esemi/vigilant-chainsaw/actions/workflows/unittests.yml/badge.svg?branch=master)](https://github.com/esemi/vigilant-chainsaw/actions/workflows/unittests.yml)
---

## Project local running

```bash
$ git clone PATH

$ cd vigilant-chainsaw
$ python3.9 -m venv venv
$ source venv/bin/activate
$ pip install poetry
$ poetry install
$ poetry run mypy bot/
$ poetry run pytest -ra -v --cov=bot  tests

```

## TODO
- fishing bot
- unittests
- readme runner
- select water cell only once
- deploy to pypi + badge
- sigint handler
