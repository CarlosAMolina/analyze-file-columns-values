test:
	python -m unittest discover -s tests
test-filter:
	python -m unittest discover -s tests -k test_show_string_column_analysis

