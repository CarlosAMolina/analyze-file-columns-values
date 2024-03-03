test:
	python -m unittest discover -s tests
test-filter:
	python -m unittest discover -s tests -k test_expected_result_is_returned

