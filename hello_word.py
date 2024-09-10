import dash
from dash import html
from dash import dcc
import plotly.express as px
import plotly.io as pio

import pandas as pd

data=pd.read_csv("C:/Users/admin/Downloads/WAMSI/GHRSST_sst_point_15.csv", usecols=['time','analysed_sst'])

## create a figure

fig=px.line(data,x='time',y='analysed_sst', title='SST time series at the point 15')

fig.update_layout(
    template='plotly_dark',
    xaxis_title='Time',
    yaxis_title='SST',
    font=dict(
        family="Times New Roman",
        size=18,
        color="RebeccaPurple"
    )
)

app = dash.Dash(__name__)

app.title='SST time series at the point 15'

app.layout = html.Div(
    id="app-container",
    children=[
        html.H1("SST time series at the point 15"),
        html.P("This is a simple example of a Dash app."),
        dcc.Graph(figure=fig),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)