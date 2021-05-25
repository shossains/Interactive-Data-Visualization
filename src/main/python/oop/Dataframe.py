import base64
import io
import pandas as pd


class Dataframe:

    def __init__(self, contents, filename):
        """
        Initialise Dataframe object and reads in csv, xls or txt files.
        @rtype: object
        """
        self.contents = contents
        self.filename = filename

        content_type, content_string = self.contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV or TXT file
                # global df
                self.data = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
                self.all_dims = self.data.columns
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                self.data = pd.read_excel(io.BytesIO(decoded))
                self.all_dims = self.data.columns
            elif 'txt' or 'tsv' in filename:
                # Assume that the user upl, delimiter = r'\s+'oaded an excel file
                self.data = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')), delimiter=r'\s+')
                self.all_dims = self.data.columns


        except Exception as e:
            print(e)

    def get_data(self):
        """
        Gives dataframe.
        @rtype: object
        """
        return self.data

    def get_dimensions(self):
        """
        Gives amount of dimensions
        @rtype: object
        """
        return self.all_dims

    def set_data(self, data):
        """
        Sets datafile
        @type data: object
        """
        self.data = data

    def set_columns(self, columns):
        """
        Sets columnd
        @rtype: object
        """
        self.data = columns

