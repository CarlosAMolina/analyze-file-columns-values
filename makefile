test:
	python -m unittest discover -s tests
test-filter:
	python -m unittest discover -s tests -k test_does_not_raise_exception

