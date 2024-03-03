test:
	python -m unittest discover -s tests
test-filter:
	python -m unittest discover -s tests -k TestFunction_show_file_analysis

