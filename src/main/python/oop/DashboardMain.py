__all__ = ['Dashboard']

from src.main.python.oop.Components import NormalPlot, OtherToolExample, Instructions
from dash_bootstrap_components.themes import FLATLY

from src.main.python.oop.Components.Table import Table
from src.main.python.oop.Components.ToolSelector import ToolSelector
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
        self.ToolSelector = ToolSelector(plot_factory,df, "Tool selector")
        self.Table = Table(plot_factory, df, "Show Table")
        self.Instructions = Instructions.Instructions(plot_factory, df, "Instruction page")

    def layout(self, params=None):
        return dbc.Container([
            dbc.Row(dbc.Col(html.H1("Interactive data visualizer"), width="auto"), justify="center"),

            # Row for uploading the data
            dbc.Row(
                dbc.Col(
                    html.Div(
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                # 'width': '20%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '10px',
                                'textAlign': 'center',
                                'background-color': '#5ebfff',
                                'color': 'white'
                            },
                            # Allow multiple files to be uploaded
                            multiple=True
                        ),
                   ), width=2
                ), justify="center"
            ),

            self.querystring(params)(DashComponentTabs)(id="tabs",
                                                        tabs=[self.Instructions, self.ToolSelector],
                                                        params=params, component=self,),


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
                self.ToolSelector.set_data(df)
                self.Table.set_data(df, contents, filename)
                print("data uploaded")
                return {}


if __name__ == '__main__':
    plot_factory = FigureFactories.FigureFactories()
    dashboard = Dashboard(plot_factory)
    DashApp = DashApp(dashboard, querystrings=True, bootstrap=FLATLY)

    DashApp.run(debug=True)
