__all__ = ['Dashboard']

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp
from src.main.python.oop.Figure_factories import MachineLearningPlot


class ExampleML2(DashComponent):
    def __init__(self, plot_factory, df, title="Example ML"):
        super().__init__(title=title)
        self.plot_factory = MachineLearningPlot.MachineLearningPlot()
        self.df = df

    def layout(self, params=None):
        page = dbc.Container([
            html.Div([
                html.H3("This is another tool "),
                html.H4("Select variable x"),
                self.querystring(params)(dcc.Dropdown)(
                    id='select-variable-x-ml2',
                    placeholder='Select ...'),
                html.H4("Select variable y"),
                self.querystring(params)(dcc.Dropdown)(
                    id='select-variable-y-ml2',
                    placeholder='Select ...'),
                html.H4("Select Characteristics"),
                self.querystring(params)(dcc.Dropdown)(
                    id='select-characteristics-ml2',
                    placeholder='Select ...',
                    # multi=True
                ),
                html.H4("Select plot method"),
                self.querystring(params)(dcc.Dropdown)(id='select-plot-options-ml2',
                                                       options=[
                                                           {'label': 'Area', 'value': 'area'},
                                                           {'label': 'Bar', 'value': 'bar'},
                                                           {'label': 'Box', 'value': 'box'},
                                                           {'label': 'Density', 'value': 'density'},
                                                           {'label': 'Histogram', 'value': 'histogram'},
                                                           {'label': 'Line', 'value': 'line'},
                                                           {'label': 'Scatter', 'value': 'scatter'},
                                                       ], value='scatter'
                                                       ),
                html.Div(id='output-select-data-ml2'),
                dcc.Graph(id='Mygraph-ml2')],
                id='t-sne', style={'display': 'block'}),
            dcc.Checklist(id='show-table-ml2', options=[
                {'label': 'Show table', 'value': 'show-table'}]),
        ], fluid=True)
        return page

    def component_callbacks(self, app):
        @app.callback(Output('Mygraph-ml2', 'figure'), [
            Input('select-variable-x-ml2', 'value'),
            Input('select-variable-y-ml2', 'value'),
            Input('select-characteristics-ml2', 'value'),
            Input('select-plot-options-ml2', 'value'),
        ])
        def update_plot(xvalue, yvalue, charvalue, plotvalue):
            return self.plot_factory.plot_scatter(self.df, xvalue, yvalue, charvalue, plotvalue)

        @app.callback([Output('select-variable-x-ml2', 'options'),
                       Output('select-variable-y-ml2', 'options'),
                       Output('select-characteristics-ml2', 'options')],
                      [
                          Input('dummy', 'children')
                      ])
        def set_options_variable(dummy):
            """
            loads in possible parameters for the x and y-axis from the data.
            :param dummy: dummy html property
            :return: Possible options for dropdown x-axis.
            """
            dataframe = self.df.reset_index()
            return [{'label': i, 'value': i} for i in dataframe.columns], [{'label': i, 'value': i} for i in
                                                                           dataframe.columns], [
                       {'label': i, 'value': i} for i in dataframe.columns]