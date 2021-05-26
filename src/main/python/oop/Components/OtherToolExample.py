__all__ = ['Dashboard']

import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_oop_components import DashComponent
from src.main.python.oop.Figure_factories import FigureFactories


class ExampleML2(DashComponent):
    def __init__(self, plot_factory, df, title="Example ML"):
        """
        NO Pydocs not in use code TODO: make second class
        :param plot_factory:
        :param df:
        :param title:
        """
        super().__init__(title=title)
        self.plot_factory = FigureFactories.FigureFactories()
        self.df = df

    def layout(self, params=None):
        page = dbc.Container([
            html.Div([
                html.H3("This is another tool "),
            ],
                id='OtherToolExample', style={'display': 'block'}),
        ], fluid=True)
        return page

    # def component_callbacks(self, app):

    def set_data(self, data):
        self.df = data
