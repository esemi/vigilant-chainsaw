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
- CI + linters
- fishing bot
- unittests
- readme runner
- select water cell only once
- sigint handler
