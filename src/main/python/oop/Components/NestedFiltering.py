import dash
import numpy as np
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp

from src.main.python.oop.Components.ClientCode.ClientCode import example_function2, example_function1


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
            "margin-right": "15px"
        }
        self.filters = []

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
                dbc.Col(html.Br()),
                dbc.Col(html.Div([
                    html.Button("Add filter", id="add-filter-button", n_clicks=0,
                                style=self.buttonstyle)])),
                # dbc.Col(html.Div([
                #     html.Button("Remove filter", id="remove-filter-button", n_clicks=0,
                #                 style=self.buttonstyle)])),
                dbc.Col(html.Div([
                    html.Button("Apply filter", id="apply-filter-button", n_clicks=0,
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
                dbc.Col(html.Div(
                    html.Br()
                ))
            ]))

            children.append(page)
            return children

        @app.callback(
            Output({'type': 'query-label', 'index': MATCH}, 'options'),
            [
                Input('file-name', 'data'),
                Input('data-process-dummy', 'children'),
            ])
        def update_query(dummy, data_process_dummy):
            if self.df is not None:
                if self.df.columns is not None:
                    labels = [{'label': '', 'value': 'select'}]

                if 'row_index_label' in self.df.columns:
                    del self.df['row_index_label']

                row_labels = np.arange(0, self.df.shape[0], 1)
                self.df.insert(0, 'row_index_label', row_labels)

                dataFrame = self.df

                for i in dataFrame.columns[1::]:
                    labels = labels + [{'label': i, 'value': i}]

                return labels
            else:
                return [{'label': 'no-label', 'value': 'no-label'}]

        @app.callback(Output('test-dummy', 'value'), [
            Input({'type':  'query-label', 'index': ALL}, 'value'),
            Input({'type':  'query-condition', 'index': ALL}, 'value'),
            Input({'type': 'query-input', 'index': ALL}, 'value'),
            Input('apply-filter-button', 'n_clicks'),
        ])
        def apply_query(labels, conditions, input, apply):
            query = ""
            if None not in labels and None not in conditions and None not in input:
                amount = len(labels)
                for i in range(amount):
                    print(i)
                    query = query  + str(labels[i]) + str(conditions[i]) + str(input[i])

                    if i < amount - 1:
                        query = query + " & "

                return query
            else:
                return query

    def set_data(self, data):
        self.df = data
        self.original_data = data
