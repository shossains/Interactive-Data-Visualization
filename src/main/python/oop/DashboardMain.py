__all__ = ['Dashboard']

from src.main.python.oop.Components import NormalPlot, OtherToolExample, Instructions
from dash_bootstrap_components.themes import FLATLY

from src.main.python.oop.Components.Table import Table
from src.main.python.oop.Components.ToolSelector import ToolSelector
from src.main.python.oop.Figure_factories import FigureFactories
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashComponent, DashComponentTabs, DashApp
import pandas as pd
from src.main.python.oop.Dataframe import Dataframe


class Dashboard(DashComponent):
    def __init__(self, plotfactory):
        """
        Initializes the main component of the dashboard. Makes the subclasses ToolSelector, Table and Instructions
        @rtype: object
        """
        super().__init__(title="Interactive data visualiser")
        df = None
        self.ToolSelector = ToolSelector(plotfactory, df, "Tool selector")
        self.Table = Table(plotfactory, df, "Show Table")
        self.Instructions = Instructions.Instructions(plotfactory, df, "Instruction page")

    def layout(self, params=None):
        """
        Shows the html layout of the main dashboard. Toolselector, table and instructions are integrated within the layout. Parameters are also passed through
        :param params: Parameters selected at the current level of the dashboard.
        :return: Html layout of the program.
        """
        sidebar_header = dbc.Row(
            [
                dbc.Col(html.H4("Interactive data visualizer")),
                dbc.Col(
                    [
                        html.Button(
                            # use the Bootstrap navbar-toggler classes to style
                            html.Span(className="navbar-toggler-icon"),
                            className="navbar-toggler",
                            # the navbar-toggler classes don't set color
                            style={
                                "color": "rgba(0,0,0,.5)",
                                "border-color": "rgba(0,0,0,.1)",
                            },
                            id="navbar-toggle",
                        ),
                        html.Button(
                            # use the Bootstrap navbar-toggler classes to style
                            html.Span(className="navbar-toggler-icon"),
                            className="navbar-toggler",
                            # the navbar-toggler classes don't set color
                            style={
                                "color": "rgba(0,0,0,.5)",
                                "border-color": "rgba(0,0,0,.1)",
                            },
                            id="sidebar-toggle",
                        ),
                    ],
                    # the column containing the toggle will be only as wide as the
                    # toggle, resulting in the toggle being right aligned
                    width="auto",
                    # vertically align the toggle in the center
                    align="center",
                ),



                # Row for uploading the data
                dbc.Col(
                    html.Div(
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                # 'width': '20%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '10px',
                                'textAlign': 'center',
                                'background-color': '#5ebfff',
                                'color': 'white'
                            },
                            # Allow multiple files to be uploaded
                            multiple=True
                        ),
                    ), width=2
                ),

                # dbc.Row(html.Br()),  # Only for styling, spacing out

                self.querystring(params)(DashComponentTabs)(id="tabs",
                                                            tabs=[self.Instructions, self.ToolSelector],
                                                            params=params, component=self, ),
                self.Table.layout(params),
                html.P(id='dummy'),
                html.Pre(id='dummy2')
            ]
        )
        sidebar = html.Div(
            [
                sidebar_header,
            ],
            id="sidebar",
        )
        # return dbc.Container([
        #
        #     dbc.Row(html.Br()), # Only for styling, spacing out
        #
        #     dbc.Row(dbc.Col(html.H1("Interactive data visualizer"), width="auto"), justify="center"),
        #
        #     # Row for uploading the data
        #     dbc.Row(
        #         dbc.Col(
        #             html.Div(
        #                 dcc.Upload(
        #                     id='upload-data',
        #                     children=html.Div([
        #                         'Drag and Drop or ',
        #                         html.A('Select Files')
        #                     ]),
        #                     style={
        #                         # 'width': '20%',
        #                         'height': '60px',
        #                         'lineHeight': '60px',
        #                         'borderWidth': '1px',
        #                         'borderStyle': 'dashed',
        #                         'borderRadius': '10px',
        #                         'textAlign': 'center',
        #                         'background-color': '#5ebfff',
        #                         'color': 'white'
        #                     },
        #                     # Allow multiple files to be uploaded
        #                     multiple=True
        #                 ),
        #            ), width=2
        #         ), justify="center"
        #     ),
        #
        #     dbc.Row(html.Br()), # Only for styling, spacing out
        #
        #     self.querystring(params)(DashComponentTabs)(id="tabs",
        #                                                 tabs=[self.Instructions, self.ToolSelector],
        #                                                 params=params, component=self,),
        #     dbc.Row(html.Br()), # Only for styling, spacing out
        #
        #     # Shows table or not
        #     self.Table.layout(params),
        #     html.P(id='dummy'),
        #     html.Pre(id='dummy2')
        # ], fluid=True)

        content = html.Div(id="page-content")
        return html.Div([dcc.Location(id="url"), sidebar, content])

    def component_callbacks(self, app):
        """
        Automatically does the callbacks of the interactive parts of the dashboard main components.
        :param app: Dash app that uses the code
        :return: Output of the callback functions.
        """
        @app.callback(Output('dummy', 'children'),
                      [
                          Input('upload-data', 'contents'),
                          Input('upload-data', 'filename')
                      ])
        def upload_data(contents, filename):
            """
                   Updates the dataframe when a file is loaded in.
                   :param contents: the contents of the file
                   :param filename: the name of the file
                   :return: dummy html.P, which is used to activate chained callbacks.
                   """
            print("running")
            if contents:
                contents = contents[0]
                filename = filename[0]
                if contents is None:
                    return

                df = Dataframe(contents, filename).data

                # IMPORTANT: Dont forget if you add new classes to give the data
                self.ToolSelector.set_data(df)
                self.Table.set_data(df, contents, filename)
                print("data uploaded")
                return {}

        @app.callback(
            Output("sidebar", "className"),
            [Input("sidebar-toggle", "n_clicks")],
            [State("sidebar", "className")],
        )
        def toggle_classname(n, classname):
            if n and classname == "":
                return "collapsed"
            return ""

        @app.callback(
            Output("collapse", "is_open"),
            [Input("navbar-toggle", "n_clicks")],
            [State("collapse", "is_open")],
        )
        def toggle_collapse(n, is_open):
            if n:
                return not is_open
            return is_open


if __name__ == '__main__':
    """"
    Main function to be run
    """
    plot_factory = FigureFactories.FigureFactories()
    dashboard = Dashboard(plot_factory)
    DashApp = DashApp(dashboard, querystrings=True, bootstrap=FLATLY)
    DashApp.run(debug=True)
else:
    '''
    This code exists to be able to run test_application.py
    When running test_application, the __name__ is not equal to __main__
    Dash testing api is looking for a Dash app instance in the DashboardMain.py, which is created here.
    '''
    plot_factory = FigureFactories.FigureFactories()
    dashboard = Dashboard(plot_factory)
    app = DashApp(dashboard, querystrings=True, bootstrap=FLATLY).app




