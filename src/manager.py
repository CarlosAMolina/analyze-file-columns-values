import datetime
import typing as tp

from src import extractors
from src import type_analyzer
from src import value_analyzer


def show_file_analysis(file_path_name: str):
    print("[{}] Analyzing file {}".format(datetime.datetime.now(), file_path_name))
    file_df = extractors.get_df_from_csv(file_path_name)
    column_names = file_df.columns.tolist()
    sql_definition: tp.List[str] = []
    for index, column_name in enumerate(file_df, 1):
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
        if column_type == type_analyzer.Type.ALL_NULL:
            value_analyzer.show_all_null_column_analysis()
            sql_definition.append(value_analyzer.get_all_null_sql_definition(column_name))
        elif column_type == type_analyzer.Type.DECIMAL:
            analysis = value_analyzer.get_decimal_analysis(column)
            value_analyzer.show_decimal_column_analysis(analysis)
            sql_definition.append(value_analyzer.get_decimal_sql_definition(analysis, column_name))
        elif column_type == type_analyzer.Type.INTEGER:
            analysis = value_analyzer.get_integer_analysis(column)
            value_analyzer.show_integer_column_analysis(analysis)
            sql_definition.append(value_analyzer.get_integer_sql_definition(analysis, column_name))
        elif column_type == type_analyzer.Type.STRING:
            analysis = value_analyzer.get_string_analysis(column)
            value_analyzer.show_string_column_analysis(analysis)
            sql_definition.append(value_analyzer.get_string_sql_definition(analysis, column_name))
        else:
            raise ValueError(column_type)
    _show_sql_definition(sql_definition)


def _show_sql_definition(sql_definition: tp.List[str]):
    print("\nSQL definition")
    sql_definition_str = "\n".join(sql_definition)
    print(sql_definition_str)
