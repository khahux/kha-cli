pip install --editable .
python setup.py sdist
python setup.py install
twine upload dist/*
