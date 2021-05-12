import base64
import io
import plotly.graph_objs as go
import plotly.express as px
import time

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import dash_oop_components

from src.main.python.Dataframe import Dataframe

df = pd.DataFrame({})

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

app.layout = html.Div([
    #Upload bar
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    #Machine learning tool selection
    html.H4("Select machine learning tool"),


    #Data table
    html.Div(id='output-data-upload', style={'display': 'none'}),
    html.P(id='dummy')
])


@app.callback(Output('dummy', 'children'),
              [
                  Input('upload-data', 'contents'),
                  Input('upload-data', 'filename')
              ])
def update_dataframe(contents, filename):
    """
    Updates the dataframe when a file is loaded in.
    :param contents: the contents of the file
    :param filename: the name of the file
    :return: dummy html.P, which is used to activate chained callbacks.
    """
    if contents:
        contents = contents[0]
        filename = filename[0]
        if contents is None:
            return

        global df
        df = Dataframe(contents, filename).data


@app.callback(
    Output(component_id='t-sne', component_property='style'),
    [Input(component_id='select-tool', component_property='value')])
def show_hide_element(visibility_state):
    """
    Looks at which tool is selected in the dropdown select-tool and displays selection functions for that certain tool.
    :param visibility_state:
    :return: visibility style
    """
    if visibility_state == 'T-sne':
        return {'display': 'block'}
    if visibility_state == 'other_ml_tool':
        return {'display': 'none'}
    if visibility_state == 'index':
        return {'display': 'none'}


@app.callback([Output('select-variable-x', 'options'),
               Output('select-variable-y', 'options'),
               Output('select-characteristics', 'options')],
              [
                  Input('dummy', 'children')
              ])
def set_options_variable(dummy):
    """
    loads in possible parameters for the x and y-axis from the data.
    :param dummy: dummy html property
    :return: Possible options for dropdown x-axis.
    """
    global df
    dataframe = df.reset_index()
    return [{'label': i, 'value': i} for i in dataframe.columns], [{'label': i, 'value': i} for i in
                                                                   dataframe.columns], [
               {'label': i, 'value': i} for i in dataframe.columns]


@app.callback([Output('select-variable-x', 'value'),
               Output('select-variable-y', 'value'),
               Output('select-characteristics', 'value')],
              [
                  Input('select-variable-x', 'options'),
                  Input('select-variable-y', 'options'),
                  Input('select-characteristics', 'options')
              ])
def set_variables(options_x, options_y, options_char):
    """
    Gets the ouput of the dropdown of the 'select-variable-x' and 'select-variable-y'.
    :param options_x: All possible x-axis options
    :param options_y: All possible x-axis options
    :param options_char: All possible characteristic options
    :return: The choosen x-axis and y-axis and characteristic
    """
    if (options_y is None or options_x is None or options_char is None):
        return None, None, None
    if len(options_y) <= 0 or (len(options_x) <= 0) or (len(options_char) <= 0):
        return None, None, None
    return options_x[0]['value'], options_y[0]['value'], options_char[0]['value']


@app.callback(Output('Mygraph', 'figure'), [
    Input('select-variable-x', 'value'),
    Input('select-variable-y', 'value'),
    Input('select-characteristics', 'value'),
    Input('select-plot-options', 'value'),
])
def update_graph(xvalue, yvalue, charvalue, plotvalue):
    """
    Displays the graph. Only normal plotting at the moment (x-axis, y-axis).
    TODO: Make multiple y-axis in the same graph possible.
    TODO: Make separate graphic plots possible
    :param xvalue: Value of the x-axis
    :param yvalue: value of the y-axis
    :param charvalue: value of characteristic
    :param plotvalue: Value of the plot selection e.g. scatter
    :return:  graph
    """
    if xvalue is None or yvalue is None or charvalue is None:
        return {}
    if xvalue == "index" or yvalue == "index" or charvalue == "index":
        return {}

    global df

    if (df is not None):
        dataframe = df.reset_index()
        x = dataframe['{}'.format(xvalue)]
        y = dataframe['{}'.format(yvalue)]

        fig = go.Figure()

        if ('scatter' in plotvalue):
            fig = px.scatter(
                dataframe, x=x, y=y, color=charvalue, hover_data=df
            )

        if ('density' in plotvalue):
            fig = px.density_contour(dataframe, x=x, y=y, color=charvalue, hover_data=df)

        if ('line' in plotvalue):
            fig = px.line(dataframe, x=x, y=y, color=charvalue, hover_data=df)

        if ('histogram' in plotvalue):
            fig = px.histogram(dataframe, x=x, y=y, color=charvalue, hover_data=df)

        if ('box' in plotvalue):
            fig = px.box(dataframe, x=x, y=y, color=charvalue, hover_data=df)

        if ('bar' in plotvalue):
            fig = px.bar(dataframe, x=x, y=y, color=charvalue, hover_data=df)

        if ('area' in plotvalue):
            fig = px.area(dataframe, x=x, y=y, color=charvalue, hover_data=df)

        return fig
    else:
        return {}


@app.callback(
    Output(component_id='output-data-upload', component_property='style'),
    [Input(component_id='show-table', component_property='value')])
def show_hide_table(visibility_state):
    """
    Looks at which tool is selected in the dropdown select-tool and displays selection functions for that certain tool.
    TODO: Add more return states for more tools.
    Joost knows this^
    :param visibility_state:
    :return: visibility style
    """
    if visibility_state == ['show-table']:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(Output('output-data-upload', 'children'),
              [
                  Input('upload-data', 'contents'),
                  Input('upload-data', 'filename'),
                  Input('dummy', 'children'),
                  Input('show-table', 'value')
              ])
def update_table(contents, filename, dummy, showtable):
    """
    Makes a table from the uploaded data.
    :param contents: contents of the data
    :param filename: filename of the data
    :param dummy: dummy html.P. Used to activate chained callbacks.
    :return: Table
    """
    if showtable is not None:
        table = html.Div()
        if contents:
            contents = contents[0]
            filename = filename[0]
            global df
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


if __name__ == '__main__':
    app.run_server(debug=True)
