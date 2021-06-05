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
                self.otherGraphs = children

            return children

        @app.callback(Output('buttons', 'children'),
                      Input('add-graph-button', 'n_clicks'))
        def set_options_variable(n_clicks):
            labels = []
            length = len(self.graphList)
            for i in range(length):
                labels.append(html.Button('{}'.format(self.graphList[i].IdTitlePair[1]), value='{}'.format(self.graphList[i].IdTitlePair[0]), id='Button {}'.format(i)))

            # children.append(labels)
            return labels
            # for i in range(length):
            #     print(str(i) + " = " + str(self.graphList[i].IdTitlePair[0]))
            #     @app.callback(Output(str(self.graphList[i].IdTitlePair[0]), 'figure'), [
            #         Input('plot-button', 'n_clicks'),
            #         State('select-variable-x-normal-plot', 'value'),
            #         State('select-variable-y-normal-plot', 'value'),
            #         State('select-characteristics-normal-plot', 'value'),
            #         State('select-plot-options-normal-plot', 'value'),
            #         State('query-normal-plot', 'value'),
            #         State('data-process-dummy', 'children'),
            #         State('Mygraph-normal-plot', 'figure'),
            #     ])
            #     def update_graph(clicks, xvalue, yvalue, color_based_characteristic, plot_type, query,
            #                      data_process_dummy, figure):
            #         """
            #         Updates a normal graph with different options how to plot.
            #
            #         :param data_process_dummy:
            #         :param xvalue: Selected x-axis value in the data
            #         :param yvalue: Selected y-axis value in the data
            #         :param color_based_characteristic: Selected characteristic of the data
            #         :param plot_type: Selected kind of plot 'scatter', 'density' etc.
            #         :param query: Query for filtering data
            #         :return: Graph object with the displayed plot
            #         """
            #         if xvalue is None or yvalue is None or color_based_characteristic is None or self.df is None:
            #             return figure
            #         if xvalue == "select" or yvalue == "select" or color_based_characteristic == "select" or plot_type == "select":
            #             return figure
            #
            #         if query:
            #             dataframe = self.df.query(query)
            #         else:
            #             dataframe = self.df.reset_index()
            #
            #         title = figure["layout"]["title"]["text"]
            #         return self.plot_factory.graph_methods(dataframe, xvalue, yvalue, color_based_characteristic,
            #                                                plot_type, title)