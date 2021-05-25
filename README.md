# vigilant-chainsaw
Tmp
---

## Project local running

```bash
$ git clone PATH

$ cd vigilant-chainsaw
$ python3.9 -m venv venv
$ source venv/bin/activate
$ pip install poetry
$ poetry install
$ poetry run pytest -ra -v --cov=bot  tests


```

## TODO
- requirements cleaning
- fishing bot
- CI + linters
- unittests
- readme
- sigint handler
- clustering for water cells