import dash
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash_oop_components import DashComponent, DashFigureFactory, DashComponent, DashComponentTabs, DashApp
from src.main.python.oop.Components.ClientCode.ClientCode import example_function2, example_function1
from src.main.python.oop.Components.Menu.StandardMenu.NestedFiltering import NestedFiltering

class StandardMenu(DashComponent):

    def __init__(self, plot_factory, df, title="Standard menu"):
        """
        Plot function of basic plot options with graph and subgraph
        :param plot_factory: Factory with all plot functions
        :param df: Dataframe with all data
        :param title: Title of the page
        """
        super().__init__(title=title)
        self.plot_factory = plot_factory
        self.df = df
        self.original_data = df
        self.NestedFiltering = NestedFiltering(plot_factory, df, "Nested filtering")
        self.buttonstyle = {
            'borderWidth': '1px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'background-color': '#5ebfff',
            'color': 'white',
            "margin-left": "15px",
            "margin-right": "15px"
        }
        self.dropdownstyle = {
            'padding-left': '5px',
            'padding-right': '5px'
        }

    def layout(self, params=None):
        """
               Shows the html layout of the Standard menu. Parameters are also passed through
               :param params: Parameters selected at the current level of the dashboard.
               :return: Html layout of the program.
        """
        page = dbc.Container([
            # Only for styling, spaces out selectors
            dbc.Row(html.Br()),
            dbc.Row(html.H5("Select files to project")),
            html.Div([
                self.querystring(params)(dcc.Dropdown)(
                    id='select-file',
                    placeholder='Select ...',
                    multi = True
                ),
                dcc.Store(id='file-name')
            ]),
            dbc.Row(html.Br()),
            dbc.Row(html.H5("Main Graph")),
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.H6("x-axis"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-variable-x-normal-plot',
                            placeholder='Select ...',
                            clearable=False)
                    ])
                    , style=self.dropdownstyle),
                dbc.Col(
                    html.Div([
                        html.H6("y-axis"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-variable-y-normal-plot',
                            placeholder='Select ...',
                            clearable=False)
                    ])
                    , style=self.dropdownstyle)]),
            dbc.Row(html.Br()),
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.H6("color label"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-characteristics-normal-plot',
                            placeholder='Select ...',
                            clearable=False)
                        # multi=True
                    ])
                    , style=self.dropdownstyle),
                dbc.Col(
                    html.Div([
                        html.H6("plot method"),
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
                                                               value='scatter', clearable=False,
                                                               persistence_type='memory')
                    ]),
                    style=self.dropdownstyle
                ),
            ]),

            #Empty space between main menu and filter menu
            dbc.Row(html.Br()),

            # Nested filtering
            self.NestedFiltering.layout(params),
            # Buttons for client code. Client can change name and texts of these buttons and add new buttons to extend code. Look at update_processed_data to add functionality of the new buttons
            dbc.Row(html.Br()),
            dbc.Row(html.H5("Process data with client code")),
            dbc.Row([
                html.Div([
                    html.Button("Add new column (example)", id="example-function-1-button", n_clicks=0,
                                style=self.buttonstyle),
                    html.Button("add two new columns (example)", id="example-function-2-button", n_clicks=0,
                                style=self.buttonstyle),
                    html.Button("reset to original data", id="reset-button", n_clicks=0, style=self.buttonstyle)
                ]),
                html.P(id="data-process-dummy"),
            ]),

            # Only for styling, spaces out selectors
            dbc.Row(html.Br()),
            dbc.Row(html.H5("Subgraph")),
            dbc.Row(
                dbc.Col(
                    html.Div([
                        html.H6("features"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-dimensions-normal-plot',
                            placeholder='Select ...',
                            multi=True
                        )
                    ])
                    , style={"padding-left": "5px", "padding-right": "5px"}),
            ),
            dbc.Row(
                dcc.Checklist(id='show-table', options=[{'label': 'Show table', 'value': 'show-table'}]),
            )

        ], fluid=True)

        return page

    def component_callbacks(self, app):
        """
               Automatically does the callbacks of the interactive parts of the dashboard main components.
               :param app: Dash app that uses the code
               :return: Output of the callback functions.
        """

        @app.callback(
            Output(component_id='output-data-upload', component_property='style'),
            [Input(component_id='show-table', component_property='value')])
        def show_hide_table(visibility_state):
            """
            Shows or hides the table. Only loads in the data when checkbox selected.
            :param visibility_state:
            :return: visibility style
            """
            if visibility_state == ['show-table']:
                return {'display': 'block'}
            else:
                return {'display': 'none'}

        @app.callback(Output('output-data-upload', 'children'),
                      [
                          Input('show-table', 'value'),
                          Input('select-file', 'value')
                      ])
        def update_table(showtable, select_file):
            """
            Updates table and calls plot_factory show table
            :param showtable: Checkbox if marked shows table else it won't.
            :return: Table
            """
            return self.plot_factory.show_table(self.df, showtable)

        @app.callback(Output('Mygraph-normal-plot', 'figure'), [
            Input('select-variable-x-normal-plot', 'value'),
            Input('select-variable-y-normal-plot', 'value'),
            Input('select-characteristics-normal-plot', 'value'),
            Input('select-plot-options-normal-plot', 'value'),
            Input('data-process-dummy', 'value'),
        ], State('query', 'value'))
        def update_graph(xvalue, yvalue, color_based_characteristic, plot_type, data_process_dummy, query):
            """
            Updates a normal graph with different options how to plot.

            :param data_process_dummy:
            :param xvalue: Selected x-axis value in the data
            :param yvalue: Selected y-axis value in the data
            :param color_based_characteristic: Selected characteristic of the data
            :param plot_type: Selected kind of plot 'scatter', 'density' etc.
            :param query: Query for filtering data
            :return: Graph object with the displayed plot
            """
            if xvalue is None or yvalue is None or color_based_characteristic is None or self.df is None:
                return {}
            if xvalue == "select" or yvalue == "select" or color_based_characteristic == "select" or plot_type == "select":
                return {}

            if query and data_process_dummy == 'true':
                dataframe = self.df.query(query)
            else:
                dataframe = self.df.reset_index()

            return self.plot_factory.graph_methods(dataframe, xvalue, yvalue, color_based_characteristic, plot_type)

        @app.callback(Output('Subgraph-normal-plot', 'figure'), [
            Input('select-characteristics-normal-plot', 'value'),
            Input('select-dimensions-normal-plot', 'value'),
            Input('data-process-dummy', 'children'),
        ])
        def update_subgraph(options_char, dims, data_process_dummy):
            """
            Updates subgraphs based on new options.
            :param data_process_dummy: just there as a dummy to trigger callback.
            :param options_char: Selected characteristic of the data
            :param dims: Multiple dimensions that are chosen
            :return: subgraph
            """
            if dims is None or dims == 'select' or self.df is None:
                return {}

            dataframe = self.df.reset_index()
            return self.plot_factory.subgraph_methods(dataframe, options_char, dims)

        @app.callback([Output('select-variable-x-normal-plot', 'options'),
                       Output('select-variable-y-normal-plot', 'options'),
                       Output('select-characteristics-normal-plot', 'options'),
                       Output('select-dimensions-normal-plot', 'options'),
                       ],
                      [
                          Input('file-name', 'data'),
                          Input('data-process-dummy', 'children'),
                      ])
        def set_options_variable(file_name, data_process_dummy):
            """
            loads in possible parameters for the x and y-axis in dropdown from the data.
            :param data_process_dummy: just there as a dummy to trigger callback.
            :param file_name: intermediate-value
            :return: Possible options for dropdown x-axis.
            """
            labels = []

            if self.df is not None:
                if self.df.columns is not None:
                    labels = [{'label': '', 'value': 'select'}]

                if 'row_index_label' in self.df.columns:
                    del self.df['row_index_label']

                row_labels = np.arange(0, self.df.shape[0], 1)
                self.df.insert(0, 'row_index_label', row_labels)

                dataFrame = self.df
                colorLabel = [{'label': '', 'value': 'select'}, {'label': 'No color', 'value': 'no-color'}]

                for i in dataFrame.columns[1::]:
                    labels = labels + [{'label': i, 'value': i}]
                    colorLabel = colorLabel + [{'label': i, 'value': i}]

                return labels, labels, colorLabel, labels
            else:
                return labels, labels, labels, labels

        @app.callback([Output('select-variable-x-normal-plot', 'value'),
                       Output('select-variable-y-normal-plot', 'value'),
                       Output('select-characteristics-normal-plot', 'value'),
                       Output('select-dimensions-normal-plot', 'value'),
                       ],
                      [
                          Input('select-variable-x-normal-plot', 'options'),
                          Input('select-variable-y-normal-plot', 'options'),
                          Input('select-characteristics-normal-plot', 'options'),
                          Input('select-dimensions-normal-plot', 'options')
                      ])
        def set_variables(options_x, options_y, options_char, dims):
            """
            Gets the first option and displays it as the dropdown of the 'select-variable-x' and 'select-variable-y'.
            :param options_x: All possible x-axis options
            :param options_y: All possible x-axis options
            :param options_char: All possible characteristic options
            :return: The chosen x-axis and y-axis and characteristic
            """
            if options_y is None or options_x is None or options_char is None or dims is None:
                return None, None, None, None
            if len(options_y) <= 0 or (len(options_x) <= 0) or (len(options_char) <= 0) or (len(dims) <= 0):
                return None, None, None, None
            return options_x[0]['value'], options_y[0]['value'], options_char[0]['value'], None

        @app.callback(Output('data-process-dummy', 'value'), [
            Input('example-function-1-button', 'n_clicks'),
            Input('example-function-2-button', 'n_clicks'),
            Input('reset-button', 'n_clicks'),
            Input('apply-filter-button', 'n_clicks'),
        ])
        def update_processed_data(button1, button2, reset_button, apply):
            """
                When one of the buttons is clicked, the client code is executed for that example. Makes a deep copy of
                original data and alters this data in return.
                :param button1: Activates example 1
                :param button2: Activates example 2
                :param reset_button: Reset to original data
                :return: Nothing.
            """
            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
            if 'example-function-1-button' in changed_id:
                self.df = example_function1(self.df)
            elif 'example-function-2-button' in changed_id:
                self.df = example_function2(self.df)
            elif 'reset-button' in changed_id:
                self.df = self.original_data
            elif 'apply-filter-button' in changed_id:
                return 'true'

            return ''

    def get_data(self, data):
        self

    def set_data(self, data):
        self.df = data
        self.original_data = data
        self.NestedFiltering.set_data(data)
