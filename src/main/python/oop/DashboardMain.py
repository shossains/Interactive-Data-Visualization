__all__ = ['Dashboard']

import base64
import datetime

import dash_table

from src.main.python.oop.Components import NormalPlot, OtherToolExample, Instructions
from dash_bootstrap_components.themes import FLATLY

from src.main.python.oop.Components.ToolSelector import ToolSelector
from src.main.python.oop.Figure_factories import FigureFactories
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashComponent, DashComponentTabs, DashApp
import pandas as pd
from src.main.python.oop.Dataframe import Dataframe
import io

class Dashboard(DashComponent):
    def __init__(self, plotfactory):
        """
        Initializes the main component of the dashboard. Makes the subclasses ToolSelector, Table and Instructions
        @rtype: object
        """
        super().__init__(title="Interactive data visualiser")
        df = None
        self.dfList = []
        self.ToolSelector = ToolSelector(plotfactory, df, "Tool selector")
        self.Instructions = Instructions.Instructions(plotfactory, df, "Instruction page")

    def layout(self, params=None):
        """
        Shows the html layout of the main dashboard. Toolselector, table and instructions are integrated within the layout. Parameters are also passed through
        :param params: Parameters selected at the current level of the dashboard.
        :return: Html layout of the program.
        """
        return dbc.Container([

            dbc.Row(html.Br()), # Only for styling, spacing out

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

            dbc.Row(html.Br()), # Only for styling, spacing out

            self.querystring(params)(DashComponentTabs)(id="tabs",
                                                        tabs=[self.Instructions, self.ToolSelector],
                                                        params=params, component=self,),
            dbc.Row(html.Br()), # Only for styling, spacing out
            html.P(id='dummy'),
            html.Pre(id='dummy2')
        ], fluid=True)

    def component_callbacks(self, app):
        """
        Automatically does the callbacks of the interactive parts of the dashboard main components.
        :param app: Dash app that uses the code
        :return: Output of the callback functions.
        """
        @app.callback(Output('dummy', 'children'),
                          Input('upload-data', 'contents'),
                          State('upload-data', 'filename'),
                          State('upload-data', 'last_modified'))
        def update_output(list_of_contents, list_of_names, list_of_dates):
            '''
            Initialises and/or updates the list containing data frames when a new file is uploaded.
            :param list_of_contents: Content of the data frames.
            :param list_of_names: Names of the data frames.
            :param list_of_dates: Last modified date of the frames.
            :return: dummy, which is a placeholder because Dash requires a output.
            '''
            if list_of_contents is not None:
                for name, content in zip(list_of_names, list_of_contents):
                    dfToAdd = Dataframe(content, name).data

                    length = len(self.dfList)
                    #if a file with the same name has been detected, only update the dataframe, don't add it again
                    for i in range(length):
                        if name == self.dfList[i][1]:
                            self.dfList[i] = [dfToAdd, name]
                            break;
                    else:
                        self.dfList.insert(0, [dfToAdd, name])

                self.ToolSelector.set_data(self.dfList)
                print("data uploaded")

if __name__ == '__main__':
    """"
    Main function to be run
    """
    plot_factory = FigureFactories.FigureFactories()
    dashboard = Dashboard(plot_factory)
    DashApp = DashApp(dashboard, querystrings=True, bootstrap=FLATLY)
    DashApp.run(debug=True)
else:
    '''
    This code exists to be able to run test_application.py
    When running test_application, the __name__ is not equal to __main__
    Dash testing api is looking for a Dash app instance in the DashboardMain.py, which is created here.
    '''
    plot_factory = FigureFactories.FigureFactories()
    dashboard = Dashboard(plot_factory)
    app = DashApp(dashboard, querystrings=True, bootstrap=FLATLY).app




