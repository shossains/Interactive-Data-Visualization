import dash
import numpy as np
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
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

    def layout(self, params=None):
        """
               Shows the html layout of the Normal plot. Parameters are also passed through
               :param params: Parameters selected at the current level of the dashboard.
               :return: Html layout of the program.
        """
        page = dbc.Container([
            dbc.Row([
                html.H6("Filtering"),
                dbc.Col(html.Div(id="filters")),
                dbc.Col(html.Div([
                    html.Button("Add filter", id="add-filter-button", n_clicks=0,
                                style=self.buttonstyle)])),
                dbc.Col(html.Div([
                    html.Button("Remove filter", id="remove-filter-button", n_clicks=0,
                                style=self.buttonstyle)]))
            ]),
        ], fluid=True)
        return page

    def component_callbacks(self, app):
        """
               Automatically does the callbacks of the interactive parts of the dashboard main components.
               :param app: Dash app that uses the code
               :return: Output of the callback functions.
        """

        @app.callback(Output('filters', 'children'), [
            Input('add-filter-button', 'n_clicks'),
            Input('remove-filter-button', 'n_clicks'),
        ])
        def add_filter(add_filter_button, remove_filter_button):

            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
            if 'add-filter-button' in changed_id:
                self.amount_filters = self.amount_filters + 1
            elif 'remove-filter-button' in changed_id:
                self.amount_filters = 0
                # return {}

            filters = []

            for i in range(self.amount_filters):
                page = html.Div(dbc.Row([
                    dbc.Col(
                        html.Div([
                            dcc.Dropdown(
                                id='query-labels' + str(i),
                                placeholder='Select ...',
                                clearable=False)
                            # multi=True
                        ])
                    ),
                    dbc.Col(
                        html.Div([
                            dcc.Dropdown(
                                id='query-conditions' + str(i),
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
                            dcc.Input(id='query-input' + str(i),
                                      placeholder='Fill in your query',
                                      debounce=True),

                        ])
                    ),
                    dbc.Col(
                        html.Div([
                            html.Button("Remove filter", id="remove-filter-button" + str(i), n_clicks=0,
                                        style=self.buttonstyle)
                        ])
                    )
                ]))

                filters.append(page)

            return html.Div(filters)




    def set_data(self, data):
        self.df = data
        self.original_data = data
