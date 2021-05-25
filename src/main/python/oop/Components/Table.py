__all__ = ['Dashboard']

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp

from src.main.python.oop.Dataframe import Dataframe
from src.main.python.oop.Figure_factories import FigureFactories

dcc.Checklist(id='show-table-ml2', options=[
    {'label': 'Show table', 'value': 'show-table'}]),


class Table(DashComponent):
    def __init__(self, plot_factory, df, title="Table"):
        """
        Displays table at the bottom of the page.
        :param plot_factory: Factory with all plot functions
        :param df: Dataframe with all data
        :param title: Title of the page
        """
        super().__init__(title=title)
        self.contents = None
        self.filename = None
        self.plot_factory = plot_factory
        self.df = df

    def layout(self, params=None):
        """
        Shows the html layout of the main dashboard. Toolselector, table and instructions are integrated within the layout. Parameters are also passed through
        :param params: Parameters selected at the current level of the dashboard.
        :return: Html layout of the program.
        """
        return html.Div([
            dcc.Checklist(id='show-table', options=[{'label': 'Show table', 'value': 'show-table'}]),
            html.Div(id='output-data-upload'),
            dcc.Loading(
                id="loading-icon3",
                children=[html.Div(id='output-data-upload')],
                type="dot",
            )
        ])

    def component_callbacks(self, app):
        """
        Automatically does the callbacks of the interactive parts of the normal plot components.
        :param app: Dash app that uses the code
        :return: Output of the callback functions.
        """
        @app.callback(
            Output(component_id='output-data-upload', component_property='style'),
            [Input(component_id='show-table', component_property='value')])
        def show_hide_table(visibility_state):
            """
            Shows or hides the table. Only loads in the data when checkbox selected.
            :param visibility_state:
            :return: visibility style
            """
            if visibility_state == ['show-table']:
                return {'display': 'block'}
            else:
                return {'display': 'none'}

        @app.callback(Output('output-data-upload', 'children'),
                      [
                          Input('show-table', 'value'),
                          Input('select-file', 'value')
                      ])
        def update_table(showtable, select_file):
            """
            Updates table and calls plot_factory show table
            :param showtable: Checkbox if marked shows table else it won't.
            :return: Table
            """
            return self.plot_factory.show_table(self.df, showtable)

    def set_data(self, df):
        """
        Loads in possible parameters for the x and y-axis in dropdown from the data.
        :param dummy: dummy html property
        :return: Possible options for dropdown x-axis.
        """
        self.df = df