run:
	python -m src /tmp/file.csv

test:
	python -m unittest discover -s tests
test-filter:
	python -m unittest discover -s tests -k show_file_analysis

