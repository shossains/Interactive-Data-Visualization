import pandas as pd


def example_function1(dataframe: pd.DataFrame):
    """
    Example function for client. Makes a copy of dataframe and adds a new column with existing data of the first column.
    :param dataframe: Received dataframe
    :return: Must return pandas dataframe
    """
    altered_dataframe = dataframe.copy()
    columns = altered_dataframe.columns
    altered_dataframe.insert(1, "new column", dataframe[columns[0]], True)
    return altered_dataframe


def example_function2(dataframe: pd.DataFrame):
    """
    E Example function for client. Makes a copy of dataframe and adds twi new columns with existing data of the first column.
    :param dataframe: Received dataframe
    :return: Must return pandas dataframe
    """
    altered_dataframe = dataframe.copy()
    columns = altered_dataframe.columns
    altered_dataframe.insert(1, "new column 2", dataframe[columns[0]], True)
    altered_dataframe.insert(1, "new column", dataframe[columns[0]], True)
    return altered_dataframe
