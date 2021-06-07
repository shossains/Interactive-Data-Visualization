__all__ = ['Dashboard']

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_oop_components import DashComponent

from src.main.python.oop.Components.Table import Table


    def __init__(self, plot_factory, df, title="Graph"):
        """
                Graph function that will only show the graph and not the options reliant from it
                :param plot_factory: Factory with all plot functions
                :param df: Dataframe with all data
                :param title: Title of the page
                """
        super().__init__(title=title)
        # self.Table = Table(plot_factory, df, "Show Table")
        self.plot_factory = plot_factory
        self.df = df
        self.IdTitlePair = ["id", "title"]

    def layout(self, params=None):
        self.set_data([params[0], params[1]])
        page = dbc.Row(
            dbc.Col(
                dcc.Loading(
                    id="loading-icon-normal-plot",
                    children=[html.Div(
                        dcc.Graph(
                            figure={'layout': {'title': params[1]}},
                            id={'type': 'page_content_graph', 'index': params[0]},
                            config={
                                "displaylogo": False,
                                "showTips": True,
                                "showAxisDragHandles": True,
                                "scrollZoom": True,
                                "edits": {"titleText": True}
                            },
                        ),
                    )],
                    type="graph"
                )
            )
        )
        return page

    # def component_callbacks(self, app):

    def set_data(self, idTitlePair):
        self.IdTitlePair = idTitlePair

__all__ = ['Dashboard']

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_oop_components import DashComponent

from src.main.python.oop.Components.Table import Table


class PlotContent(DashComponent):
    def __init__(self, plot_factory, df, title="Graph"):
        """
                Graph function that will only show the graph and not the options reliant from it
                :param plot_factory: Factory with all plot functions
                :param df: Dataframe with all data
                :param title: Title of the page
                """
        super().__init__(title=title)
        self.Table = Table(plot_factory, df, "Show Table")
        self.plot_factory = plot_factory
        self.df = df

    def layout(self, params=None):
        page = dbc.Container([
                dbc.Row(
                    dbc.Col(
                        dcc.Loading(
                            id="loading-icon-normal-plot",
                            children=[html.Div(
                                dcc.Graph(
                                    id='Mygraph-normal-plot',
                                    config={
                                        "displaylogo": False,
                                        "showTips": True,
                                        "showAxisDragHandles": True,
                                        "scrollZoom": True
                                    }
                                ),
                            )],
                            type="graph"
                        )
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        dcc.Loading(
                            id="loading-icon2-normal-plot",
                            children=[html.Div(
                                dcc.Graph(
                                    id='Subgraph-normal-plot',
                                    config={
                                        "displaylogo": False,
                                        "showTips": True,
                                        "showAxisDragHandles": True,
                                        "scrollZoom": True
                                    }
                                )
                            )],
                            type="graph"
                        )
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        html.Div(self.Table.layout(params))
                    )
                )
        ], fluid=True)
        return page

    # def component_callbacks(self, app):

    def set_data(self, data):
        self.Table.set_data(data)
        self.df = data
