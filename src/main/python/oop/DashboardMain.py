__all__ = ['Dashboard']

from src.main.python.oop.Components import Instructions, GraphPlot
from dash_bootstrap_components.themes import FLATLY

from src.main.python.oop.Components.ToolSelector import ToolSelector
from src.main.python.oop.Figure_factories import FigureFactories
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashComponent, DashApp
from src.main.python.oop.Dataframe import Dataframe
import io


class Dashboard(DashComponent):
    def __init__(self, plotfactory):
        """
        Initializes the main component of the dashboard. Makes the subclasses ToolSelector, Table and Instructions
        @rtype: object
        """
        super().__init__(title="Interactive data visualiser")
        df = None
        self.dfList = []
        self.ToolSelector = ToolSelector(plotfactory, df, "Tool selector")
        self.Instructions = Instructions.Instructions(plotfactory, df, "Instruction page")
        self.GraphPlot = GraphPlot.GraphPlot(plotfactory, df, "Graph")

    def layout(self, params=None):
        """
        Shows the html layout of the main dashboard. Toolselector, table and instructions are integrated within the
        layout. Parameters are also passed through.
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
                    # The column containing the toggle will be only as wide as the
                    # toggle, resulting in the toggle being right aligned.
                    width="auto",
                    # vertically align the toggle in the center
                    align="center",
                ),

                html.P(id='dummy'),
                html.Pre(id='dummy2')
            ]
        )
        sidebar = html.Div(
            [
                sidebar_header,

                dbc.Collapse([
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
                                    'background-color': '#18bc9d',
                                    'color': 'white'
                                },
                                # Allow multiple files to be uploaded
                                multiple=True
                            ),
                        )
                    ),

                    dbc.Collapse(dbc.Nav(
                        [
                            dbc.NavLink("Home", href="/", active="exact"),
                            dbc.NavLink("Instructions", href="/instructions", active="exact"),
                            dbc.NavLink("Plot", href="/plotting", active="exact"),
                        ],
                        vertical=True,
                        pills=True,
                    ),
                        id="collapse"),

                    html.Div(id='sidebar-plot-menu'),

                ], id="collapse"),
            ],
            id="sidebar",
            style={
                # 'height':'90vh',
                'overflow-y':'auto'
            }
        )

        content = html.Div(id="page-content")
        return html.Div([sidebar, content])

    def component_callbacks(self, app):
        """
        Automatically does the callbacks of the interactive parts of the dashboard main components.
        :param app: Dash app that uses the code
        :return: Output of the callback functions.
        """

        @app.callback(Output('dummy', 'children'),
                      Input('upload-data', 'contents'),
                      State('upload-data', 'filename'),
                      State('upload-data', 'last_modified'))
        def update_output(list_of_contents, list_of_names, list_of_dates):
            '''
            Initialises and/or updates the list containing data frames when a new file is uploaded.
            :param list_of_contents: Content of the data frames.
            :param list_of_names: Names of the data frames.
            :param list_of_dates: Last modified date of the frames.
            :return: dummy, which is a placeholder because Dash requires a output.
            '''
            if list_of_contents is not None:
                for name, content in zip(list_of_names, list_of_contents):
                    df_to_add = Dataframe(content, name).data

                    length = len(self.dfList)
                    # if a file with the same name has been detected, only update the dataframe, don't add it again
                    for i in range(length):
                        if name == self.dfList[i][1]:
                            self.dfList[i] = [df_to_add, name]
                            break
                    else:
                        self.dfList.insert(0, [df_to_add, name])

                # IMPORTANT: Dont forget if you add new classes to give the data
                self.ToolSelector.set_data(self.dfList)
                print("data uploaded")

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

        @app.callback([Output("page-content", "children"),
                       Output("sidebar-plot-menu", "children")],
                      [Input("url", "pathname")])
        def render_page_content(pathname):
            if pathname == "/":
                return html.P("This is the content of the home page!"), None
            elif pathname == "/instructions":
                return html.Div([self.Instructions.layout()]), None
            elif pathname == "/plotting":
                return html.Div([self.GraphPlot.layout()]), html.Div([self.ToolSelector.layout()])
            # If the user tries to reach a different page, return a 404 message
            return dbc.Jumbotron(
                [
                    html.H1("404: Not found", className="text-danger"),
                    html.Hr(),
                    html.P(f"The pathname {pathname} was not recognised..."),
                ]
            )


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
