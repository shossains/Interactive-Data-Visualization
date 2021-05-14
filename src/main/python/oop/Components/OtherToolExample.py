__all__ = ['Dashboard']

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp
from src.main.python.oop.Figure_factories import FigureFactories



class ExampleML2(DashComponent):
    def __init__(self, plot_factory, df, title="Example ML"):
        super().__init__(title=title)
        self.plot_factory = FigureFactories.FigureFactories()
        self.df = df

    def layout(self, params=None):
        page = dbc.Container([
            html.Div([
                html.H3("This is another tool "),
                ],
                id='OtherToolExample', style={'display': 'block'}),
        ], fluid=True)
        return page

    # def component_callbacks(self, app):
    #     @app.callback(Output('Mygraph-ml2', 'figure'), [
    #         Input('select-variable-x-ml2', 'value'),
    #         Input('select-variable-y-ml2', 'value'),
    #         Input('select-characteristics-ml2', 'value'),
    #         Input('select-plot-options-ml2', 'value'),
    #     ])
    #     def update_plot(xvalue, yvalue, charvalue, plotvalue):
    #         return self.plot_factory.graph_methods(self.df, xvalue, yvalue, charvalue, plotvalue)
    #
    #     @app.callback([Output('select-variable-x-ml2', 'options'),
    #                    Output('select-variable-y-ml2', 'options'),
    #                    Output('select-characteristics-ml2', 'options')],
    #                   [
    #                       Input('dummy', 'children')
    #                   ])
    #     def set_options_variable(dummy):
    #         """
    #         loads in possible parameters for the x and y-axis from the data.
    #         :param dummy: dummy html property
    #         :return: Possible options for dropdown x-axis.
    #         """
    #         dataframe = self.df.reset_index()
    #         return [{'label': i, 'value': i} for i in dataframe.columns], [{'label': i, 'value': i} for i in
    #                                                                        dataframe.columns], [
    #                    {'label': i, 'value': i} for i in dataframe.columns]

    def set_data(self, data):
            self.df = data
