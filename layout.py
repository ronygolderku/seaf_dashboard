import dash_bootstrap_components as dbc
from dash import dcc, html

# Sidebar layout
sidebar = html.Div(
    [
        # Full sidebar content
        html.Div(
            [
                html.Img(src='/assets/logo.webp', style={'width': '100%', 'height': 'auto'}),  # Add logo here
                html.Hr(),

                # Home link
                dbc.NavLink("Home", href="/", style={'fontSize': '16px', 'fontWeight': 'bold'}),

                html.Hr(),

                # Datasets section with a collapsible button
                dbc.Button(
                    "Datasets", id="datasets-button", className="mb-2", n_clicks=0, style={'fontSize': '16px', 'fontWeight': 'bold', 'backgroundColor':  'transparent','border': 'none', 'color': 'green'}
                ),
                dbc.Collapse(
                    html.Div(
                        [
                            html.H2("European Space Agency (ESA)", className="display-0", style={'fontSize': '18px'}),
                            dbc.Button(
                                "Globcolor", id="globcolor-button", className="mb-2", n_clicks=0, 
                                style={'fontSize': '16px', 'marginBottom': '10px'}
                            ),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavLink("Reflectance", href="/esa/globcolor/reflectance", style={'fontSize': '14px'}),
                                        dbc.NavLink("PP", href="/esa/globcolor/pp", style={'fontSize': '14px'}),
                                        dbc.NavLink("Optics", href="/esa/globcolor/optics", style={'fontSize': '14px'}),
                                        dbc.NavLink("Transp", href="/esa/globcolor/transp", style={'fontSize': '14px'}),
                                        dbc.NavLink("Plankton", href="/esa/globcolor/plankton", style={'fontSize': '14px'}),
                                    ], vertical=True
                                ),
                                id="globcolor-collapse",
                                is_open=True,
                            ),

                            dbc.Button(
                                "Sentinel", id="sentinel-button", className="mb-2", n_clicks=0, 
                                style={'fontSize': '16px'}
                            ),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavLink("OLCI", href="/esa/sentinel/olci", style={'fontSize': '14px'}),
                                    ], vertical=True
                                ),
                                id="sentinel-collapse",
                                is_open=True,
                            ),

                            html.Hr(),

                            # UKMO section
                            html.H2("UK Met Office (UKMO)", className="display-6", style={'fontSize': '18px'}),
                            dbc.NavLink("OSTIA", href="/ukmo/ostia", style={'fontSize': '14px'}),

                            html.Hr(),

                            # NASA section
                            html.H2("NASA", className="display-6", style={'fontSize': '18px'}),
                            dbc.Button(
                                "GHRSST", id="ghrsst-button", className="mb-2", n_clicks=0, 
                                style={'fontSize': '16px'}
                            ),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavLink("MUR", href="/nasa/ghrsst/mur", style={'fontSize': '14px'}),
                                    ], vertical=True
                                ),
                                id="ghrsst-collapse",
                                is_open=True,
                            ),

                            dbc.Button(
                                "MODIS", id="modis-button", className="mb-2", n_clicks=0, 
                                style={'fontSize': '16px'}
                            ),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavLink("POC", href="/nasa/modis/poc", style={'fontSize': '14px'}),
                                        dbc.NavLink("PIC", href="/nasa/modis/pic", style={'fontSize': '14px'}),
                                        dbc.NavLink("PAR", href="/nasa/modis/par", style={'fontSize': '14px'}),
                                    ], vertical=True
                                ),
                                id="modis-collapse",
                                is_open=True,
                            ),

                            html.Hr(),

                            # MOI section
                            html.H2("Mercator Ocean International (MOI)", className="display-6", style={'fontSize': '18px'}),
                            dbc.Button(
                                "MODEL", id="model-button", className="mb-2", n_clicks=0, 
                                style={'fontSize': '16px'}
                            ),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavLink("PISCES", href="#", id="pisces-link", style={'fontSize': '14px'}),
                                        dbc.Collapse(
                                            dbc.Nav(
                                                [
                                                    dbc.NavLink("Bio", href="/moi/model/pisces/bio", style={'fontSize': '14px'}),
                                                    dbc.NavLink("Nut", href="/moi/model/pisces/nut", style={'fontSize': '14px'}),
                                                    dbc.NavLink("optics", href="/moi/model/pisces/optics", style={'fontSize': '14px'}),
                                                    dbc.NavLink("Car", href="/moi/model/pisces/car", style={'fontSize': '14px'}),
                                                    dbc.NavLink("PFTs", href="/moi/model/pisces/pfts", style={'fontSize': '14px'})
                                                ], vertical=True
                                            ),
                                            id="pisces-collapse",
                                            is_open=True,
                                        ),
                                        dbc.NavLink("SEAPODYM", href="#", id="seapodym-link", style={'fontSize': '14px'}),
                                        dbc.Collapse(
                                            dbc.Nav(
                                                [
                                                    dbc.NavLink("Biomass", href="/moi/model/seapodym/biomass", style={'fontSize': '14px'})
                                                ], vertical=True
                                            ),
                                            id="seapodym-collapse",
                                            is_open=True,
                                        ),

                                        dbc.NavLink("NEMO", href="#", id="nemo-link", style={'fontSize': '14px'}),
                                        dbc.Collapse(
                                            dbc.Nav([
                                                    dbc.NavLink("Salinity", href="/moi/model/nemo/salinity", style={'fontSize': '14px'})
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
            style={"display": "block"}  # Initially show the full sidebar
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
        "overflowY": "auto"  # Add scrollbar if content overflows
    }
)


# Content area
content = html.Div(id="page-content", style={"margin-left": "14rem", "padding": "2rem 1rem"})

# Main layout
layout = html.Div([dcc.Location(id="url"), sidebar, content])
