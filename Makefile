# https://packaging.python.org/tutorials/packaging-projects/#packaging-python-projects

.PHONY:dist
dist:
	python3 setup.py sdist bdist_wheel

.PHONY:upload
upload:
	python3 -m twine upload --skip-existing dist/*


.PHONY:test
test:
	pytest tests
