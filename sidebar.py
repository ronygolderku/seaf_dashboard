import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sidebar structure based on your provided folder structure
sidebar = html.Div(
    [
        html.H1("European Space Agency (ESA)", className="display-6"),
        html.Hr(),
        html.H2("Globcolor (4 km) [DAILY]", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Reflectance", href="#"),
                dbc.NavLink("PP [mg C m⁻² d⁻¹]", href="#"),
                dbc.NavLink("Optics", href="#"),
                dbc.NavLink("Transp", href="#"),
                dbc.NavLink("Plankton", href="#"),
            ], vertical=True
        ),
        html.H2("Sentinel (300 m) [DAILY]", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("OLCI", href="#"),
                dbc.NavLink("CHL [mg m⁻³]", href="#"),
            ], vertical=True
        ),
        html.H1("UK Met Office (UKMO)", className="display-6"),
        html.Hr(),
        dbc.NavLink("OSTIA (~ 5 km) [DAILY]", href="#"),
        html.H1("NASA", className="display-6"),
        html.Hr(),
        html.H2("GHRSST (~1 km) [DAILY]", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("MUR", href="#"),
                dbc.NavLink("SST [°C]", href="#"),
            ], vertical=True
        ),
        html.H2("MODIS [MONTHLY]", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("POC [mg m⁻³]", href="#"),
                dbc.NavLink("PIC [mg m⁻³]", href="#"),
                dbc.NavLink("PAR [Einstein m⁻² d⁻¹]", href="#"),
            ], vertical=True
        ),
        html.H1("Mercator Ocean International (MOI)", className="display-6"),
        html.Hr(),
        html.H2("MODEL", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("PISCES (~25 km) [DAILY]", href="#"),
                dbc.NavLink("SEAPODYM (~ 9 km) [DAILY]", href="#"),
                dbc.NavLink("NEMO (~ 9 km) [EVERY 6 HOUR]", href="#"),
            ], vertical=True
        ),
    ],
    style={
        "position": "fixed",
        "top": 0, "left": 0, "bottom": 0,
        "width": "20rem", "padding": "2rem 1rem",
        "background-color": "#f8f9fa"
    }
)

# Content area
content = html.Div(id="page-content", style={"margin-left": "22rem", "padding": "2rem 1rem"})

# Layout with sidebar and content
app.layout = html.Div([sidebar, content])

# Example callbacks to update content area based on sidebar clicks
@app.callback(
    Output("page-content", "children"),
    [Input("navlink_id_here", "n_clicks")]  # Add similar inputs for other nav links
)
def display_content(n_clicks):
    # Depending on which navlink is clicked, return different content.
    # Example content for ESA:
    if n_clicks:
        return html.Div([
            dl.Map(center=[51.505, -0.09], zoom=10, children=[dl.TileLayer()]),
            dcc.Graph(figure=px.scatter(x=[1, 2, 3], y=[4, 1, 2]))
        ])
    return "Select an item from the sidebar."

if __name__ == "__main__":
    app.run_server(debug=True)
