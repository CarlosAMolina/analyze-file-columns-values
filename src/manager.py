from src import extractors
from src import type_analyzer
from src import value_analyzer


def show_file_analysis(file_path_name: str):
    file_df = extractors.get_df_from_csv(file_path_name)
    for column_name in file_df:
        column = file_df[column_name]
        print()
        print(f"Analyzed column name: {column.name}")
        column_type = type_analyzer.get_column_type(column)
        print(f"Column type: {column_type}")
        if column_type == type_analyzer.Type.DECIMAL:
            value_analyzer.show_decimal_column_analysis(column)
        elif column_type == type_analyzer.Type.INTEGER:
            value_analyzer.show_integer_column_analysis(column)
        elif column_type == type_analyzer.Type.STRING:
            value_analyzer.show_string_column_analysis(column)
        else:
            raise ValueError(column_type)
