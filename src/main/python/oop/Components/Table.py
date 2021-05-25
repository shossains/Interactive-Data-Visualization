__all__ = ['Dashboard']

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
from src.main.python.oop.Figure_factories import FigureFactories

# dcc.Checklist(id='show-table-ml2', options=[
#     {'label': 'Show table', 'value': 'show-table'}]),


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
        Shows the html layout of the main dashboard. Toolselector, table and instructions are integrated within the
        layout. Parameters are also passed through
        :param params: Parameters selected at the current level of the dashboard.
        :return: Html layout of the program.
        """
        return html.Div([
            # dcc.Checklist(id='show-table', options=[{'label': 'Show table', 'value': 'show-table'}]),
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
            Output('main_table', 'selected_rows'),
            Input('Mygraph-normal-plot', 'selectedData'))
        def display_selected_data(graphPoints):
            points_selected = []
            print(graphPoints)
            if graphPoints is not None:
                print(graphPoints)
                for point in graphPoints['points']:
                    points_selected.append(point['customdata'][0])
            return points_selected

        # This function returns the selected rows in the table. This will most likely go hand-in-hand with a button click which will call this function
        @app.callback(
            Output('dummy2', 'children'),
            Input('main_table', 'selected_rows')
        )
        def selected_to_dataframe(selectedRows):
            pdf = pd.DataFrame(columns=self.df.columns)

            for i in selectedRows:
                pdf = pdf.append(self.df.iloc[i])

            print(pdf)
            return None

        # @app.callback(
        #     Output(component_id='output-data-upload', component_property='style'),
        #     [Input(component_id='show-table', component_property='value')])
        # def show_hide_table(visibility_state):
        #     """
        #     Shows or hides the table. Only loads in the data when checkbox selected.
        #     :param visibility_state:
        #     :return: visibility style
        #     """
        #     if visibility_state == ['show-table']:
        #         return {'display': 'block'}
        #     else:
        #         return {'display': 'none'}
        #
        # @app.callback(Output('output-data-upload', 'children'),
        #               [
        #                   Input('show-table', 'value'),
        #                   Input('select-file', 'value')
        #               ])
        # def update_table(showtable, select_file):
        #     """
        #     Updates table and calls plot_factory show table
        #     :param showtable: Checkbox if marked shows table else it won't.
        #     :return: Table
        #     """
        #     return self.show_table(self.df, showtable)

    def selected_data_callbacks(self, app):
        @app.callback(
            Output('main_table', 'selected_rows'),
            [Input('Mygraph-normal-plot', 'selectedData')])
        def display_selected_data(selectedData):
            print("at least it gets called lol")
            points_selected = []
            if selectedData is not None:
                for point in selectedData['points']:
                    points_selected.append(point['customdata'][0])
                print(points_selected)
            return points_selected

    def set_data(self, df):
        """
        Loads in possible parameters for the x and y-axis in dropdown from the data.
        :param dummy: dummy html property
        :return: Possible options for dropdown x-axis.
        """
        self.df = df

    # def show_table(self, df, showtable):
    #     """
    #         Makes a table from the uploaded data.
    #         :param df: dataframe
    #         :param showtable: Boolean to show table or don't show table.
    #         :return: Table
    #     """
    #     if df is None:
    #         return None
    #
    #     if showtable is not None:
    #         table = html.Div([
    #             dash_table.DataTable(
    #                 data=df.to_dict('rows'),
    #                 columns=[{'name': i, 'id': i} for i in df.columns]
    #             ),
    #             html.Hr(),
    #             html.Div('Raw Content'),
    #         ], id='table-uploaded')
    #         return table
    #     else:
    #         return html.Div()