__all__ = ['Dashboard']

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp

from src.main.python.oop.Components.OtherToolExample import ExampleML2
from src.main.python.oop.Components.NormalPlot import NormalPlot
from src.main.python.oop.Figure_factories import FigureFactories


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
            html.Div([
                html.H5("Select which file to project"),
                self.querystring(params)(dcc.Dropdown)(
                    id='select-file',
                    # style={'display':'none'},
                    # options=[
                    #     {'label': 'Choose file to plot', 'value': 'index'},
                    #     {'label': 'Normal plot', 'value': 'normal-plot'},
                    #     {'label': 'other machine learning tool  (not implemented)', 'value': 'other-ml-tool'}
                    # ],
                    placeholder='Select ...'
                ),
            ]),


            html.Div([self.NormalPlot.layout(params)], id='view-normal-plot'),
            html.Div([self.ExampleML2.layout(params)], id='view-other-ml-tool')
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

#hier

        @app.callback(Output('dataframe', 'data'),
            Input('select-file', 'value'))
        def update_graph(file):
            """
            Updates a normal graph with different options how to plot.

            :param xvalue: Selected x-axis value in the data
            :param yvalue: Selected y-axis value in the data
            :param options_char: Selected characteristic of the data
            :param plotvalue: Selected kind of plot 'scatter', 'density' etc.
            :return: Graph object with the displayed plot
            """
            if file is None:
                return {}
            if file == "select":
                return {}

            dataframe = self.df.reset_index()

            return self.plot_factory.graph_methods(self.dfList[0])


        @app.callback(Output('select-file', 'options'),
                          Input('dummy', 'children'))
        def set_options_variable(dummy):
            """
            loads in possible parameters for the x and y-axis in dropdown from the data.
            :param dummy: dummy html property
            :return: Possible options for dropdown x-axis.
            """
            labels = [{'label': 'select', 'value': 'select'}]

            if self.dfList is not None:
                length = len(self.dfList)
                for i in range(length):
                    print(self.dfList[i][1])
                    labels = labels + [{'label': self.dfList[i][1], 'value': self.dfList[i][1]}]

                return labels
            else:
                return labels

        @app.callback([Output('select-file', 'value')],
                      [
                          Input('select-file', 'options')])
        def set_variables(options):
            """
            Gets the first option and displays it as the dropdown of the 'select-variable-x' and 'select-variable-y'.
            :param options_x: All possible x-axis options
            :param options_y: All possible x-axis options
            :param options_char: All possible characteristic options
            :return: The choosen x-axis and y-axis and characteristic
            """

            # print(options)
            # print(len(options))
            if (options is None):
                return [None]
            if len(options) <= 2:
                print("here")
                return [None]
            return options[0]['value']

        # @app.callback(Output('select-file', 'options'),
        #             [Input('dummy', 'children')])
        #
        # def set_options_variable(dummy):
        #     labels = [{'label': 'Select', 'value': 'select'}]
        #     labels = labels + [{'label': 'a'}, {'value': 'b'}]
        #     labels = labels + [{'label': 'c'}, {'value': 'd'}]
        #

            #
            # return labels
        #
        # @app.callback([Output('select-file', 'value')],
        #               [
        #                   Input('select-file', 'options')
        #               ])
        # def set_variables(options):
        #     """
        #     Gets the first option and displays it as the dropdown of the 'select-variable-x' and 'select-variable-y'.
        #     :param options_x: All possible x-axis options
        #     :param options_y: All possible x-axis options
        #     :param options_char: All possible characteristic options
        #     :return: The choosen x-axis and y-axis and characteristic
        #     """
        #     if (options is None):
        #         return [None]
        #     if len(options) <= 0:
        #         return [None]
        #     return [options[0]['value']]
    #
    def set_data(self, dfList):
        """
        Method to pass through data to ToolSelector from other classes.
        :param data: Pandas dataframe that is passed through
        :return: No return
        """

        if (len(dfList)) == 1:
            self.df = dfList[0]
            self.dfList = dfList
            self.NormalPlot.set_data(dfList[0])
            self.ExampleML2.set_data(dfList[0])
        else:

            return



