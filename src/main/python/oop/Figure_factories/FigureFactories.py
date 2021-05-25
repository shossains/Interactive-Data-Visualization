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
    def graph_methods(dataframe, xvalue, yvalue, charvalue, plotvalue):
        """
        Plots a normal graph with different options how to plot.
        :param dataframe:  Dataframe with all data
        :param xvalue: Selected x-axis value in the data
        :param yvalue: Selected y-axis value in the data
        :param charvalue: Selected characteristic of the data
        :param plotvalue: Selected kind of plot 'scatter', 'density' etc.
        :return: Graph object with the displayed plot
        """

        fig = go.Figure()
        if charvalue == 'no-color':
            charvalue = None

        elif 'scatter' in plotvalue:
            fig = px.scatter(data_frame=dataframe, x=xvalue, y=yvalue, color=charvalue, hover_data=dataframe, )

        elif 'density' in plotvalue:
            fig = px.density_contour(data_frame=dataframe, x=xvalue, y=yvalue, color=charvalue, hover_data=dataframe)

        elif 'line' in plotvalue:
            fig = px.line(data_frame=dataframe, x=xvalue, y=yvalue, color=charvalue, hover_data=dataframe)

        elif 'histogram' in plotvalue:
            fig = px.histogram(data_frame=dataframe, x=xvalue, y=yvalue, color=charvalue, hover_data=dataframe)

        elif 'box' in plotvalue:
            fig = px.box(data_frame=dataframe, x=xvalue, y=yvalue, color=charvalue, hover_data=dataframe)

        elif 'bar' in plotvalue:
            fig = px.bar(data_frame=dataframe, x=xvalue, y=yvalue, color=charvalue, hover_data=dataframe)

        elif 'area' in plotvalue:
            fig = px.area(data_frame=dataframe, x=xvalue, y=yvalue, color=charvalue, hover_data=dataframe)
        
        return fig

    @staticmethod
    def subgraph_methods(dataframe, options_char, dims):
        """
            displays subgraphs when comparing labels to each other
            :param dataframe:  Dataframe with all data
            :param options_char: Selected characteristic of the data
            :param dims: Multiple dimensions that are chosen
            :return: graph
        """
        if options_char == 'no-value' or options_char == 'select':
            options_char = None
            
        return px.scatter_matrix(dataframe, dimensions=dims, color=options_char)

