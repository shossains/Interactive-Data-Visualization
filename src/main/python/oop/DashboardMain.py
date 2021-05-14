__all__ = ['Dashboard']

from src.main.python.oop.Components import NormalPlot, ExampleML2
from dash_bootstrap_components.themes import FLATLY

from src.main.python.oop.Components.Table import Table
from src.main.python.oop.Figure_factories import FigureFactories
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash_oop_components import DashComponent, DashComponentTabs, DashApp
import pandas as pd
from src.main.python.oop.Dataframe import Dataframe


class Dashboard(DashComponent):
    def __init__(self, plot_factory):
        super().__init__(title="Interactive data visualiser")
        df = pd.DataFrame({})

        self.NormalPlot = NormalPlot.NormalPlot(plot_factory, df, "Normal plot")
        self.ExampleML2 = ExampleML2.ExampleML2(plot_factory, df, "Example Ml 2")
        self.Table = Table(plot_factory, df, "Show Table")

    def layout(self, params=None):
        return dbc.Container([
            html.H1("Interactive data visualiser"),
            # Data uploader
            html.Div([
                self.querystring(params)(dcc.Upload)(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    className="three columns",
                    style={
                        # 'width': '20%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '10px',
                        'textAlign': 'center',
                        # 'margin': '10px',
                        'background-color': '#878787',
                        'color': 'white'
                    },
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
            ], className="twelve columns"),

            # Selector for tool
            html.Div([
                html.H5("Select machine learning tool"),
                self.querystring(params)(
                    dcc.Dropdown)(
                    id='select-tool',
                    options=[
                        {'label': 'Choose ML method', 'value': 'index'},
                        {'label': 'Normal plot', 'value': 'normal-plot'},
                        {'label': 'other machine learning tool  (not implemented)', 'value': 'other-ml-tool'}
                    ],
                    value='index',
                    className="four columns"
                ),
            ], className="twelve columns"),

            # Used tool
            html.Div(id='selection', className="twelve columns"),

            # Shows table or not
            self.Table.layout(params),
            html.P(id='dummy')
        ], fluid=True)

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
            print("running")
            if contents:
                contents = contents[0]
                filename = filename[0]
                if contents is None:
                    return

                df = Dataframe(contents, filename).data

                # IMPORTANT: Dont forget if you add new classes to give the data
                self.NormalPlot.set_data(df)
                self.ExampleML2.give_data(df)
                self.Table.give_data(df, contents, filename)
                print("data uploaded")
                return {}

        @app.callback(Output('selection', 'children'),
                      Input('select-tool', 'value'))
        def choose_component(selection):
            if selection == 'normal-plot':
                return self.NormalPlot.layout()
            if selection == 'other-ml-tool':
                return self.ExampleML2.layout()
            else:
                return html.Div()


if __name__ == '__main__':
    plot_factory = FigureFactories.FigureFactories()
    dashboard = Dashboard(plot_factory)
    DashApp = DashApp(dashboard, querystrings=True, bootstrap=FLATLY)

    DashApp.run(debug=True)
