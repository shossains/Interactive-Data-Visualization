import base64
import datetime
import io
import plotly.graph_objs as go
import cufflinks as cf

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import pandas as pd

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
                    {'label': 'T-sne (not implemented)', 'value': 'T-sne'},
                    {'label': 'other_ml_tool  (not implemented)', 'value': 'other_ml_tool'}
                ],
                value='T-sne'
            ),
    html.H4("Select variable x"),
    dcc.Dropdown(id='select-variable-x'),
    html.H4("Select variable y"),
    dcc.Dropdown(
        id='select-variable-y',
        multi=True),
    html.Div(id='output-select-data'),
    dcc.Graph(id='Mygraph'),
    html.Div(id='output-data-upload')
])



@app.callback(Output('select-variable-x', 'options'),
            [
                Input('upload-data', 'contents'),
                Input('upload-data', 'filename'),
            ])
def set_options_variable_x(contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
    df = parse_data(contents, filename)
    df = df.reset_index()

    return [{'label': i, 'value': i} for i in df.columns]


@app.callback(Output('select-variable-x', 'value'),
            [
                Input('select-variable-x', 'options')
            ])
def set_variable_x(options_x ):
    return options_x[0]['value']


@app.callback(Output('select-variable-y', 'options'),
            [
                Input('upload-data', 'contents'),
                Input('upload-data', 'filename'),
            ])
def set_options_variable_y(contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
    df = parse_data(contents, filename)
    df = df.reset_index()

    return [{'label': i, 'value': i} for i in df.columns]


@app.callback(Output('select-variable-y', 'value'),
            [
                Input('select-variable-y', 'options')
            ])
def set_variable_x(options_y ):
    return options_y[0]['value']



@app.callback(Output('Mygraph', 'figure'), [
Input('upload-data', 'contents'),
Input('upload-data', 'filename'),
Input('select-variable-x', 'value'),
Input('select-variable-y', 'value'),
])
def update_graph(contents, filename, xvalue, yvalue):
    x = []
    y = []

    if contents:
        contents = contents[0]
        filename = filename[0]
    df = parse_data(contents, filename)
    df = df.reset_index()
    print("xvalue: {} yvalue: {}".format(xvalue, yvalue))
    x = df['{}'.format(xvalue)]
    for ycol in yvalue:
        print(ycol)
        y = df[ycol]
    fig = go.Figure(
        data=[
            go.Scatter(
                x=x,
                y=y,
                mode='lines+markers')
            ],
        layout=go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"]
        ))
    return fig

@app.callback(Output('output-data-upload', 'children'),
            [
                Input('upload-data', 'contents'),
                Input('upload-data', 'filename')
            ])
def update_table(contents, filename):
    table = html.Div()

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)


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
        ])

    return table

def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
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
