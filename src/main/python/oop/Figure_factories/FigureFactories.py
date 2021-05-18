import plotly.graph_objs as go
import plotly.express as px
import dash_html_components as html
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp
import dash_table
import pandas as pd


class FigureFactories(DashFigureFactory):

    def __init__(self):
        """
        Initializes the figure factories. All different graphing methods are stored here for all classes.
        """
        super().__init__()

    @staticmethod
    def graph_methods(df, xvalue, yvalue, charvalue, plotvalue, timeseries_bool):
        """
        Plots a normal graph with different options how to plot.
        :param df:  Dataframe with all data
        :param xvalue: Selected x-axis value in the data
        :param yvalue: Selected y-axis value in the data
        :param charvalue: Selected characteristic of the data
        :param plotvalue: Selected kind of plot 'scatter', 'density' etc.
        :return: Graph object with the displayed plot
        """

        if df is not None:
            dataframe = df.reset_index()
            x = dataframe['{}'.format(xvalue)]
            y = dataframe['{}'.format(yvalue)]

            print(x)
            if timeseries_bool is not None:
                x = pd.to_datetime(x, format='%d/%m/%Y %H:%M:%S')
                print("Converted time series")
                print(pd.to_datetime(x, format='%d/%m/%Y %H:%M:%S'))

            fig = go.Figure()

            if 'scatter' in plotvalue:
                fig = px.scatter(
                    data_frame=dataframe, x=xvalue, y=yvalue, color=charvalue, hover_data=df,
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

    @staticmethod
    def subgraph_methods(df, options_char, dims):
        """
            displays subgraphs when comparing labels to each other
            :param df:  Dataframe with all data
            :param options_char: Selected characteristic of the data
            :param dims: Multiple dimensions that are chosen
            :return: graph
        """
        if dims is None:
            return {}
        if dims == "index":
            return {}

        if df is not None:

            dataframe = df.reset_index()

            fig = px.scatter_matrix(
                dataframe, dimensions=dims, color=options_char
            )

            return fig
        else:
            return {}

    @staticmethod
    def show_table(df, contents, filename, showtable):
        """
            Makes a table from the uploaded data.
            :param df: dataframe
            :param contents: contents of the data
            :param filename: filename of the data
            :param dummy: dummy html.P. Used to activate chained callbacks.
            :param showtable: Boolean
            :return: Table
            """
        if showtable is not None:
            table = html.Div()
            if contents:
                contents = contents[0]

                table = html.Div([
                    html.H5(filename),
                    dash_table.DataTable(
                        data=df.to_dict('rows'),
                        columns=[{'name': i, 'id': i} for i in df.columns]
                    ),
                    html.Hr(),
                    html.Div('Raw Content'),

                    html.Pre(contents[0:200] + '...', style={
                        'whiteSpace': 'pre-wrap',
                        'wordBreak': 'break-all'
                    })
                ], id='table-uploaded')
            return table
        else:
            return html.Div()
