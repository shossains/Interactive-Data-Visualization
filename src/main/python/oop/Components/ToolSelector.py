__all__ = ['Dashboard']

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp

from src.main.python.oop.Components.OtherToolExample import ExampleML2
from src.main.python.oop.Components.NormalPlot import NormalPlot
from src.main.python.oop.Figure_factories import FigureFactories
from src.main.python.oop.Components.Table import Table



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
        self.NormalPlot = NormalPlot(plot_factory, df, "Normal plot")
        self.ExampleML2 = ExampleML2(plot_factory, df, "Example Ml 2")
        # self.Table = Table(plot_factory, df, "Show Table")


    def layout(self, params=None):
        """
        Shows the html layout of the tool selector. NormalPlot and otherToolExample are integrated within the layout.
        Parameters are also passed through
        :param params: Parameters selected at the current level of the tool selector.
        :return: Html layout of the program.
        """
        page = dbc.Container([
            dbc.Row(html.Br()),  # Only for styling, spacing out
            # Selector for tool
            html.Div([
                html.H5("Select machine learning tool"),
                self.querystring(params)(
                    dcc.Dropdown)(
                    id='select-tool',
                    options=[
                        {'label': 'Choose ML method', 'value': 'index'},
                        {'label': 'Normal plot', 'value': 'normal-plot'},
                        {'label': 'other machine learning tool  (not implemented)', 'value': 'other-ml-tool'}
                    ],
                    value='index',
                ),
            ]),
            html.Div([self.NormalPlot.layout(params)], id='view-normal-plot'),
            html.Div([self.ExampleML2.layout(params)], id='view-other-ml-tool'),
            dbc.Row(html.Br()), #For styling
            # self.Table.layout(params), #Checkbox for showing table
        ], fluid=True)
        return page

    def component_callbacks(self, app):
        """
        Automatically does the callbacks of the interactive parts of the dashboard main components.
        :param app: Dash app that uses the code
        :return: Output of the callback functions.
        """
        @app.callback([Output(component_id='view-normal-plot', component_property='style'),
                       Output(component_id='view-other-ml-tool', component_property='style')],
                      Input('select-tool', 'value'))
        def choose_component(selection):
            """"
            Chooses which component to show and which not. Show NormalPlot class or OtherToolExamples.
            @:param selection: Gets the id of the selected dropdown of the component id select-tool. 'normal-plot',
            'other-ml-tool', 'index'.
            """
            if selection == 'normal-plot':
                return {'display': 'block'}, {'display': 'none'}
            if selection == 'other-ml-tool':
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
                if (i[1] == value):
                    self.df = i[0]
                    self.NormalPlot.set_data(i[0])
                    self.ExampleML2.set_data(i[0])
                    # self.Table.set_data(i[0])

    def set_data(self, dfList):
        """
        Method to pass through data to ToolSelector from other classes.
        :param data: Pandas dataframe that is passed through
        :return: No return
        """
        self.dfList = dfList




