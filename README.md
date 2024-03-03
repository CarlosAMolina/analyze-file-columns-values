## Introduction

Get information about the values in the columns of a file.

This information helps to define the SQL columns for the file.

## Logic

1. Read .csv file as strings to not modify the data.
2. Detect the type of each column: integer, decimal or string. To do this, each value is stripped, for example ` 1 ` is an integer.
3. Analyze each column to show information like the maximum and minimum value, the value with maximum number of digits/characters, etc.

## Tests

First, activate the virtual environment with the requirements installed.

```bash
make test
```
