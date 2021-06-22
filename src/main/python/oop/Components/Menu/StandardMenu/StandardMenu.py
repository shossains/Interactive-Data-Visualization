import dash
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH
from dash_oop_components import DashComponent
from src.main.python.oop.Components.ClientCode.ClientCode import example_function1
from src.main.python.oop.Components.Menu.StandardMenu.NestedFiltering import NestedFiltering


class StandardMenu(DashComponent):

    def __init__(self, plot_factory, df, title="Standard menu"):
        """
        Plot function of basic plot options for graphs
        :param plot_factory: Factory with all plot functions
        :param df: Dataframe with all data
        :param title: Title of the page
        """
        super().__init__(title=title)
        self.plot_factory = plot_factory
        self.df = df
        self.original_data = df
        self.NestedFiltering = NestedFiltering(plot_factory, df, "Nested filtering")
        self.totalButtons = 10
        self.plot_factory.show_table(self.df, True)

    def layout(self, params=None):
        """
               Shows the html layout of the Standard menu. Parameters are also passed through
               :param params: Parameters selected at the current level of the dashboard.
               :return: Html layout of the program.
        """
        buttons = html.Div([])
        for i in range(1, self.totalButtons + 1):
            if i <= 3:
                buttons.children.append(
                    html.Button('Graph {}'.format(i), id={'type': 'graph-button', 'index': i}, n_clicks=0,
                                className='graph-visible',
                                style={}))
            else:
                buttons.children.append(
                    html.Button('Graph {}'.format(i), id={'type': 'graph-button', 'index': i}, n_clicks=0,
                                className='graph-hidden',
                                style={}))
        page = dbc.Container([
            # Only for styling, spaces out selectors
            dbc.Row(html.Br()),
            dbc.Row(className="line-above"),
            dbc.Row(html.H5("Select")),
            dbc.Row(html.H6("File(s)")),
            html.Div([
                self.querystring(params)(dcc.Dropdown)(
                    id='select-file',
                    placeholder='Select ...',
                    multi=True,
                    className='multi-dropdown',
                ),
                dcc.Store(id='file-name')
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.H6("x-axis"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-variable-x-normal-plot',
                            placeholder='Select ...',
                            clearable=False,
                            className='dropdown',
                        )
                    ])
                    , className='dropdrown-graph'
                ),
                dbc.Col(
                    html.Div([
                        html.H6("y-axis"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-variable-y-normal-plot',
                            placeholder='Select ...',
                            clearable=False,
                            className='dropdown',
                        )
                    ])
                    , className='dropdrown-graph'
                )]),
            dbc.Row(html.Br()),
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.H6("color label"),
                        self.querystring(params)(dcc.Dropdown)(
                            id='select-characteristics-normal-plot',
                            placeholder='Select ...',
                            clearable=False,
                            className='dropdown',
                        )
                        # multi=True
                    ])
                    , className='dropdrown-graph'
                ),
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
                                                               persistence_type='memory',
                                                               className='dropdown',
                                                               )
                    ])
                    , className='dropdrown-graph'
                ),
            ]),

            # Empty space between main menu and filter menu
            dbc.Row(html.Br()),
            dbc.Row(className="line-above"),
            dbc.Row(html.H5("Manipulate data")),
            # Nested filtering
            self.NestedFiltering.layout(params),

            dbc.Row([dbc.Col(html.Div(id='error-message'))]),

            # -----------------------------------------------------------------------------------------------------------------------------
            # CLIENT CODE BUTTON HTML LAYOUT
            # Buttons for client code. Client can change name and texts of these buttons and add new buttons to extend functionality.
            # Look at update_processed_data to add functionality of the new buttons
            #
            # TODO: For a new button add: html.Button("Example show text", id="new_button_id", n_clicks=0, className='clientcode')

            dbc.Row(html.Br()),
            dbc.Row(html.H6("Manipulate data with custom function")),
            dbc.Row([
                    html.Button("Add new column (example)", id="example-function-1-button", n_clicks=0,
                                className='clientcode'),
                    #  Add new button here:
                    html.P(id="data-process-dummy"),
            ]),
            # ------------------------------------------------------------------------------------------------------------------------------

            dbc.Row(html.Br()),
            dbc.Row(html.H6("Reset data")),
            dbc.Row([
                html.Button("Reset to original data", id="reset-button", n_clicks=0, className='clientcode')
            ]),

            dbc.Row(html.Br()),
            dbc.Row(className="line-above"),
            dbc.Row(html.H5("Plot on")),

            # Plot buttons
            dbc.Row(dbc.Col(buttons)),

            # Empty space for styling
            dbc.Row(html.Br()),

            dcc.Checklist(id='plot-selection', options=[{'label': 'Plot selected data', 'value': 'plot-selection'}],
                          className='show-table'),

            # Empty space for styling
            dbc.Row(html.Br()),

            dbc.Row([
                dbc.Col(
                    html.Button('Graph++', id='add-graph', n_clicks=3, className='add-graph', style={})
                ),
                dbc.Col(
                    html.Button('Graph--', id='remove-graph', n_clicks=4, className='remove-graph', style={}),
                )
            ]),

            dbc.Row(html.Div(id='select-dimensions-normal-plot')),
            # Empty space for styling
            dbc.Row(html.Br()),
            dbc.Row(
                dcc.Checklist(id='show-table', options=[{'label': ' Show table', 'value': 'show-table'}], className='show-table'),
            )

        ], fluid=True)

        return page

    def component_callbacks(self, app):
        """
               Automatically does the callbacks of the interactive parts of the dashboard main components.
               :param app: Dash app that uses the code
               :return: Output of the callback functions.
        """

        @app.callback([Output('data-process-dummy', 'value'),
                       Output('error-message', 'children')],
                      [
                          Input('example-function-1-button', 'n_clicks'),
                          Input('reset-button', 'n_clicks'),
                          Input('apply-filter-button', 'n_clicks'),
                          Input('query', 'value')
                      ])
        def update_processed_data(example_button, reset_button, apply_button, query):
            """
                When one of the buttons is clicked, the client code or filters are executed for that example. Makes a deep copy of
                original data and alters this data in return. Data is filtered or altered by client code or filter.

                TODO:To add back_end of a new button for client code:
                    - Import clients new method from src.main.python.oop.Components.ClientCode.ClientCode
                    - At @app.callback add at the bottom of the inputs.:
                        Input('id_of_new_button', 'n_clicks'),
                    - Add the new Input at the inputs of the update_processed_data. For example:
                        def update_processed_data(button1, reset_button, apply, query, new_input):
                    - Add functionality of the new button to the method as one of the elif statements:
                                 elif 'id_of_new_button' in changed_id:
                                        try:
                                            self.df = function_name_in_client_code(self.df)
                                            self.NestedFiltering.set_data(self.df)
                                            query_message = html.Div('Client function successfully applied to data.')
                                        except Exception as e:
                                            query_message = html.Div(
                                                [html.Div('Error with client code: {}.'.format(query), style=self.ErrorMessageStyle),
                                                 html.Div('Error: {}.'.format(e), style=self.ErrorMessageStyle),
                                                 html.Div('Data reset to original data.')])

                The back-end of the new button is now added to the GUI.

                :param example_button: When pressed, Example client function is used
                :param reset_button: When pressed, resets data to original data
                :param apply_button: When pressed, applies the query on self.df
                :param query: Filter recieved in query form from the NestedFiltering.py
                :return data-process-dummy: if 'true' query filter is used if empty not.
                :return error-message: Returns error message when filter or client code can't be applied.
            """
            query_message = ''
            if self.df is None:
                return '', query_message

            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
            if 'example-function-1-button' in changed_id:
                try:
                    self.df = example_function1(self.df)
                    self.NestedFiltering.set_data(self.df)
                    query_message = html.Div('Client function successfully applied to data.', className='message')

                except Exception as e:
                    query_message = html.Div(
                        [html.Div('Error with client code: {}.'.format(query), className='error-message'),
                         html.Div('Error: {}.'.format(e), className='error-message'),
                         html.Div('Data reset to original data.', className='message')])

            elif 'reset-button' in changed_id:
                self.df = self.original_data
                self.NestedFiltering.set_data(self.df)
                query_message = html.Div('Data reset to original data.', className='message')

            elif 'apply-filter-button' in changed_id:
                try:
                    self.df = self.df.query(query)
                    query_message = html.Div('filters successfully applied to data.', className='message')

                except Exception as e:
                    query_message = html.Div(
                        [html.Div('Error with query: {}.'.format(query), className='error-message'),
                         html.Div('Error: {}.'.format(e), className='error-message'),
                         html.Div('Data reset to original data.', className='message')])
                    self.df = self.original_data
                return 'true', query_message

            return '', query_message

        @app.callback([Output('select-variable-x-normal-plot', 'options'),
                       Output('select-variable-y-normal-plot', 'options'),
                       Output('select-characteristics-normal-plot', 'options'),
                       ],
                      [
                          Input('file-name', 'data'),
                          Input('data-process-dummy', 'value'),
                      ])
        def set_options_variable(file_name, data_process_dummy):
            """
            Loads in possible parameters for the x and y-axis in dropdown from the data.
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

                return labels, labels, colorLabel
            else:
                return labels, labels, labels

        @app.callback([Output('select-variable-x-normal-plot', 'value'),
                       Output('select-variable-y-normal-plot', 'value'),
                       Output('select-characteristics-normal-plot', 'value'),
                       ],
                      [
                          Input('file-name', 'data'),
                      ],
                      [
                          State('select-variable-x-normal-plot', 'options'),
                          State('select-variable-y-normal-plot', 'options'),
                          State('select-characteristics-normal-plot', 'options'),
                      ])
        def set_variables(file_dummy, options_x, options_y, options_char):
            """
            Gets the first option and displays it as the dropdown of the 'select-variable-x-normal-plot' and 'select-variable-y-normal-plot'.
            :param file_dummy: Non used input, but used as sign to use method
            :param options_x: All possible x-axis options
            :param options_y: All possible x-axis options
            :param options_char: All possible characteristic options
            :return: The chosen x-axis and y-axis and characteristic
            """
            if options_y is None or options_x is None or options_char is None:
                return None, None, None
            if len(options_y) <= 0 or (len(options_x) <= 0) or (len(options_char) <= 0):
                return None, None, None
            return options_x[0]['value'], options_y[0]['value'], options_char[0]['value']

        for i in range(1, self.totalButtons):
            @app.callback(Output({'type': 'graph-button', 'index': i}, 'style'),
                          Output({'type': 'graph-content', 'index': i}, 'style'),
                          Input('add-graph', 'n_clicks'),
                          Input('remove-graph', 'n_clicks'),
                          State({'type': 'graph-button', 'index': i}, 'style'),
                          State({'type': 'graph-content', 'index': i}, 'style'))
            def add_graph(n_clicks_add, n_clicks_remove, buttonstyle, graphstyle, c=i):
                """
                Make one more button and graph appear after Graph++ has been clicked.
                :param n_clicks_add: Number of clicks when add graph is pressed.
                :param n_clicks_remove: Number of clicks when remove graph is pressed. 
                :param buttonstyle: CSS Style of the buttons
                :param graphstyle: CSS style of the graph
                :param c: Number of graphs
                :return graph-button: Style of the graph button
                :return graph-content: Style of the graph
                """""
                ctx = dash.callback_context

                if not ctx.triggered:
                    print("entered but no trigger")

                if ctx.triggered[0]['prop_id'].split('.')[0] == 'add-graph':
                    if n_clicks_add >= c:
                        buttonstyle['display'] = 'initial'
                        graphstyle['display'] = 'block'

                elif ctx.triggered[0]['prop_id'].split('.')[0] == 'remove-graph':
                    if n_clicks_remove <= c:
                        buttonstyle['display'] = 'none'
                        graphstyle['display'] = 'none'

                return buttonstyle, graphstyle

        @app.callback(Output({'type': 'graph-content', 'index': MATCH}, 'figure'),
                      Input({'type': 'graph-button', 'index': MATCH}, 'n_clicks'),
                      State('select-variable-x-normal-plot', 'value'),
                      State('select-variable-y-normal-plot', 'value'),
                      State('select-characteristics-normal-plot', 'value'),
                      State('select-plot-options-normal-plot', 'value'),
                      State({'type': 'graph-content', 'index': MATCH}, 'figure'),
                      State('plot-selection', 'value'),
                      State('main_table', 'selected_rows')
                      , prevent_initial_call=True)
        def plot_graph(n_clicks_graph_button, xvalue, yvalue, color_based_characteristic, plot_type, figure, plotSelection, selectedRows):
            """
            Updates a graph with altered data by filters and client code. The graph can be displayed in a number of different ways.
            :param n_clicks_graph_button: Number of times the graph button is pressed. This is the sign to update the current graphs.
            :param xvalue: Selected x-axis value in the data
            :param yvalue: Selected y-axis value in the data
            :param color_based_characteristic: Selected characteristic of the data
            :param plot_type: Selected kind of plot 'scatter', 'density' etc.
            :param figure: Selected figure wich needs to be updated
            :return: Graph object with the displayed plot
            """
            title = figure['layout']['title']['text']

            if plotSelection:
                print(selectedRows)

                df2 = self.df.iloc[selectedRows]
                return self.plot_factory.graph_methods(df2, xvalue, yvalue, color_based_characteristic, plot_type,
                                                       title)
            else:
                if xvalue is None or yvalue is None or color_based_characteristic is None or self.df is None:
                    return figure
                if xvalue == "select" or yvalue == "select" or color_based_characteristic == "select" or plot_type == "select":
                    return figure

                return self.plot_factory.graph_methods(self.df, xvalue, yvalue, color_based_characteristic, plot_type,
                                                       title)

        @app.callback(Output('add-graph', 'n_clicks'),
                      Output('remove-graph', 'n_clicks'),
                      Input('add-graph', 'n_clicks'),
                      Input('remove-graph', 'n_clicks'))
        def button_cap(n_clicks_add, n_clicks_remove):
            """
            Resets the number of clicks of each button to the current amount of graphs.
            :param n_clicks_add: Number of times the add graph button is pressed
            :param n_clicks_remove: Number of times the remove graph button is pressed
            :return:
            """
            ctx = dash.callback_context

            if ctx.triggered[0]['prop_id'].split('.')[0] == 'add-graph':
                n_clicks_remove = n_clicks_add + 1
                if n_clicks_add >= self.totalButtons:
                    n_clicks_add = self.totalButtons - 1
                    n_clicks_remove = self.totalButtons

            if ctx.triggered[0]['prop_id'].split('.')[0] == 'remove-graph':
                n_clicks_add = n_clicks_add - 1
                n_clicks_remove = n_clicks_add + 1

                if n_clicks_remove <= 2:
                    n_clicks_remove = 2
                if n_clicks_add <= 1:
                    n_clicks_add = 1

            return n_clicks_add, n_clicks_remove

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
            :param select_file: Shows the selected file(s)
            :return: Table
            """
            if select_file is None:
                return "No file selected"
            else:
                return self.plot_factory.show_table(self.df, showtable)

    def set_data(self, data):
        """
        Method to pass through data to StandardMenu from other classes. Also sets data of the NestedFiltering class.
        :param data: Pandas list of dataframes that is passed through
        :return: No return
        """
        self.df = data
        self.original_data = data
        self.NestedFiltering.set_data(data)
