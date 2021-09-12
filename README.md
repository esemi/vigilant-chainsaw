Albion-online bot
---

[![wemake-python-styleguide](https://github.com/esemi/vigilant-chainsaw/actions/workflows/linters.yml/badge.svg?branch=master)](https://github.com/esemi/vigilant-chainsaw/actions/workflows/linters.yml)
[![pytest](https://github.com/esemi/vigilant-chainsaw/actions/workflows/unittests.yml/badge.svg?branch=master)](https://github.com/esemi/vigilant-chainsaw/actions/workflows/unittests.yml)
---

Небольшой бот для фарминга ресурсов в mmorpg [albion online](https://albiononline.com/ru/home).

Умеет: 
- рыбачить при наличии водоёма на экране;
- собирать весь хлопок на экране.

![image](https://user-images.githubusercontent.com/4115497/132979592-b2b896dc-2062-4795-82d3-b98b5d209ff5.png)

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

### usage 
```bash
$ poetry run python -m bot.farm --help
```

### run fishing
```bash
$ poetry run python -m bot.farm --resource=fish --limit=1000
```

### run cotton crawling
```bash
$ poetry run python -m bot.farm --resource=cotton --limit=1000
```
