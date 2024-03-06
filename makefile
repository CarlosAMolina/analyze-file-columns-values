run:
	python -m src /tmp/file.csv

test:
	python -m unittest discover -s tests
test-filter:
	python -m unittest discover -s tests -k TestFunction_get_column_names_and_types_from_df

