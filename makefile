test:
	python -m unittest discover -s tests
test-filter:
	python -m unittest discover -s tests -k test_is_column_of_this_type_is_true_if_integers_and_null

