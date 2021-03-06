import dash_table
import plotly.graph_objs as go
import plotly.express as px
from dash_oop_components import DashFigureFactory
import dash_html_components as html


class FigureFactories(DashFigureFactory):

    def __init__(self):
        """
        Initializes the figure factories. All different graphing methods are stored here for all classes.
        """
        super().__init__()

    @staticmethod
    def graph_methods(dataframe, xvalue, yvalue, color_based_characteristic, plot_type, title):
        """
        Plots a normal graph with different options how to plot.
        :param dataframe:  Dataframe with all data
        :param xvalue: Selected x-axis value in the data
        :param yvalue: Selected y-axis value in the data
        :param color_based_characteristic: Selected characteristic of the data
        :param plot_type: Selected kind of plot 'scatter', 'density' etc.
        :param title: Selected title of the plot.
        :return: Graph object with the displayed plot
        """

        fig = go.Figure()
        if color_based_characteristic == 'no-color':
            color_based_characteristic = None

        if 'scatter' in plot_type:
            fig = px.scatter(data_frame=dataframe, x=xvalue, y=yvalue, color=color_based_characteristic,
                             hover_data=dataframe)

        elif 'density' in plot_type:
            fig = px.density_contour(data_frame=dataframe, x=xvalue, y=yvalue, color=color_based_characteristic,
                                     hover_data=dataframe)

        elif 'line' in plot_type:
            fig = px.line(data_frame=dataframe, x=xvalue, y=yvalue, color=color_based_characteristic,
                          hover_data=dataframe)

        elif 'histogram' in plot_type:
            fig = px.histogram(data_frame=dataframe, x=xvalue, y=yvalue, color=color_based_characteristic,
                               hover_data=dataframe)

        elif 'box' in plot_type:
            fig = px.box(data_frame=dataframe, x=xvalue, y=yvalue, color=color_based_characteristic,
                         hover_data=dataframe)

        elif 'bar' in plot_type:
            fig = px.bar(data_frame=dataframe, x=xvalue, y=yvalue, color=color_based_characteristic,
                         hover_data=dataframe)

        elif 'area' in plot_type:
            fig = px.area(data_frame=dataframe, x=xvalue, y=yvalue, color=color_based_characteristic,
                          hover_data=dataframe)

        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True,
                    thickness=0.05,
                )
            )
        )

        fig.update_layout(title_text=title, title_x=0.5)

        return fig

    @staticmethod
    def show_table(df, show_table_boolean):
        """
            Makes a table from the uploaded data.
            :param df: dataframe.
            :param show_table_boolean: Boolean to show table or don't show table.
            :return: Table.
        """
        if df is None:
            return None
        if show_table_boolean is not None:
            table = html.Div([
                dash_table.DataTable(
                    id='main_table',
                    data=df.to_dict('rows'),
                    columns=[{'name': i, 'id': i} for i in df.columns[1::]],
                    filter_action='native',
                    sort_action='native',
                    sort_mode='multi',
                    row_selectable='multi',
                    hidden_columns=['row_index_label'],
                ),
                html.Hr(),
                html.Div('Raw Content'),
            ], id='table-uploaded')
            return table
        else:
            return html.Div()
