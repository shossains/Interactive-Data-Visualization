__all__ = ['Dashboard']

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp
from src.main.python.oop.Figure_factories import FigureFactories
from src.main.python.oop.Components.ClientCode.ClientCode import example_function1, example_function2


class ProcessDataTool(DashComponent):

    def __init__(self, plot_factory, df, title="Normal plot"):
        """
        Plot function of basic plot options with graph and subgraph
        :param plot_factory: Factory with all plot functions
        :param df: Dataframe with all data
        :param title: Title of the page
        """
        super().__init__(title=title)
        self.plot_factory = plot_factory
        self.df = df

    def layout(self, params=None):
        """
               Shows the html layout of the Normal plot. Parameters are also passed through
               :param params: Parameters selected at the current level of the dashboard.
               :return: Html layout of the program.
        """
        page = dbc.Container([
            # Only for styling, spaces out selectors
            dbc.Row(html.Br()),
            dbc.Row(html.H5("Selected Graph")),
            # client back end code part for selected data
            dbc.Row([
                html.Br(),
                html.H6("Calculate selected data with back-end formula's")
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Button("example function 1", id="example-function-1-button", n_clicks=0)
                    ])
                ]),
                dbc.Col([
                    html.Div([
                        html.Button("example function 2", id="example-function-2-button", n_clicks=0)
                    ])
                ])
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.H6("Select variable x"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-variable-x-processed-plot',
                            placeholder='Select ...'),
                    ])
                ),
                dbc.Col(
                    html.Div([
                        html.H6("Select variable y"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-variable-y-processed-plot',
                            placeholder='Select ...')
                    ])
                ),
                dbc.Col(
                    html.Div([
                        html.H6("Color based on"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-characteristics-processed-plot',
                            placeholder='Select ...')
                        # multi=True
                    ])
                ),
                dbc.Col(
                    html.Div([
                        html.H6("Select plot method"),
                        self.querystring(params)(dcc.Dropdown)(id='select-plot-options-processed-plot',
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
                ),

            ]),
            # Only for styling, spaces out selectors
            dbc.Row([
                dbc.Col(
                    dcc.Loading(
                        id="loading-icon-processed-plot",
                        children=[html.Div(
                            dcc.Graph(
                                id='processed-plot'
                            ),
                        )],
                        type="circle"
                    ),

                )
            ])
        ], fluid=True)
        return page

    def component_callbacks(self, app):
        """
               Automatically does the callbacks of the interactive parts of the dashboard main components.
               :param app: Dash app that uses the code
               :return: Output of the callback functions.
        """

        @app.callback(Output('processed-plot', 'figure'), [
            Input('select-variable-x-processed-plot', 'value'),
            Input('select-variable-y-processed-plot', 'value'),
            Input('select-characteristics-processed-plot', 'value'),
            Input('select-plot-options-processed-plot', 'value'),
            Input('example-function-1-button', 'n_clicks'),
            Input('example-function-2-button', 'n_clicks'),
        ])
        def processed_graph(xvalue, yvalue, options_char, plotvalue, button1, button2):
            if xvalue is None or yvalue is None or options_char is None or self.df is None:
                return {}
            if xvalue == "select" or yvalue == "select" or options_char == "select" or plotvalue == "select":
                return {}

            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
            if 'example-function-1-button' in changed_id:
                dataframe = example_function1(self.df)
            elif 'example-function-2-button' in changed_id:
                dataframe = example_function2(self.df)
            else:
                dataframe = self.df

            return self.plot_factory.graph_methods(dataframe, xvalue, yvalue, options_char, plotvalue)

        @app.callback([Output('select-variable-x-processed-plot', 'options'),
                       Output('select-variable-y-processed-plot', 'options'),
                       Output('select-characteristics-processed-plot', 'options')],
                      [
                          Input('dummy', 'children')
                      ])
        def set_options_variable(dummy):
            """
            loads in possible parameters for the x and y-axis in dropdown from the data.
            :param dummy: dummy html property
            :return: Possible options for dropdown x-axis.
            """
            labels = [{'label': 'Select', 'value': 'select'}]

            if self.df is not None:
                dataframe = self.df
                colorlabel = [{'label': 'Select', 'value': 'select'}, {'label': 'No color', 'value': 'no-color'}]

                for i in dataframe.columns:
                    labels = labels + [{'label': i, 'value': i}]
                    colorlabel = colorlabel + [{'label': i, 'value': i}]

                return labels, labels, colorlabel
            else:
                return labels, labels, labels

        @app.callback([Output('select-variable-x-processed-plot', 'value'),
                       Output('select-variable-y-processed-plot', 'value'),
                       Output('select-characteristics-processed-plot', 'value'),
                       ],
                      [
                          Input('select-variable-x-processed-plot', 'options'),
                          Input('select-variable-y-processed-plot', 'options'),
                          Input('select-characteristics-processed-plot', 'options'),
                      ])
        def set_variables(options_x, options_y, options_char):
            """
            Gets the first option and displays it as the dropdown of the 'select-variable-x' and 'select-variable-y'.
            :param options_x: All possible x-axis options
            :param options_y: All possible x-axis options
            :param options_char: All possible characteristic options
            :return: The choosen x-axis and y-axis and characteristic
            """
            if options_y is None or options_x is None or options_char is None:
                return None, None, None
            if len(options_y) <= 0 or (len(options_x) <= 0) or (len(options_char) <= 0):
                return None, None, None
            return options_x[0]['value'], options_y[0]['value'], options_char[0]['value']

    def set_data(self, data):
        self.df = data
