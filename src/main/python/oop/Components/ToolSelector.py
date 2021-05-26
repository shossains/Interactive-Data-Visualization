__all__ = ['Dashboard']

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash_oop_components import DashComponent

from src.main.python.oop.Components.Menu.OtherMenu import OtherMenu
from src.main.python.oop.Components.Menu.StandardMenu import StandardMenu


class ToolSelector(DashComponent):
    def __init__(self, plot_factory, df, title="Tool selector"):
        """
        Initializes the tool selector. Menu which loads in all tools (subclasses). Feature to display tool the
        selected tool.
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
        Shows the html layout of the tool selector. StandardMenu and OtherMenu are integrated within the layout.
        Parameters are also passed through
        :param params: Parameters selected at the current level of the tool selector.
        :return: Html layout of the program.
        """
        page = dbc.Container([
            dbc.Row(html.Br()),  # Only for styling, spacing out
            # Selector for tool
            html.Div([
                html.H5("Select a menu"),
                self.querystring(params)(
                    dcc.Dropdown)(
                    id='select-tool',
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
        ], fluid=True, style={"padding-left": "0px", "padding-right": "0px"})
        return page

    def component_callbacks(self, app):
        """
        Automatically does the callbacks of the interactive parts of the dashboard main components.
        :param app: Dash app that uses the code
        :return: Output of the callback functions.
        """

        @app.callback([Output(component_id='view-standard-menu', component_property='style'),
                       Output(component_id='view-other-menu', component_property='style')],
                      Input('select-tool', 'value'))
        def choose_component(selection):
            """"
            Chooses which component to show and which not. Show StandardMenu class or OtherMenu.
            @:param selection: Gets the id of the selected dropdown of the component id select-tool. 'standard-menu',
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
            if value is None:
                return {}
            if value == "select":
                return {}

            for i in self.dfList:
                if i[1] == value:
                    self.df = i[0]
                    self.StandardMenu.set_data(i[0])
                    self.OtherMenu.set_data(i[0])
                    # Something has to change here, line above needs to be moved
                    # or done in another way

    def set_data(self, dfList):
        """
        Method to pass through data to ToolSelector from other classes.
        :param dfList: Pandas list of dataframes that is passed through
        :return: No return
        """
        self.dfList = dfList
