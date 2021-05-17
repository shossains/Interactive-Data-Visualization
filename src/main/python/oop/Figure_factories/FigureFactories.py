import plotly.graph_objs as go
import plotly.express as px
import dash_html_components as html
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp
import dash_table


class FigureFactories(DashFigureFactory):
    def __init__(self):
        super().__init__()

    @staticmethod
    def graph_methods(df, xvalue, yvalue, charvalue, plotvalue):
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

    @staticmethod
    def subgraph_methods(df, options_char, dims, plotvalue):
        """
            displays subgraphs when comparing labels to each other
            :param df:
            :param options_char:
            :param dims: Multiple dimensions that are chosen
            :return: graph
            """
        if dims is None:
            return {}
        if dims == "index":
            return {}

        if df is not None:

            dataframe = df.reset_index()

            fig = go.Figure()

            if 'scatter' in plotvalue:
                fig = px.scatter_matrix(
                    dataframe, dimensions=dims, color=options_char
                )

            # if 'density' in plotvalue:
            #     fig = px.density_contour(
            #         dataframe, dimensions=dims, color=options_char
            #     )

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
