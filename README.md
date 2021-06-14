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
$ poetry run flake8 bot
$ poetry run pytest -ra -v --cov=bot  tests
```

### run fishing
```bash
$ poetry run TODO
```


## TODO

### common
- parse cli args
- readme runner
- deploy to pypi & badges

### fishing bot
- change algo for looking_for_nibbles method

### harvesting bot
- harvest not only cotton
- harvest by scan all frame: by mouse position + placeholder text
