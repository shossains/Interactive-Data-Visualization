import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
avocado = pd.read_csv('data/avocado-updated-2020.csv')

# Create the Dash app
app = dash.Dash()

# Set up the app layout
app.layout = html.Div(children=[
    html.H1(children='Avocado Prices Dashboard'),
    dcc.Dropdown(id='geo-dropdown',
                 options=[{'label': i, 'value': i}
                          for i in avocado['geography'].unique()],
                 value='New York'),
    dcc.Graph(id='price-graph')
])


# Set up the callback function
@app.callback(
    Output(component_id='price-graph', component_property='figure'),
    Input(component_id='geo-dropdown', component_property='value')
)
def update_graph(selected_geography):
    filtered_avocado = avocado[avocado['geography'] == selected_geography]
    line_fig = px.line(filtered_avocado,
                       x='date', y='average_price',
                       color='type',
                       title=f'Avocado Prices in {selected_geography}')
    return line_fig


# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)
