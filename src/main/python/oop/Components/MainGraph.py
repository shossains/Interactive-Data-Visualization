__all__ = ['Dashboard']

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_oop_components import DashComponent
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from src.main.python.oop.Components import Table, GraphPlot, ToolSelector


class MainGraph(DashComponent):
    def __init__(self, plot_factory, df, title="Graph"):
        """
                        Graph function that will only show the graph and not the options reliant from it
                        :param plot_factory: Factory with all plot functions
                        :param df: Dataframe with all data
                        :param title: Title of the page
                        """
        super().__init__(title=title)
        print("initialize maingraph")
        self.plot_factory = plot_factory
        self.df = df

        self.mainGraphObject = GraphPlot.GraphPlot(plot_factory, df, "Main Graph")

        self.graphList = []
        self.graphList.insert(0, self.mainGraphObject)

        self.SubGraph = GraphPlot.GraphPlot(plot_factory, df, "Sub Graph")
        self.Table = Table.Table(plot_factory, df, "Table" + self.title)

    def layout(self, params=None):
        page = html.Div([
            html.Div(self.mainGraphObject.layout(params=["Mygraph-normal-plot", "Main Graph"])),
            html.Div(id="add-graph", children=[]),
            dbc.Row(
                html.Button('Add Graph', id='add-graph-button', n_clicks=0),
            )])
        return page

    def component_callbacks(self, app, params=None):

        @app.callback(Output('add-graph', 'children'),
                      Input('add-graph-button', 'n_clicks'),
                      State('add-graph', 'children'))
        def update_output(n_clicks, children):

            if n_clicks != 0:
                newGraph = GraphPlot.GraphPlot(self.plot_factory, self.df, "Graph " + str(n_clicks))

                newGraphHTML = newGraph.layout(params=["Graph " + str(n_clicks), "Graph " + str(n_clicks)])
                self.graphList.append(newGraph)

                page = html.Div([
                    html.Div(newGraphHTML),
                    # TODO Make subgraph invisinible till instantiated
                    # html.Div(self.SubGraph.layout(params=["Subgraph-normal-plot"])),
                    html.Div(self.Table.layout(params)),
                    ])

                children.append(page)
            return children

        @app.callback(Output('select-graph', 'options'),
                      [Input('dummy3', 'children'),
                      Input('add-graph-button', 'n_clicks')])
        def set_options_variable(dummy, n_clicks):
            labels = []
            length = len(self.graphList)
            for i in range(length):
                labels = labels + [{'label': self.graphList[i].IdTitlePair[0], 'value': self.graphList[i].IdTitlePair[1]}]
            return labels
