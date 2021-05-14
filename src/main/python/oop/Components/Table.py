__all__ = ['Dashboard']

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp
from src.main.python.oop.Figure_factories import FigureFactories

dcc.Checklist(id='show-table-ml2', options=[
    {'label': 'Show table', 'value': 'show-table'}]),


class Table(DashComponent):
    def __init__(self, plot_factory, df, title="Table"):
        super().__init__(title=title)
        self.contents = None
        self.filename = None
        self.plot_factory = FigureFactories.FigureFactories()
        self.df = df

    def layout(self, params=None):
        return html.Div([
            dcc.Checklist(id='show-table', options=[{'label': 'Show table', 'value': 'show-table'}]),
            html.Div(id='output-data-upload'),
            dcc.Loading(
                id="loading-icon3",
                children=[html.Div(id='output-data-upload')],
                type="dot",
            )
        ])

    def component_callbacks(self, app):
        @app.callback(
            Output(component_id='output-data-upload', component_property='style'),
            [Input(component_id='show-table', component_property='value')])
        def show_hide_table(visibility_state):
            """
            :param visibility_state:
            :return: visibility style
            """
            if visibility_state == ['show-table']:
                return {'display': 'block'}
            else:
                return {'display': 'none'}

        @app.callback(Output('output-data-upload', 'children'),
                      [
                          Input('show-table', 'value')
                      ])
        def update_table(showtable):
            return self.plot_factory.show_table(self.df, self.contents, self.filename, showtable)

    def give_data(self, data, contents, filename):
        self.df = data
        self.contents = contents
        self.filename = filename
