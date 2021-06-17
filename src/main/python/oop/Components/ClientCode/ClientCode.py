import pandas as pd


# TODO: Client can add code here to adapt the loaded dataframe. To add code and the required button in the GUI, follow these steps:
#     1. Make a new method in client code
#         - Requirement: The method input and output is required to be a Pandas dataframe.
#     2. Make a new button in StandardMenu.py in the layout method.
#         - Search in the layout method for the comment CLIENT CODE BUTTON HTML LAYOUT and follow the required steps
#     3. Add the back-end of the GUI to the update_processed_data method in StandardMenu.py and follow the required steps

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
