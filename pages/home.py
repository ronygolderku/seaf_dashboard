from dash import dcc, html
import dash_bootstrap_components as dbc

def home_layout():
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H2("Make Virtual Sensor with Satellite Data in Cockburn Sound (CS)", className="display-6"),
                    html.Hr(),
                    html.P(
                        "Cockburn Sound (CS) is monitored by numerous sensors providing continuous data on oceanic and atmospheric parameters. "
                        "These data streams are accessible through various agencies such as BOM, DWER, WAMSI, and UWA. However, in situ data may "
                        "not always be available for specific areas of interest, especially for assessing the environmental impacts of ongoing "
                        "development activities like WESTPORT.",
                        className="lead"
                    ),
                    html.P(
                        "Deploying sensors in such locations is costly, involving expenses for purchase, deployment, and maintenance. "
                        "To overcome these challenges, virtual sensors using satellite data can be a viable solution. Satellite data provide "
                        "comprehensive and continuous coverage, enabling effective environmental monitoring where physical sensors cannot be installed.",
                        className="lead"
                    ),
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H3("About this Repo", className="mt-4"),
                    html.P(
                        "This repository contains Python scripts designed to automate the downloading and processing of data from several key agencies: "
                        "the European Space Agency (ESA), UK Met Office (UKMO), NASA, Mercator Ocean International (MOI). The scripts are capable of "
                        "retrieving long-term datasets for specified geographical areas [points, polygons] and time ranges, converting the data into "
                        "CSV files, and scheduling the execution using GitHub Actions. The final processed data is then stored in the Pawsey S3 bucket.",
                        className="lead"
                    ),
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H3("Data Source and Data Point Position", className="mt-4"),
                    html.P(
                        "Explore the data point positions on the interactive map: ",
                        className="lead"
                    ),
                    dbc.Button("Data point position in the Map", href="#", color="primary", className="mt-2"),
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H3("Data Sources", className="mt-4"),
                    html.Ul([
                        html.Li("ESA: GLOBCOLOR (resolution: 4km) and Sentinel (resolution: 300m) marine environment products."),
                        html.Li("MOI: Numerous MODEL output."),
                        html.Li("UKMO: Access data from OSTIA temperature (resolution: 0.05°) products."),
                        html.Li("NASA: Access data from the Group for High-Resolution Sea Surface Temperature (GHRSST (resolution: 0.01°)) and MODIS (resolution: 4km) through ERDDAP."),
                    ], className="lead")
                ], width=12)
            ]),
        ], fluid=True)
    ], style={"padding": "20px"})
