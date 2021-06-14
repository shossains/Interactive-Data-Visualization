import dash
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp


class NestedFiltering(DashComponent):

    def __init__(self, plot_factory, df, title="Nested Filtering"):
        """
        Nestedfiltering gives the ability to add and remove filters and use the filters on the current data.
        :param plot_factory: Factory with all plot functions
        :param df: Dataframe with all data
        :param title: Title of the page
        """
        super().__init__(title=title)
        self.plot_factory = plot_factory
        self.df = df
        self.original_data = df
        self.amount_filters = 0
        self.filters = []

    def layout(self, params=None):
        """
               Shows the html layout of the standard Nestedfiltering. REMARK: Parameters are not passed through
               :param params: Parameters selected at the current level of the dashboard.
               :return: Html layout of the program.
        """
        page = html.Div([
            dbc.Row(html.H5("Filtering")),
            html.Div(id="filters", children=[]),
            dbc.Row([
                dbc.Col(html.Div([
                    html.Button("Add filter", id="add-filter-button", n_clicks=0,
                                className='filter-button')])),
                dbc.Col(html.Div([
                    html.Button("Apply filter(s)", id="apply-filter-button", n_clicks=0,
                                className='filter-button')]))
            ])
            ,
            html.P(id="query")])
        return page

    def component_callbacks(self, app):
        """
               Automatically does the callbacks of the interactive parts of the dashboard main components.
               :param app: Dash app that uses the code
               :return: Output of the callback functions.
        """

        @app.callback(Output('filters', 'children'),
                      Output({'type': 'remove-filter-button', 'index': ALL}, 'n_clicks'),
                      Input('add-filter-button', 'n_clicks'),
                      Input({'type': 'remove-filter-button', 'index': ALL}, 'n_clicks'),
                      Input('file-name', 'data'),
                      State('filters', 'children')
                      )
        def add_remove_filter(add_filter_clicks, remove_filter_clicks, file_name_dummy, children):
            """
            Can remove and add filters dynamically.
            :param add_filter_clicks:  If add filter clicked, new filter is added
            :param remove_filter_clicks:  If remove filter clicked, selected filter is removed
            :param file_name_dummy: Called when file is selected
            :param children: html code of the current filters in the file
            :return: new children (filters).
            """
            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
            if 'add-filter-button' in changed_id:
                page = html.Div([
                    dbc.Row([
                        dbc.Col(
                            html.Div([
                                dcc.Dropdown(
                                    id={
                                        'type': 'query-label',
                                        'index': add_filter_clicks
                                    },
                                    placeholder='Select ...',
                                    clearable=False)
                            ])
                            , id='dropdrown-graph'),
                        dbc.Col(
                            html.Div([
                                dcc.Dropdown(
                                    id={
                                        'type': 'query-condition',
                                        'index': add_filter_clicks
                                    },
                                    placeholder='Select ...',
                                    options=[
                                        {'label': '==', 'value': '=='},
                                        {'label': '<', 'value': '<'},
                                        {'label': '>', 'value': '>'},
                                        {'label': '<=', 'value': '<='},
                                        {'label': '>=', 'value': '>='},
                                        {'label': '!=', 'value': '!='},
                                    ],
                                    clearable=False)
                            ])
                            , id='dropdown-graph'),
                    ]),
                    dbc.Row([
                        dbc.Col(
                            html.Div([
                                dbc.Row(html.H6("Query Filter")),
                                dcc.Input(id={
                                    'type': 'query-text_input',
                                    'index': add_filter_clicks},
                                    placeholder='Fill in your query',
                                    debounce=True),
                            ])
                        ),
                        dbc.Col(
                            html.Div([
                                html.Button("Remove filter",
                                            id={
                                                'type': "remove-filter-button",
                                                'index': add_filter_clicks},
                                            n_clicks=0,
                                            className='remove-filter'
                                            )
                            ])
                        ),
                    ]),
                    dbc.Row(html.Br())
                ], id={
                    'type': "filter-page",
                    'index': add_filter_clicks})

                children.append(page)

            elif 'remove-filter-button' in changed_id:
                index = remove_filter_clicks.index(1)
                del children[index]

            else:
                children = []

            return children, len(remove_filter_clicks) * [0]

        @app.callback(
            Output({'type': 'query-label', 'index': MATCH}, 'options'),
            [
                Input('file-name', 'data'),
                Input('data-process-dummy', 'value'),
            ])
        def options_query(data_selection_dummy, data_process_dummy):
            """
            Places all column options in query-label. Both dummies are used to activate function. Their data is not used
            :param data_selection_dummy: Called when file is selected
            :param data_process_dummy: Called when data is processed
            :return: Label options for query-label
            """
            if self.df is not None:
                if self.df.columns is not None:
                    labels = [{'label': '', 'value': 'select'}]

                if 'row_index_label' in self.df.columns:
                    del self.df['row_index_label']

                row_labels = np.arange(0, self.df.shape[0], 1)
                self.df.insert(0, 'row_index_label', row_labels)

                dataFrame = self.df

                for i in dataFrame.columns[1::]:
                    labels = labels + [{'label': i, 'value': i}]

                return labels
            else:
                return [{'label': 'no-label', 'value': 'no-label'}]

        @app.callback([Output({'type': 'query-label', 'index': MATCH}, 'value'),
                       ],
                      [
                          Input('file-name', 'data'),
                      ],
                      [State({'type': 'query-label', 'index': MATCH}, 'options')])
        def set_variables(file_dummy, options):
            """
            Gets the first option and displays it as the dropdown of the 'select-variable-x' and 'select-variable-y'.
            :param options:
            :param file_dummy:
            :param options_x: All possible x-axis options
            :param options_y: All possible x-axis options
            :param options_char: All possible characteristic options
            :return: The chosen x-axis and y-axis and characteristic
            """
            if options is None:
                return [None]
            if len(options) <= 0:
                return [None]
            return options[0]['value']

        @app.callback(Output('query', 'value'),
                      Input('apply-filter-button', 'add_filter_clicks'),
                      Input({'type': 'query-label', 'index': ALL}, 'value'),
                      Input({'type': 'query-condition', 'index': ALL}, 'value'),
                      Input({'type': 'query-text_input', 'index': ALL}, 'value'),
                      )
        def apply_query(apply, labels, conditions, text_input):
            """
            Takes the value of all filters and combines them to one query. This query is applied on the data
            :param labels: labels of the filters
            :param conditions: condition of the filters
            :param text_input: Text input of the filters
            :param apply: Button that is pressed to apply filter
            :return: query string
            """
            query = ""

            if labels and conditions and text_input:

                amount = len(labels)
                for i in range(amount):

                    if labels[i] is not None and conditions[i] is not None and text_input[i] is not None:
                        query = query + str(labels[i]) + str(conditions[i]) + str(text_input[i])

                    if i + 1 < len(labels) and labels[i + 1] is not None and conditions[i + 1] is not None and \
                            text_input[
                                i + 1] is not None:
                        query = query + ' & '
                return query
            else:
                return query

    def set_data(self, data):
        """
        Sets data of the NestedFiltering class
        :param data: New data set
        :return: No return
        """
        self.df = data
        self.original_data = data
