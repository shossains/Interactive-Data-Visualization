__all__ = ['Dashboard']

import numpy as np
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp
from src.main.python.oop.Figure_factories import FigureFactories


class NormalPlot(DashComponent):

    def __init__(self, plot_factory, df, title="Normal plot"):
        """
        Plot function of basic plot options with graph and subgraph
        :param plot_factory: Factory with all plot functions
        :param df: Dataframe with all data
        :param title: Title of the page
        """
        super().__init__(title=title)
        self.plot_factory = plot_factory
        self.df = df

    def layout(self, params=None):
        """
               Shows the html layout of the Normal plot. Parameters are also passed through
               :param params: Parameters selected at the current level of the dashboard.
               :return: Html layout of the program.
        """
        page = dbc.Container([
            # Only for styling, spaces out selectors
            dbc.Row(html.Br()),
            dbc.Row(html.H5("Main Graph")),
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.H6("Select variable x"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-variable-x-normal-plot',
                            placeholder='Select ...',
                            clearable=False)
                    ])
                ),
                dbc.Col(
                    html.Div([
                        html.H6("Select variable y"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-variable-y-normal-plot',
                            placeholder='Select ...',
                            clearable=False)
                    ])
                ),
                dbc.Col(
                    html.Div([
                        html.H6("Color based on"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-characteristics-normal-plot',
                            placeholder='Select ...',
                            clearable=False)
                        # multi=True
                    ])
                ),
                dbc.Col(
                    html.Div([
                        html.H6("Select plot method"),
                        self.querystring(params)(dcc.Dropdown)(id='select-plot-options-normal-plot',
                                                               options=[
                                                                   {'label': 'Area', 'value': 'area'},
                                                                   {'label': 'Bar', 'value': 'bar'},
                                                                   {'label': 'Box', 'value': 'box'},
                                                                   {'label': 'Density', 'value': 'density'},
                                                                   {'label': 'Histogram', 'value': 'histogram'},
                                                                   {'label': 'Line', 'value': 'line'},
                                                                   {'label': 'Scatter', 'value': 'scatter'},
                                                               ],
                                                               value='scatter', clearable=False)
                    ])
                ),
            ]),
            dbc.Row(
                dbc.Col(
                    html.Div([
                        html.H6("Query Filter"),
                        dcc.Input(id='query-normal-plot',
                                  placeholder='Fill in your query',
                                  debounce=True),

                    ])
                )
            ),
            # Only for styling, spaces out selectors
            dbc.Row(html.Br()),
            dbc.Row(html.H5("Subgraph")),
            dbc.Row(
                dbc.Col(
                    html.Div([
                        html.H6("Select subgraph features"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-dimensions-normal-plot',
                            placeholder='Select ...',
                            multi=True
                        )
                    ])
                ),
            ),
            dbc.Row([
                dbc.Col(
                    dcc.Loading(
                        id="loading-icon-normal-plot",
                        children=[html.Div(
                            dcc.Graph(
                                id='Mygraph-normal-plot'
                            ),
                        )],
                        type="circle"
                    ),

                ),

                dbc.Col(
                    dcc.Loading(
                        id="loading-icon2-normal-plot",
                        children=[html.Div(
                            dcc.Graph(
                                id='Subgraph-normal-plot'
                            ),
                        )],
                        type="circle"
                    )
                )
            ]),
        ], fluid=True)
        return page

    def component_callbacks(self, app):
        """
               Automatically does the callbacks of the interactive parts of the dashboard main components.
               :param app: Dash app that uses the code
               :return: Output of the callback functions.
        """

        @app.callback(Output('Mygraph-normal-plot', 'figure'), [
            Input('select-variable-x-normal-plot', 'value'),
            Input('select-variable-y-normal-plot', 'value'),
            Input('select-characteristics-normal-plot', 'value'),
            Input('select-plot-options-normal-plot', 'value'),
            Input('query-normal-plot', 'value')
        ])
        def update_graph(xvalue, yvalue, options_char, plotvalue, query):
            """
            Updates a normal graph with different options how to plot.

            :param xvalue: Selected x-axis value in the data
            :param yvalue: Selected y-axis value in the data
            :param options_char: Selected characteristic of the data
            :param plotvalue: Selected kind of plot 'scatter', 'density' etc.
            :return: Graph object with the displayed plot
            """
            if xvalue is None or yvalue is None or options_char is None or self.df is None:
                return {}
            if xvalue == "select" or yvalue == "select" or options_char == "select" or plotvalue == "select":
                return {}

            dataframe = self.df.reset_index()
            if query is not None:
                dataframe = dataframe.query(query)

            return self.plot_factory.graph_methods(dataframe, xvalue, yvalue, options_char, plotvalue, query)

        @app.callback(Output('Subgraph-normal-plot', 'figure'), [
            Input('select-characteristics-normal-plot', 'value'),
            Input('select-dimensions-normal-plot', 'value'),
        ])
        def update_subgraph(options_char, dims):
            """
            updates subgraphs when comparing labels to each other
            :param options_char: Selected characteristic of the data
            :param dims: Multiple dimensions that are chosen
            :return: subgraph
            """
            if dims is None or dims == 'select' or self.df is None:
                return {}

            dataframe = self.df.reset_index()

            return self.plot_factory.subgraph_methods(dataframe, options_char, dims)

        @app.callback([Output('select-variable-x-normal-plot', 'options'),
                       Output('select-variable-y-normal-plot', 'options'),
                       Output('select-characteristics-normal-plot', 'options'),
                       Output('select-dimensions-normal-plot', 'options')],
                      [
                          Input('dummy', 'children')
                      ])
        def set_options_variable(dummy):
            """
            loads in possible parameters for the x and y-axis in dropdown from the data.
            :param dummy: dummy html property
            :return: Possible options for dropdown x-axis.
            """
            labels = []

            if self.df is not None:
                if self.df.columns is not None:
                    labels = [{'label': '', 'value': 'select'}]

                if 'row_index_label' in self.df.columns:
                    del self.df['row_index_label']

                row_labels = np.arange(0, self.df.shape[0], 1)
                self.df.insert(0, 'row_index_label', row_labels)

                dataFrame = self.df
                colorLabel = [{'label': '', 'value': 'select'}, {'label': 'No color', 'value': 'no-color'}]

                for i in dataFrame.columns[1::]:
                    labels = labels + [{'label': i, 'value': i}]
                    colorLabel = colorLabel + [{'label': i, 'value': i}]

                return labels, labels, colorLabel, labels
            else:
                return labels, labels, labels, labels

        @app.callback([Output('select-variable-x-normal-plot', 'value'),
                       Output('select-variable-y-normal-plot', 'value'),
                       Output('select-characteristics-normal-plot', 'value'),
                       Output('select-dimensions-normal-plot', 'value')
                       ],
                      [
                          Input('select-variable-x-normal-plot', 'options'),
                          Input('select-variable-y-normal-plot', 'options'),
                          Input('select-characteristics-normal-plot', 'options'),
                          Input('select-dimensions-normal-plot', 'options')
                      ])
        def set_variables(options_x, options_y, options_char, dims):
            """
            Gets the first option and displays it as the dropdown of the 'select-variable-x' and 'select-variable-y'.
            :param options_x: All possible x-axis options
            :param options_y: All possible x-axis options
            :param options_char: All possible characteristic options
            :return: The chosen x-axis and y-axis and characteristic
            """
            if options_y is None or options_x is None or options_char is None or dims is None:
                return None, None, None, None
            if len(options_y) <= 0 or (len(options_x) <= 0) or (len(options_char) <= 0) or (len(dims) <= 0):
                return None, None, None, None
            return options_x[0]['value'], options_y[0]['value'], options_char[0]['value'], None

    def set_data(self, data):
        self.df = data
