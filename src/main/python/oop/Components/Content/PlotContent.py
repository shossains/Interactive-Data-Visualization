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
        self.totalButtons = 10
        self.plot_factory = plot_factory
        self.df = df
        self.IdTitlePair = ["id", "title"]

    def layout(self, params=None):
        graphs = html.Div([])

        for i in range(1, self.totalButtons+1):
            if i <= 3:
                graphs.children.append(dbc.Row(
                    dbc.Col(
                        dcc.Loading(
                            id="loading-icon-normal-plot",
                            children=[dcc.Graph(
                                figure={'layout': { 'title': 'Graph {}'.format(i)}},
                                id={'type': 'graph-content', 'index': i},
                                config={
                                    'autosizable': True,
                                    "displaylogo": False,
                                    "showTips": True,
                                    "showAxisDragHandles": True,
                                    "scrollZoom": True,
                                    'edits': {'titleText': True}
                                },
                                style={
                                    'display': 'block',
                                    'width': '100%'
                                }
                            )],
                        type='graph')
                    )
                ))
            else:
                graphs.children.append(dbc.Row(
                    dbc.Col(
                        dcc.Loading(
                            id="loading-icon-normal-plot",
                            children=[
                                dcc.Graph(
                                    figure={'layout': {'title': 'Graph {}'.format(i)}},
                                    id={'type': 'graph-content', 'index': i},
                                    config={
                                        'autosizable': True,
                                        "displaylogo": False,
                                        "showTips": True,
                                        "showAxisDragHandles": True,
                                        "scrollZoom": True,
                                        'edits': {'titleText': True}
                                    },
                                    style={
                                        'display': 'none',
                                        'width': '100%'
                                    }
                                )],
                        type='graph')
                    )
                ))

        page = dbc.Container([
            graphs,
            dbc.Row(
                dbc.Col(
                    html.Div(self.Table.layout(params))
                )
            )

        ], fluid=True)
        return page

    # def component_callbacks(self, app):

    def set_data(self, idTitlePair):
        self.IdTitlePair = idTitlePair