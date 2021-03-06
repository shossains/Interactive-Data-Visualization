import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_oop_components import DashFigureFactory, DashComponent, DashComponentTabs, DashApp
from src.main.python.oop.Figure_factories import VisualFactories


class Instructions(DashComponent):
    def __init__(self, plot_factory, df, title="Instruction page"):
        """
        Instruction page with explanation and other info.
        :param plot_factory: Factory with all plot functions
        :param df: Dataframe with all data
        :param title: Title of the page
        """
        super().__init__(title=title)
        self.plot_factory = VisualFactories.FigureFactories()
        self.df = df

    def layout(self, params=None):
        """
               Shows the html layout of the Instructions page. Parameters are also passed through
               :param params: Parameters selected at the current level of the dashboard.
               :return: Html layout of the program.
        """
        page = dbc.Container([
            html.Div([
                html.H1("Welcome to the interactive data visualiser", style={'text-align': 'center'}),
                html.H6("Made by", style={'text-align': 'center'}),
                html.H4("Glenn van den Belt", style={'text-align': 'center'}),
                html.H4("Shaan Hossain", style={'text-align': 'center'}),
                html.H4("Joost Jansen", style={'text-align': 'center'}),
                html.H4("Adrian Kuiper", style={'text-align': 'center'}),
                html.H4("Philip Tempelman", style={'text-align': 'center'}),
                html.H2("Instructions"),
                html.Br(),

                html.H5("Uploading and selecting data files"),
                html.P("To upload csv files click on the green button on the left top. There is a possibility to "
                       " upload multiple csv files. The different csv files can then be selected and plotted "
                       "separately by selecting the file in the 'select files to project' dropdown menu.",
                       style={'font-size': '20px'}),
                html.Br(),

                html.H5("Plotting Main Graph"),
                html.P("To plot the main graph, select the labels you want to use as the x-axis and the y-axis. "
                       "To differentiate between values of a specific label, you can select a color label, which gives "
                       "the graph different colors according to their value within the label. There is also a "
                       "possibility to select different plot methods like scatter, box, density plots etc. ",
                       style={'font-size': '20px'}),
                html.Br(),

                html.H5("Adding Filters to Graph"),
                html.P(["To add a filter, click on the add filter button. After filling in the filters, click on apply "
                        "filters to apply them to the graph. There is also a possibility to remove filters. ",
                        html.Span("**Important!!!**:", style={'font-weight': 'bold'}),
                        " If you are filtering on a string in a column, the filtering is case sensitive and make sure "
                        "you put them between brackets.    i.e. geography == 'Detroit'"],
                       style={'font-size': '20px'}),
                html.Br(),

                html.H5("Procesing your own code"),
                html.P("To process your own code click on one the buttons under 'process data with client code' "
                       "to apply your own code on the graph",
                       style={'font-size': '20px'}),
                html.Br(),

                html.H5("Viewing Table "),
                html.P("To view the table, tick the box indicating 'show table'. Within the table you are able to "
                       "filter on the data by writing a query above one of the columns. You are also able to use "
                       "lasso/box select on the graph, where the selected data points in the graph will be ticked "
                       "in the table.",
                       style={'font-size': '20px'}),
                html.Br(),
            ], id='Instructions')
        ], fluid=True)
        return page
