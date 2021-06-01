__all__ = ['Dashboard']

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_oop_components import DashComponent
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

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

        self.graphList = []
        self.graphList.insert(0, self.MainGraph)

        self.SubGraph = GraphPlot.GraphPlot(plot_factory, df, "Sub Graph")

        self.Table = Table.Table(plot_factory, df, "Table" + self.title)

    def layout(self, params=None):

        page = html.Div([
            html.Div(id="add-graph", children=[]),
            dbc.Row(
                html.Button('Add Graph', id = 'add-graph-button', n_clicks=1),
            )])
        return page

    def component_callbacks(self, app, params=None):

        @app.callback(Output('add-graph', 'children'),
                      Input('add-graph-button', 'n_clicks'),
                      State('add-graph', 'children'))

        def update_output(n_clicks, children):
            page = html.Div([
                html.Div("Graph " + str(n_clicks)),
                html.Div(self.MainGraph.layout(params=["Mygraph-normal-plot"])),
                # TODO Make subgraph invisinible till instantiated
                # html.Div(self.SubGraph.layout(params=["Subgraph-normal-plot"])),
                html.Div(self.Table.layout(params)),
                html.Div(id="add-graph", children=[])])

            children.append(page)
            return children