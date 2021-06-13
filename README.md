# vigilant-chainsaw

[![wemake-python-styleguide](https://github.com/esemi/vigilant-chainsaw/actions/workflows/linters.yml/badge.svg?branch=master)](https://github.com/esemi/vigilant-chainsaw/actions/workflows/linters.yml)
[![pytest](https://github.com/esemi/vigilant-chainsaw/actions/workflows/unittests.yml/badge.svg?branch=master)](https://github.com/esemi/vigilant-chainsaw/actions/workflows/unittests.yml)
---

## Project local running

### install
```bash
$ git clone PATH

$ cd vigilant-chainsaw
$ python3.9 -m venv venv
$ source venv/bin/activate
$ pip install poetry
$ poetry install
```

### run tests
```bash
$ poetry run mypy bot/
$ poetry run pytest -ra -v --cov=bot  tests
```

### run fishing
```bash
$ poetry run TODO
```


## TODO

### common
- readme runner
- select water cell only once
- deploy to pypi & badges
- sigint handler

### fishing bot
- parse cli args
- change algo for looking_for_nibbles method

### harvesting bot
- prototype
- search resources by args
- select random cell for hravest
- harvest and retry
