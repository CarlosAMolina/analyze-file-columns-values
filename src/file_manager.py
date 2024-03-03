import pandas as pd


def get_df_from_csv(path_name: str):
    # Read all columns as str to not modify numeric values
    return pd.read_csv(path_name, dtype=str)
