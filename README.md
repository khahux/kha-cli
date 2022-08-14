# kha

## Dev

```shell
virtualenv --python=python3.8 venv
source venv/bin/activate
pip install --editable .
```

## Publish to PyPI

```shell
python setup.py sdist --formats=zip --owner=root --group=root
python setup.py install

twine upload dist/*
```
