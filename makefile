test:
	python -m unittest discover -s tests
test-filter:
	python -m unittest discover -s tests -k test_max_length_of_integer_part_if_is_e_number

