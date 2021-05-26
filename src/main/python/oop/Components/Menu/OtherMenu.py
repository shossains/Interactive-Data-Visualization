__all__ = ['Dashboard']

import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_oop_components import DashComponent
from src.main.python.oop.Figure_factories import VisualFactories


class OtherMenu(DashComponent):
    def __init__(self, plot_factory, df, title="Example ML"):
        """
        This only serves as a demo as to where and how another menu could be made.
        :param plot_factory:
        :param df:
        :param title:
        """
        super().__init__(title=title)
        self.plot_factory = VisualFactories.FigureFactories()
        self.df = df

    def layout(self, params=None):
        page = dbc.Container([
            html.Br(),
            html.Div([
                html.H3("This would be another menu, only serves as a demo"),
            ],
                id='other-menu-selection', style={'display': 'block'}),
        ], fluid=True)
        return page

    # def component_callbacks(self, app):

    def set_data(self, data):
        self.df = data
