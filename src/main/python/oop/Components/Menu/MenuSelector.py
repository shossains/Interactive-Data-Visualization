import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
from dash_oop_components import DashComponent

from src.main.python.oop.Components.Menu.OtherMenu.OtherMenu import OtherMenu
from src.main.python.oop.Components.Menu.StandardMenu.StandardMenu import StandardMenu


class MenuSelector(DashComponent):
    def __init__(self, plot_factory, df, title="Tool selector"):
        """
        Initializes the menu selector. Menu which loads in all menu's (subclasses).
        :param plot_factory: Factory with all plot functions
        :param df: Dataframe with all data
        :param title: Title of the page
        """
        super().__init__(title=title)
        self.dfList = []
        self.plot_factory = plot_factory
        self.df = df
        self.StandardMenu = StandardMenu(plot_factory, df, "Standard menu")
        self.OtherMenu = OtherMenu(plot_factory, df, "Example Ml 2")

    def layout(self, params=None):
        """
        Shows the html layout of the menu selector. StandardMenu and OtherMenu are integrated within the layout.
        Parameters are also passed through
        :param params: Parameters selected at the current level of the menu selector.
        :return: Html layout of the program.
        """
        page = dbc.Container([
            dbc.Row(html.Br()),  # Only for styling, spacing out
            # Selector for menu
            html.Div([
                html.H5("Menu"),
                self.querystring(params)(
                    dcc.Dropdown)(
                    id='select-menu',
                    options=[
                        {'label': 'Standard menu', 'value': 'standard-menu'},
                        {'label': 'Other menu  (not implemented)', 'value': 'other-menu'}
                    ],
                    value='standard-menu',
                    clearable=False
                ),
            ]),
            html.Div([self.StandardMenu.layout(params)], id='view-standard-menu'),
            html.Div([self.OtherMenu.layout(params)], id='view-other-menu')
        ], fluid=True)
        return page

    def component_callbacks(self, app):
        """
        Automatically does the callbacks of the interactive parts of the dashboard main components.
        :param app: Dash app that uses the code
        :return: Output of the callback functions.
        """

        @app.callback([Output(component_id='view-standard-menu', component_property='style'),
                       Output(component_id='view-other-menu', component_property='style')],
                      Input('select-menu', 'value'))
        def choose_component(selection):
            """"
            Chooses which component to show and which not. Show StandardMenu class or OtherMenu.
            @:param selection: Gets the id of the selected dropdown of the component id select-menu. 'standard-menu',
            'other-menu', 'index'.
            """
            if selection == 'standard-menu':
                return {'display': 'block'}, {'display': 'none'}
            if selection == 'other-menu':
                return {'display': 'none'}, {'display': 'block'}
            else:
                return {'display': 'none'}, {'display': 'none'}

        @app.callback(Output('select-file', 'options'),
                      Input('dummy', 'children')
                      )
        def set_options_variable(dummy):

            labels = [{'label': 'Select', 'value': 'Select'}]

            length = len(self.dfList)
            for i in range(length):
                labels = labels + [{'label': self.dfList[i][1], 'value': self.dfList[i][1]}]

            return labels

        @app.callback(Output('file-name', 'data'),
                      [Input('select-file', 'value')])
        def update_graph(value):
            """
            Sets the dataframes based on which files are selected to project.
            :param value: the selected files in the 'select files to project' dropdown.

            NOTE: Don't use "Different Files" as a name for a column. This name is hardcoded in this piece of code to
            ensure that it is possible to view multiple files in one plot.
            """
            if value is None:
                return {}
            if value == "select":
                return {}


            if len(value) == 1:
                for i in self.dfList:
                    if i[1] == value[0]:
                        self.df = i[0]
                        self.StandardMenu.set_data(i[0])
                        self.OtherMenu.set_data(i[0])
                        break
            else:
                df = pd.DataFrame()
                for i in self.dfList:
                    for v in value:
                        if i[1] == v:
                            dfToAdd = i[0]
                            dfToAdd['Different Files'] = i[1]
                            df = pd.concat([df, dfToAdd]).reset_index(drop=True)

                self.df = df
                self.StandardMenu.set_data(df)
                self.OtherMenu.set_data(df)

    def set_data(self, dfList):
        """
        Method to pass through data to MenuSelector from other classes.
        :param dfList: Pandas list of dataframes that is passed through
        :return: No return
        """
        self.dfList = dfList
