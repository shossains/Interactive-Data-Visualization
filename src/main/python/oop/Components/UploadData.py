__all__ = ['Dashboard']

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import src.main.python.Dataframe
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp

from src.main.python.Dataframe import Dataframe


class UploadData(DashComponent):
    def __init__(self):
        super().__init__()

    def layout(self, params=None):
        return html.Div([self.querystring(params)(dcc.Upload)(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
            html.P(id='dummy')
        ])

    def component_callbacks(self, app):
        @app.callback(Output('dummy', 'children'),
                      [
                          Input('upload-data', 'contents'),
                          Input('upload-data', 'filename')
                      ])
        def upload_data(contents, filename):
            """
                   Updates the dataframe when a file is loaded in.
                   :param contents: the contents of the file
                   :param filename: the name of the file
                   :return: dummy html.P, which is used to activate chained callbacks.
                   """
            if contents:
                contents = contents[0]
                filename = filename[0]
                if contents is None:
                    return

                df = Dataframe(contents, filename).data
                print("data uploaded")
