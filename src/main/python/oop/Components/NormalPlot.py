__all__ = ['Dashboard']

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp
from src.main.python.oop.Figure_factories import FigureFactories


class NormalPlot(DashComponent):
    def __init__(self, plot_factory, df, title="Example ML"):
        super().__init__(title=title)
        self.plot_factory = FigureFactories.FigureFactories()
        self.df = df

    def layout(self, params=None):
        page = dbc.Container([
            # Only for styling, spaces out selectors
            dbc.Row(html.Br()),
            dbc.Row(html.H5("Main Graph")),
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.H6("Select variable x"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-variable-x-normal-plot',
                            placeholder='Select ...')
                    ])
                ),
                dbc.Col(
                    html.Div([
                        html.H6("Select variable y"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-variable-y-normal-plot',
                            placeholder='Select ...')
                    ])
                ),
                dbc.Col(
                    html.Div([
                        html.H6("Color based on"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-characteristics-normal-plot',
                            placeholder='Select ...')
                        # multi=True
                    ])
                ),
                dbc.Col(
                    html.Div([
                        html.H6("Select plot method"),
                        self.querystring(params)(dcc.Dropdown)(id='select-plot-options-normal-plot',
                                                               options=[
                                                                   {'label': 'Area', 'value': 'area'},
                                                                   {'label': 'Bar', 'value': 'bar'},
                                                                   {'label': 'Box', 'value': 'box'},
                                                                   {'label': 'Density', 'value': 'density'},
                                                                   {'label': 'Histogram', 'value': 'histogram'},
                                                                   {'label': 'Line', 'value': 'line'},
                                                                   {'label': 'Scatter', 'value': 'scatter'},
                                                               ],
                                                               value='scatter')
                    ])
                )
            ]),
            # Only for styling, spaces out selectors
            dbc.Row(html.Br()),
            dbc.Row(html.H5("Subgraph")),
            dbc.Row(
                dbc.Col(
                    html.Div([
                        html.H6("Select subgraph features"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-dimensions-normal-plot',
                            placeholder='Select ...',
                            multi=True
                        )
                    ])
                ),
            ),
            dbc.Row([
                dbc.Col(
                    dcc.Loading(
                        id="loading-icon-normal-plot",
                        children=[html.Div(
                            dcc.Graph(
                                id='Mygraph-normal-plot'
                            ),
                        )],
                        type="circle"
                    ),

                ),

                dbc.Col(
                    dcc.Loading(
                        id="loading-icon2-normal-plot",
                        children=[html.Div(
                            dcc.Graph(
                                id='Subgraph-normal-plot'
                            ),
                        )],
                        type="circle"
                    )
                )
            ]),
        ], fluid=True)
        return page

    def component_callbacks(self, app):
        @app.callback(Output('Mygraph-normal-plot', 'figure'), [
            Input('select-variable-x-normal-plot', 'value'),
            Input('select-variable-y-normal-plot', 'value'),
            Input('select-characteristics-normal-plot', 'value'),
            Input('select-plot-options-normal-plot', 'value'),
        ])
        def update_graph(xvalue, yvalue, options_char, plotvalue):
            if xvalue is None or yvalue is None or options_char is None:
                return {}
            if xvalue == "index" or yvalue == "index" or options_char == "index":
                return {}

            return self.plot_factory.graph_methods(self.df, xvalue, yvalue, options_char, plotvalue)

        @app.callback(Output('Subgraph-normal-plot', 'figure'), [
            Input('select-characteristics-normal-plot', 'value'),
            Input('select-dimensions-normal-plot', 'value'),
        ])
        def update_subgraph(options_char, dims):
            return self.plot_factory.subgraph_methods(self.df, options_char, dims)

        @app.callback([Output('select-variable-x-normal-plot', 'options'),
                       Output('select-variable-y-normal-plot', 'options'),
                       Output('select-characteristics-normal-plot', 'options'),
                       Output('select-dimensions-normal-plot', 'options')],
                      [
                          Input('dummy', 'children')
                      ])
        def set_options_variable(dummy):
            """
            loads in possible parameters for the x and y-axis from the data.
            :param dummy: dummy html property
            :return: Possible options for dropdown x-axis.
            """
            dataframe = self.df.reset_index()
            return [{'label': i, 'value': i} for i in dataframe.columns], [{'label': i, 'value': i} for i in
                                                                           dataframe.columns], [
                       {'label': i, 'value': i} for i in dataframe.columns], [{'label': i, 'value': i} for i in
                                                                              dataframe.columns]

        @app.callback([Output('select-variable-x-normal-plot', 'value'),
                       Output('select-variable-y-normal-plot', 'value'),
                       Output('select-characteristics-normal-plot', 'value'),
                       Output('select-dimensions-normal-plot', 'value')
                       ],
                      [
                          Input('select-variable-x-normal-plot', 'options'),
                          Input('select-variable-y-normal-plot', 'options'),
                          Input('select-characteristics-normal-plot', 'options'),
                          Input('select-dimensions-normal-plot', 'options')
                      ])
        def set_variables(options_x, options_y, options_char, dims):
            """
            Gets the ouput of the dropdown of the 'select-variable-x' and 'select-variable-y'.
            :param options_x: All possible x-axis options
            :param options_y: All possible x-axis options
            :param options_char: All possible characteristic options
            :return: The choosen x-axis and y-axis and characteristic
            """
            if (options_y is None or options_x is None or options_char is None or dims is None):
                return None, None, None, None
            if len(options_y) <= 0 or (len(options_x) <= 0) or (len(options_char) <= 0) or (len(dims) <= 0):
                return None, None, None, None
            return options_x[0]['value'], options_y[0]['value'], options_char[0]['value'], None

    def set_data(self, data):
        self.df = data
