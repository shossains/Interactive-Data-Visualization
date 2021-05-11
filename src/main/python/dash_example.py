import base64
import io
import plotly.graph_objs as go
import time

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

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
    html.H4("Select machine learning tool"),
    dcc.Dropdown(
                id='select-tool',
                options=[
                    {'label': 'Choose ML method', 'value': 'index'},
                    {'label': 'T-sne (not implemented)', 'value': 'T-sne'},
                    {'label': 'other_ml_tool  (not implemented)', 'value': 'other_ml_tool'}
                ],
                value='index'
            ),
    # When T-sne choosen this one will be visible
    html.Div([
    html.H4("Select variable x"),
    dcc.Dropdown(
        id='select-variable-x',
        placeholder = 'Select ...'),
    html.H4("Select variable y"),
    dcc.Dropdown(
        id='select-variable-y',
        placeholder = 'Select ...'),
    html.Div(id='output-select-data'),
    dcc.Graph(id='Mygraph')],
    id='t-sne', style= {'display': 'block'}),
    dcc.Checklist(id='select-table',
        options=[
            {'label': 'Scatter plot', 'value': 'scatter'},
            {'label': 'View raw data', 'value': 'raw-data'},
        ]),
    html.Div(id='output-data-upload', style={'display': 'none'}),
    html.P(id='dummy')
])

@app.callback(Output('dummy', 'children'),
                [
                    Input('upload-data', 'contents'),
                    Input('upload-data', 'filename')
                ])
def update_dataframe(contents, filename):
    print("called")
    if contents:
        contents = contents[0]
        filename = filename[0]
        global df
        df = parse_data(contents, filename)
        df = df.reset_index()
        print(len(df))

@app.callback(
    Output(component_id='t-sne', component_property='style'),
    [Input(component_id='select-tool', component_property='value')])

def show_hide_t_sne(visibility_state):
    """
    Looks at wich tool is selected in the dropdown select-tool and displays selection functions for that certain tool.
    TODO: Add more return states for more tools.
    Joost knows this^
    :param visibility_state:
    :return: visibility style
    """
    if visibility_state == 'T-sne':
        return {'display': 'block'}
    if visibility_state == 'other_ml_tool':
        return {'display': 'none'}
    if visibility_state == 'index':
        return {'display': 'none'}

@app.callback(
    Output(component_id='output-data-upload', component_property='style'),
    [Input(component_id='select-table', component_property='value')])

def show_hide_table_scatter(visibility_state):
    """
    Hides or shows the data in a table at the bottom
    :param visibility_state: Selected or unselected
    :return: style format visible or not
    """
    print(visibility_state)
    if visibility_state == 'raw-data':
        return {'display': 'block'}
    if visibility_state == []:
        return {'display': 'none'}

@app.callback([Output('select-variable-x', 'options'),
               Output('select-variable-y', 'options')],
            [
                Input('dummy', 'children')
            ])
def set_options_variable(dummy):
    print("THIS IS cALLed")
    """
    loads in possible parameters for the x and y-axis from the data.
    TODO: Load the data in ones as a global variable. At the moment df is loaded in per function (inefficient).
    :param contents: contents of the data
    :param filename: filename of the data
    :return: Possible options for dropdown x-axis.
    """
    # df = pd.DataFrame({})
    # if (contents is not None):
    #     if contents:
    #         contents = contents[0]
    #         filename = filename[0]
    #         global df
    #         df = df.reset_index()
    # return [{'label': i, 'value': i} for i in df.columns], [{'label': i, 'value': i} for i in df.columns]

    if dummy:
        global df
        # df = df.reset_index()
    return [{'label': i, 'value': i} for i in df.columns], [{'label': i, 'value': i} for i in df.columns]


@app.callback([Output('select-variable-x', 'value'),
               Output('select-variable-y', 'value')],
            [
                Input('select-variable-x', 'options'),
                Input('select-variable-y', 'options')
            ])
def set_variables(options_x, options_y):
    """
    Gets the ouput of the dropdown of the 'select-variable-x' and 'select-variable-y'.
    :param options_x: All possible x-axis options
    :param options_y: All possible x-axis options
    :return: The choosen x-axis and y-axis
    """
    if len(options_y) <= 0 or (len(options_x) <= 0):
        return None, None
    return options_x[0]['value'], options_y[0]['value']

@app.callback(Output('Mygraph', 'figure'), [
# Input('upload-data', 'contents'),
# Input('upload-data', 'filename'),
Input('select-variable-x', 'value'),
Input('select-variable-y', 'value'),
Input('select-variable-y', 'value'),
])
def update_graph(xvalue, yvalue):
    """
    Displays the graph. Only normal plotting at the moment (x-axis, y-axis).
    TODO: Make different graphic plots possible.
    TODO: Make multiple y-axis in the same graph possible.
    TODO: Make separate graphic plots possible
    :param contents: contents of the data
    :param filename: filename of the data
    :param xvalue: Value of the x-axis
    :param yvalue: value of the y-axis
    :return:  graph
    """
    if (xvalue is None or yvalue is None):
        return {}
    if (xvalue == "index" or yvalue == "index"):
        return {}

    x = []
    y = []

    # if contents:
    #     contents = contents[0]
    #     filename = filename[0]
    global df
    if (df is not None):

        # df = df.reset_index()
        x = df['{}'.format(xvalue)]
        y = df['{}'.format(yvalue)]

        fig = go.Figure(
            data=[
                go.Scatter(
                    x=x,
                    y=y,

                    mode='markers')
                ],
            layout=go.Layout(
                plot_bgcolor=colors["graphBackground"],
                paper_bgcolor=colors["graphBackground"]
            ))
        return fig
    else:
        return {}

@app.callback(Output('output-data-upload', 'children'),
            [
               Input('dummy', 'children')
            ])
def update_table(dummy):
    """
    Makes a table from the uploaded data.
    :param contents: contents of the data
    :param filename: filename of the data
    :return: Table
    """
    table = html.Div()

    # if contents:
    #     contents = contents[0]
    #     filename = filename[0]
    if dummy:
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
                'wordBreak': 'break-all',
                'display': 'none'
            })
        ])

    return table

def parse_data(contents, filename):
    """
    Parses the data in a pandas dataframe.
    TODO: Make the dataframe global accessible.
    :param contents: contents of the data
    :param filename: filename of the data
    :return: Dataframe
    """
    if (contents is None):
        return

    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            global df
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df

if __name__ == '__main__':
    app.run_server(debug=True)
