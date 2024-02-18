test:
	python -m unittest discover -s tests
test-filter:
	python -m unittest discover -s tests -k test_show_integer_column_analysis

