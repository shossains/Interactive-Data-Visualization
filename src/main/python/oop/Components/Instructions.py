__all__ = ['Dashboard']

import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp
from src.main.python.oop.Figure_factories import FigureFactories


class Instructions(DashComponent):
    def __init__(self, plot_factory, df, title="Instruction page"):
        """
        Instruction page with explanation and other info.
        :param plot_factory: Factory with all plot functions
        :param df: Dataframe with all data
        :param title: Title of the page
        """
        super().__init__(title=title)
        self.plot_factory = FigureFactories.FigureFactories()
        self.df = df

    def layout(self, params=None):
        """
               Shows the html layout of the Instructions page. Parameters are also passed through
               :param params: Parameters selected at the current level of the dashboard.
               :return: Html layout of the program.
        """
        page = dbc.Container([
            html.Div([
                html.H1("Welcome to the interactive data visualiser", style={'text-align': 'center'}),
                html.H6("Made by", style={'text-align': 'center'}),
                html.H4("Glenn van den Belt", style={'text-align': 'center'}),
                html.H4("Shaan Hossain", style={'text-align': 'center'}),
                html.H4("Joost Jansen", style={'text-align': 'center'}),
                html.H4("Adrian Kuiper", style={'text-align': 'center'}),
                html.H4("Philip Tempelman", style={'text-align': 'center'}),
                html.H2("Instructions"),
                html.H6("Explanation texts")
            ], id='Instructions')
        ], fluid=True)
        return page

    # def component_callbacks(self, app):
