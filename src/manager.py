import datetime

from src import extractors
from src import type_analyzer
from src import value_analyzer


def show_file_analysis(file_path_name: str):
    print("[{}] Analyzing file {}".format(datetime.datetime.now(), file_path_name))
    file_df = extractors.get_df_from_csv(file_path_name)
    column_names = file_df.columns.tolist()
    for column_name in file_df:
        index = column_names.index(column_name) + 1  # TODO change with enumerate()
        print()
        print(
            "[{}] Analyzing column {} of {}. Column name: {}".format(
                datetime.datetime.now(),
                index,
                len(column_names),
                column_name,
            )
        )
        column = file_df[column_name]
        column_type = type_analyzer.get_column_type(column)
        print(f"Column type: {column_type.value}")
        if column_type == type_analyzer.Type.DECIMAL:
            analysis = value_analyzer.get_decimal_analysis(column)
            value_analyzer.show_decimal_column_analysis(column, analysis)
        elif column_type == type_analyzer.Type.INTEGER:
            analysis = value_analyzer._get_integer_analysis(column)
            value_analyzer.show_integer_column_analysis(column, analysis)
        elif column_type == type_analyzer.Type.STRING:
            value_analyzer.show_string_column_analysis(column)
        else:
            raise ValueError(column_type)
