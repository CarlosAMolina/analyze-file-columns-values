test:
	python -m unittest discover -s tests
test-filter:
	python -m unittest discover -s tests -k test_is_column_of_this_type_is_false_if_e_number_is_integer

