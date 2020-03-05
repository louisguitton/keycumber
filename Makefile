# https://packaging.python.org/tutorials/packaging-projects/#packaging-python-projects
dist:
	python3 setup.py sdist bdist_wheel

upload:
	python3 -m twine upload dist/*
