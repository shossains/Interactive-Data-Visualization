import plotly.graph_objs as go
from dash_oop_components import DashFigureFactory
import plotly.express as px


class MachineLearningPlot(DashFigureFactory):
    def __init__(self):
        super().__init__()

    def plot_scatter(self, df, xvalue, yvalue, charvalue, plotvalue):

        if xvalue is None or yvalue is None or charvalue is None:
            return {}
        if xvalue == "index" or yvalue == "index" or charvalue == "index":
            return {}

        if df is not None:
            dataframe = df.reset_index()
            x = dataframe['{}'.format(xvalue)]
            y = dataframe['{}'.format(yvalue)]

            fig = go.Figure()

            if 'scatter' in plotvalue:
                fig = px.scatter(
                    dataframe, x=x, y=y, color=charvalue, hover_data=df
                )

            if 'density' in plotvalue:
                fig = px.density_contour(dataframe, x=x, y=y, color=charvalue, hover_data=df)

            if 'line' in plotvalue:
                fig = px.line(dataframe, x=x, y=y, color=charvalue, hover_data=df)

            if 'histogram' in plotvalue:
                fig = px.histogram(dataframe, x=x, y=y, color=charvalue, hover_data=df)

            if 'box' in plotvalue:
                fig = px.box(dataframe, x=x, y=y, color=charvalue, hover_data=df)

            if 'bar' in plotvalue:
                fig = px.bar(dataframe, x=x, y=y, color=charvalue, hover_data=df)

            if 'area' in plotvalue:
                fig = px.area(dataframe, x=x, y=y, color=charvalue, hover_data=df)

            return fig
        else:
            return {}
