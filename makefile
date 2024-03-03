test:
	python -m unittest discover -s tests
test-filter:
	python -m unittest discover -s tests -k test_decimal_column_null_value_has_expected_type

