import dash_table
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash_oop_components import DashComponent
import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp


from src.main.python.oop.Dataframe import Dataframe
from src.main.python.oop.Figure_factories import VisualFactories

class Table(DashComponent):
    def __init__(self, plot_factory, df, title="Table"):
        """
        Displays table at the bottom of the page.
        :param plot_factory: Factory with all plot functions
        :param df: Dataframe with all data
        :param title: Title of the page
        """
        super().__init__(title=title)
        self.plot_factory = plot_factory
        self.df = df

    def layout(self, params=None):
        """
        Shows the html layout of the table component.
        :param params: Parameters selected at the current level of the dashboard.
        :return: Html layout of the program.
        """
        return html.Div([
            dcc.Loading(
                id="loading-icon3",
                children=[html.Div(id='output-data-upload')],
                type="dot",
            )
        ])

    def component_callbacks(self, app):
        """
        Automatically does the callbacks of the interactive parts of the table component.
        :param app: Dash app that uses the code.
        :return: Output of the callback functions.
        """
        @app.callback(
            Output('main_table', 'selected_rows' + self.title),
            Input('Mygraph-normal-plot', 'selectedData'))
        def display_selected_data(graphPoints):
            """
            Display the selected data i the table.
            :param graphPoints:  Data that is currently displayed
            :return:  Table
            """
            points_selected = []
            if graphPoints is not None:
                print(graphPoints)
                for point in graphPoints['points']:
                    points_selected.append(point['customdata'][0])
            return points_selected

    def set_data(self, df):
        """
        Loads in possible parameters for the x and y-axis in dropdown from the data.
        :param dummy: dummy html property
        :return: Possible options for dropdown x-axis.
        """
        self.df = df