__all__ = ['Dashboard']

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_oop_components import DashComponent

from src.main.python.oop.Components import Table, GraphPlot


class MainGraph(DashComponent):
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
        self.MainGraph = GraphPlot.GraphPlot(plot_factory, df, "Main Graph")
        self.SubGraph = GraphPlot.GraphPlot(plot_factory, df, "Sub Graph")

    def layout(self, params=None):
        page = dbc.Container([
            html.P("Habibti please, ana akeed, inti wa ana ahla"),
            html.Div(self.MainGraph.layout(params=["Mygraph-normal-plot"])),
            html.Div(self.SubGraph.layout(params=["Subgraph-normal-plot"]))
        ], fluid=True)
        return page