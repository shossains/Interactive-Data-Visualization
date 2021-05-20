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
    def __init__(self, plot_factory, df, title="Example ML"):
        super().__init__(title=title)
        self.plot_factory = plot_factory
        self.df = df
        self.NormalPlot = NormalPlot(plot_factory, df, "Normal plot")
        self.ExampleML2 = ExampleML2(plot_factory, df, "Example Ml 2")

    def layout(self, params=None):
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
                    clearable=False
                ),
            ]),
            html.Div([self.NormalPlot.layout(params)], id='view-normal-plot'),
            html.Div([self.ExampleML2.layout(params)], id='view-other-ml-tool')
        ], fluid=True)
        return page

    def component_callbacks(self, app):
        @app.callback([Output(component_id='view-normal-plot', component_property='style'),
                       Output(component_id='view-other-ml-tool', component_property='style')],
                      Input('select-tool', 'value'))
        def choose_component(selection):
            print(selection)
            if selection == 'normal-plot':
                print("normal")
                return {'display': 'block'}, {'display': 'none'}
            if selection == 'other-ml-tool':
                print("other")
                return {'display': 'none'}, {'display': 'block'}
            else:
                print("empty")
                return {'display': 'none'}, {'display': 'none'}

    def set_data(self, data):
        self.df = data
        self.NormalPlot.set_data(data)
        self.ExampleML2.set_data(data)
