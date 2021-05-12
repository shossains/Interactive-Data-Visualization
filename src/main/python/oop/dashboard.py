__all__ = ['Dashboard']

from src.main.python.oop.Components import ExampleML1, ExampleML2, UploadData
from dash_bootstrap_components.themes import FLATLY
from src.main.python.oop.Figure_factories import MachineLearningPlot
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp
import pandas as pd
from src.main.python.Dataframe import Dataframe

df = pd.DataFrame({})


class Dashboard(DashComponent):
    def __init__(self, plot_factory):
        super().__init__(title="Interactive data visualiser")

        self.example_ml1 = ExampleML1.ExampleML1(plot_factory, df, "Example Ml 1")
        self.example_ml2 = ExampleML2.ExampleML2(plot_factory, df, "Example Ml 2")
        self.UploadData = UploadData.UploadData()

    def layout(self, params=None):
        return dbc.Container([
            html.H1("Interactive data visualiser"),
            self.UploadData.layout(params),
            self.querystring(params)(DashComponentTabs)(id="tabs",
                                                        tabs=[self.example_ml1, self.example_ml2],
                                                        params=params, component=self, single_tab_querystrings=True),

        ], fluid=True)




if __name__ == '__main__':
    plot_factory = MachineLearningPlot.MachineLearningPlot()
    dashboard = Dashboard(plot_factory)
    app = DashApp(dashboard, querystrings=True, bootstrap=FLATLY)

    app.run(debug=True)
