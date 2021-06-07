__all__ = ['Dashboard']

import dash_bootstrap_components as dbc
from dash_oop_components import DashComponent
import dash_html_components as html
from dash.dependencies import Input, Output, State

from src.main.python.oop.Components import Table
from oop.Components.Content import PlotContent


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

        self.mainGraphObject = PlotContent.GraphPlot(plot_factory, df, "Main Graph")

        self.graphList = []
        self.graphList.insert(0, self.mainGraphObject)

        self.SubGraph = PlotContent.GraphPlot(plot_factory, df, "Sub Graph")
        self.Table = Table.Table(plot_factory, df, "Table" + self.title)
        # self.mainGraphObject = html.Div(self.mainGraphObject.layout(params=["Mygraph-normal-plot", "Main Graph"]))
        self.otherGraphs = []

    def layout(self, params=None):
        page = html.Div([
            html.Div(self.mainGraphObject.layout(params=["Mygraph-normal-plot", "Main Graph"])),
            html.Div(id="add-graph", children = self.otherGraphs),
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
                newGraph = PlotContent.GraphPlot(self.plot_factory, self.df, "Graph " + str(n_clicks))
                # newGraphHTML = newGraph.layout(params=["Graph " + str(n_clicks), "Graph " + str(n_clicks)])
                newGraphHTML = newGraph.layout(params=["Graph " + str(n_clicks), str(n_clicks)])
                self.graphList.append(newGraph)

                page = html.Div([
                    html.Div(newGraphHTML),
                    # TODO Make subgraph invisinible till instantiated
                    # html.Div(self.SubGraph.layout(params=["Subgraph-normal-plot"])),
                    html.Div(self.Table.layout(params)),
                    ])

                children.append(page)
                self.otherGraphs = children

            return children

        @app.callback(Output('buttons', 'children'),
                      Input('add-graph-button', 'n_clicks'))
        def set_options_variable(n_clicks):
            # print(self.graphList[i].IdTitlePair[0])
            labels = []
            length = len(self.graphList)
            for i in range(length):
                labels.append(html.Button('{}'.format(self.graphList[i].IdTitlePair[1]), value='{}'.format(self.graphList[i].IdTitlePair[0]),
                                          id={"type": "button", "index": '{}'.format(self.graphList[i].IdTitlePair[0])}, n_clicks = 0))
            return labels
