import dash
import numpy as np
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp


from src.main.python.oop.Components.ClientCode.ClientCode import example_function2, example_function1
from src.main.python.oop.Figure_factories import FigureFactories


class NestedFiltering(DashComponent):

    def __init__(self, plot_factory, df, title="Nested Filtering"):
        """
        Plot function of basic plot options with graph and subgraph
        :param plot_factory: Factory with all plot functions
        :param df: Dataframe with all data
        :param title: Title of the page
        """
        super().__init__(title=title)
        self.plot_factory = plot_factory
        self.df = df
        self.original_data = df
        self.amount_filters = 0
        self.buttonstyle = {
            'borderWidth': '1px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'background-color': '#5ebfff',
            'color': 'white',
            "margin-left": "15px",
            "margin-right": "15px"
        }
        self.filters= []

    def layout(self, params=None):
        """
               Shows the html layout of the Normal plot. Parameters are also passed through
               :param params: Parameters selected at the current level of the dashboard.
               :return: Html layout of the program.
        """
        page = dbc.Container([
            dbc.Row([
                html.H6("Filtering"),
                dbc.Col(html.Div(id="filters", children=[])),
                dbc.Col(html.Div([
                    html.Button("Add filter", id="add-filter-button", n_clicks=0,
                                style=self.buttonstyle)])),
                dbc.Col(html.Div([
                    html.Button("Remove filter", id="remove-filter-button", n_clicks=0,
                                style=self.buttonstyle)]))
            ]),
            html.P(id="test-dummy")
        ], fluid=True)
        return page

    def component_callbacks(self, app):
        """
               Automatically does the callbacks of the interactive parts of the dashboard main components.
               :param app: Dash app that uses the code
               :return: Output of the callback functions.
        """

        @app.callback(Output('filters', 'children'),
            Input('add-filter-button', 'n_clicks'),
            State('filters', 'children')
        )
        def add_filter(n_clicksa, children):

                page = html.Div(dbc.Row([
                    dbc.Col(
                        html.Div([
                            dcc.Dropdown(
                                id={
                                    'type': 'query-label',
                                    'index': n_clicksa
                                },
                                placeholder='Select ...',
                                clearable=False)
                            # multi=True
                        ])
                    ),
                    dbc.Col(
                        html.Div([
                            dcc.Dropdown(
                                id={
                                    'type': 'query-condition',
                                    'index': n_clicksa
                                },
                                placeholder='Select ...',
                                options=[
                                    {'label': '==', 'value': '=='},
                                    {'label': '<', 'value': '<'},
                                    {'label': '>', 'value': '>'},
                                    {'label': '<=', 'value': '<='},
                                    {'label': '>=', 'value': '>='},
                                    {'label': '!=', 'value': '!='},
                                ],
                                clearable=False)
                        ])
                    ),
                    dbc.Col(
                        html.Div([
                            html.H6("Query Filter"),
                            dcc.Input(id={
                                'type': 'query-input',
                                'index': n_clicksa
                            },
                                placeholder='Fill in your query',
                                debounce=True),

                        ])
                    ),

                ]))

                children.append(page)
                return children


        # @app.callback(, [
        #     [
        #         Input('dummy', 'children'),
        #         Input('data-process-dummy', 'children'),
        #     ])
        # def update_query(dummy, data_process_dummy):
        #     if self.df is not None:
        #         if self.df.columns is not None:
        #             labels = [{'label': '', 'value': 'select'}]
        #
        #         if 'row_index_label' in self.df.columns:
        #             del self.df['row_index_label']
        #
        #         row_labels = np.arange(0, self.df.shape[0], 1)
        #         self.df.insert(0, 'row_index_label', row_labels)
        #
        #         dataFrame = self.df
        #
        #         for i in dataFrame.columns[1::]:
        #             labels = labels + [{'label': i, 'value': i}]
        #             colorLabel = colorLabel + [{'label': i, 'value': i}]
        #
        #         return labels, labels, colorLabel, labels
        #     else:
        #         return labels, labels, labels, labels
        #
        # @app.callback(Output('test-dummy', 'children'), [
        #     Input({'type':  'query-condition', 'index': ALL}, 'value'),
        #     Input({'type':  'query-label', 'index': ALL}, 'value'),
        #     Input({'type': 'query-input', 'index': ALL}, 'value'),
        # ])
        # def update_query(labels, conditions, input):
        #     query = ""
        #     amount = enumerate(labels)
        #     for i in amount:
        #
        #         query = query + str(labels[i]) + str(query[i])
        #
        #         if i != amount:
        #             query = query + " & "
        #
        #         print(query)
        #         return {}




    def set_data(self, data):
        self.df = data
        self.original_data = data
