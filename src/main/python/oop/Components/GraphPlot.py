__all__ = ['Dashboard']

import numpy as np
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp
from src.main.python.oop.Figure_factories import FigureFactories



class GraphPlot(DashComponent):
    def __init__(self, plot_factory, df, title="Graph"):
        """
                Graph function that will only show the graph and not the options reliant from it
                :param plot_factory: Factory with all plot functions
                :param df: Dataframe with all data
                :param title: Title of the page
                """
        super().__init__(title=title)
        self.plot_factory = plot_factory
        self.df = df

    def layout(self, params=None):
        page = dbc.Container([
            dbc.Col([
                dcc.Loading(
                    id="loading-icon-normal-plot",
                    children=[html.Div(
                        dcc.Graph(
                            id='Mygraph-normal-plot'
                        ),
                    )],
                    type="circle"
                ),

                dcc.Loading(
                    id="loading-icon2-normal-plot",
                    children=[html.Div(
                        dcc.Graph(
                            id='Subgraph-normal-plot'
                        ),
                    )],
                    type="circle"
                )
            ]),
        ], fluid=True)
        return page

    # def component_callbacks(self, app):