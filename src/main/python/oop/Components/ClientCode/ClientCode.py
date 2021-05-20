import pandas as pd


def example_function1(dataframe: pd.DataFrame):
    return dataframe.iloc[:, 0]


def example_function2(dataframe: pd.DataFrame):
    columns = dataframe.columns
    print(dataframe[columns[0]])
    return dataframe[columns[0]]
