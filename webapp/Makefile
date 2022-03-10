lint:
	black --check -t py39 -l 100 .
	pylint app --rcfile=pylint.cfg
	pylint lib --rcfile=pylint.cfg
	flake8
	mypy --config mypy.ini app
	mypy --config mypy.ini lib

test:
	coverage run --rcfile=setup.cfg --source=. -m pytest
	coverage report --rcfile=setup.cfg