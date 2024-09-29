import dash_bootstrap_components as dbc
from dash import dcc, html

# Sidebar layout
sidebar = html.Div(
    [
        html.Div(
            [
                html.Img(src='/assets/logo.webp', style={'width': '100%', 'height': 'auto'}),
                html.Hr(),
                dbc.NavLink([html.I(className="fas fa-home"), " Home"], href="/", style={'fontSize': '16px', 'fontWeight': 'bold'}),
                html.Hr(),
                dbc.Button(
                    [html.I(className="fas fa-database"), " Datasets"], id="datasets-button", className="mb-2", n_clicks=0,
                    style={'fontSize': '16px', 'fontWeight': 'bold', 'backgroundColor': 'transparent', 'border': 'none', 'color': 'green'}
                ),
                dbc.Collapse(
                    html.Div(
                        [
                            html.H2("European Space Agency (ESA)", className="display-0", style={'fontSize': '18px'}),
                            dbc.Button(
                                [html.I(className="fas fa-globe"), " GlobColour"], id="globcolor-button", className="mb-2", n_clicks=0,
                                style={'fontSize': '16px', 'marginBottom': '10px'}
                            ),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavLink([html.I(className="fas fa-sun"), " Reflectance"], href="/esa/globcolor/reflectance", style={'fontSize': '14px', 'paddingLeft': '20px'}),
                                        dbc.NavLink([html.I(className="fas fa-water"), " PP"], href="/esa/globcolor/pp", style={'fontSize': '14px', 'paddingLeft': '20px'}),
                                        dbc.NavLink([html.I(className="fas fa-eye"), " Optics"], href="/esa/globcolor/optics", style={'fontSize': '14px', 'paddingLeft': '20px'}),
                                        dbc.NavLink([html.I(className="fas fa-tint"), " Transp"], href="/esa/globcolor/transp", style={'fontSize': '14px', 'paddingLeft': '20px'}),
                                        dbc.NavLink([html.I(className="fas fa-fish"), " Plankton"], href="/esa/globcolor/plankton", style={'fontSize': '14px', 'paddingLeft': '20px'}),
                                    ], vertical=True
                                ),
                                id="globcolor-collapse",
                                is_open=True,
                            ),
                            dbc.Button(
                                [html.I(className="fas fa-satellite"), " Sentinel"], id="sentinel-button", className="mb-2", n_clicks=0,
                                style={'fontSize': '16px'}
                            ),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavLink([html.I(className="fas fa-leaf"), " Chl-a"], href="/esa/sentinel/olci", style={'fontSize': '14px', 'paddingLeft': '20px'}),
                                    ], vertical=True
                                ),
                                id="sentinel-collapse",
                                is_open=True,
                            ),
                            html.Hr(),
                            html.H2("UK Met Office (UKMO)", className="display-6", style={'fontSize': '18px'}),
                            dbc.NavLink([html.I(className="fas fa-cloud"), " SST"], href="/ukmo/ostia", style={'fontSize': '14px'}),
                            html.Hr(),
                            html.H2("NASA", className="display-6", style={'fontSize': '18px'}),
                            dbc.Button(
                                [html.I(className="fas fa-thermometer-half"), " GHRSST"], id="ghrsst-button", className="mb-2", n_clicks=0,
                                style={'fontSize': '16px'}
                            ),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavLink([html.I(className="fas fa-map"), " SST"], href="/nasa/ghrsst/mur", style={'fontSize': '14px', 'paddingLeft': '20px'}),
                                    ], vertical=True
                                ),
                                id="ghrsst-collapse",
                                is_open=True,
                            ),
                            dbc.Button(
                                [html.I(className="fas fa-satellite-dish"), " MODIS"], id="modis-button", className="mb-2", n_clicks=0,
                                style={'fontSize': '16px'}
                            ),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavLink([html.I(className="fas fa-leaf"), " POC"], href="/nasa/modis/poc", style={'fontSize': '14px', 'paddingLeft': '20px'}),
                                        dbc.NavLink([html.I(className="fas fa-cube"), " PIC"], href="/nasa/modis/pic", style={'fontSize': '14px', 'paddingLeft': '20px'}),
                                        dbc.NavLink([html.I(className="fas fa-lightbulb"), " PAR"], href="/nasa/modis/par", style={'fontSize': '14px', 'paddingLeft': '20px'}),
                                    ], vertical=True
                                ),
                                id="modis-collapse",
                                is_open=True,
                            ),
                            html.Hr(),
                            html.H2("Mercator Ocean International (MOI)", className="display-6", style={'fontSize': '18px'}),
                            dbc.Button(
                                [html.I(className="fas fa-cogs"), " MODEL"], id="model-button", className="mb-2", n_clicks=0,
                                style={'fontSize': '16px'}
                            ),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavLink([html.I(className="fas fa-fish"), html.B(" PISCES")], href="#", id="pisces-link", style={'fontSize': '14px', 'paddingLeft': '20px'}),
                                        dbc.Collapse(
                                            dbc.Nav(
                                                [
                                                    dbc.NavLink([html.I(className="fas fa-dna"), " Bio"], href="/moi/model/pisces/bio", style={'fontSize': '14px', 'paddingLeft': '40px'}),
                                                    dbc.NavLink([html.I(className="fas fa-apple-alt"), " Nut"], href="/moi/model/pisces/nut", style={'fontSize': '14px', 'paddingLeft': '40px'}),
                                                    dbc.NavLink([html.I(className="fas fa-eye"), " Optics"], href="/moi/model/pisces/optics", style={'fontSize': '14px', 'paddingLeft': '40px'}),
                                                    dbc.NavLink([html.I(className="fas fa-leaf"), " Car"], href="/moi/model/pisces/car", style={'fontSize': '14px', 'paddingLeft': '40px'}),
                                                    dbc.NavLink([html.I(className="fas fa-cube"), " CO₂"], href="/moi/model/pisces/co2", style={'fontSize': '14px', 'paddingLeft': '40px'}),
                                                    dbc.NavLink([html.I(className="fas fa-seedling"), " PFTs"], href="/moi/model/pisces/pfts", style={'fontSize': '14px', 'paddingLeft': '40px'})
                                                ], vertical=True
                                            ),
                                            id="pisces-collapse",
                                            is_open=True,
                                        ),
                                        dbc.NavLink([html.I(className="fas fa-fish"), html.B(" SEAPODYM")], href="#", id="seapodym-link", style={'fontSize': '14px', 'paddingLeft': '20px'}),
                                        dbc.Collapse(
                                            dbc.Nav(
                                                [
                                                    dbc.NavLink([html.I(className="fas fa-weight"), " Biomass"], href="/moi/model/seapodym/biomass", style={'fontSize': '14px', 'paddingLeft': '40px'})
                                                ], vertical=True
                                            ),
                                            id="seapodym-collapse",
                                            is_open=True,
                                        ),
                                        dbc.NavLink([html.I(className="fas fa-water"), html.B(" NEMO")], href="#", id="nemo-link", style={'fontSize': '14px', 'paddingLeft': '20px'}),
                                        dbc.Collapse(
                                            dbc.Nav(
                                                [
                                                    dbc.NavLink([html.I(className="fas fa-tint"), " Salinity"], href="/moi/model/nemo/salinity", style={'fontSize': '14px', 'paddingLeft': '40px'})
                                                ], vertical=True
                                            ),
                                            id="nemo-collapse",
                                            is_open=True,
                                        ),
                                    ], vertical=True
                                ),
                                id="model-collapse",
                                is_open=True,
                            ),
                        ]
                    ),
                    id="datasets-collapse",
                    is_open=False,
                ),
            ],
            id="sidebar-content",
            style={"display": "block"}
        ),
    ],
    className="sidebar",
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "14rem",
        "padding": "2rem 1rem",
        "backgroundColor": "#f8f9fa",
        "overflowY": "auto"
    }
)

# Content area
content = html.Div(id="page-content", style={"margin-left": "14rem", "padding": "2rem 1rem"})

# Main layout
layout = html.Div([dcc.Location(id="url"), sidebar, content])
