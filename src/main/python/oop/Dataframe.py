import base64
import io
import dash_html_components as html
import pandas as pd


class Dataframe:

    def __init__(self, contents, filename):
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
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                self.data = pd.read_excel(io.BytesIO(decoded))
            elif 'txt' or 'tsv' in filename:
                # Assume that the user upl, delimiter = r'\s+'oaded an excel file
                self.data = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')), delimiter=r'\s+')

        except Exception as e:
            print(e)

    def get_data(self):
        return self.data
