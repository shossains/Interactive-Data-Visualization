__all__ = ['Dashboard']

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp
from src.main.python.oop.Figure_factories import FigureFactories


class Instructions(DashComponent):
    def __init__(self, plot_factory, df, title="Instruction page"):
        super().__init__(title=title)
        self.plot_factory = FigureFactories.FigureFactories()
        self.df = df

    def layout(self, params=None):
        page = dbc.Container([
            html.Div([
                html.H2("Welcome to the interactive data visualiser"),
                html.H5("Made by Glenn van den Belt, Shaan Hossain, Joost Jansen, Adrian Kuiper,  Philip Tempelman"),

                html.H4("Instructions"),
                html.H6("Explanation texts")
            ], id='Instructions')
        ], fluid=True)
        return page

    #def component_callbacks(self, app):

