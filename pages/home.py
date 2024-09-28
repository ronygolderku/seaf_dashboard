from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.colors

# Function to generate the data for the sunburst chart
def generate_sunburst_data():
    data = [
        ["ESA", "Globcolor", "Reflectance", "RRS412, RRS443, RRS490, RRS555, RRS670"],
        ["ESA", "Globcolor", "Optics", "BBP, CDM"],
        ["ESA", "Globcolor", "Transp", "KD490, ZSD, SPM"],
        ["ESA", "Globcolor", "Plankton", "CHL, DIATO, DINO, GREEN, HAPTO, MICRO, NANO, PICO, PROCHLO, PROKAR"],
        ["ESA", "Globcolor", "PP", "PP"],
        ["ESA", "Sentinel", "OLCI", "Chl"],
        ["UKMO", "GHRSST", "OSTIA", "Temp"],
        ["NASA", "MODIS", "MODIS", "POC, PIC, PAR"],
        ["NASA", "GHRSST", "MUR", "SST"],
        ["MOI", "PISCES", "BIO", "NPPV, O2"],
        ["MOI", "PISCES", "NUT", "Fe, No3, PO4, Si"],
        ["MOI", "PISCES", "OPTICS", "KD"],
        ["MOI", "PISCES", "Car", "DIC, PH, Talk"],
        ["MOI", "PISCES", "CO2", "SPCO2"],
        ["MOI", "PISCES", "PFTs", "CHL, Phyto"],
        ["MOI", "SEAPODYM", "Biomass", "PP, ZOO"],
        ["MOI", "NEMO", "SAL", "Salinity"]
    ]

    labels = ["Datasets"]  # Starting point for the hierarchy
    parents = [""]    # The root has no parent

    for agency, program, category, variables in data:
        if agency not in labels:
            labels.append(agency)
            parents.append("Datasets")

        if program not in labels:
            labels.append(program)
            parents.append(agency)

        if category not in labels:
            labels.append(category)
            parents.append(program)

        for variable in variables.split(", "):
            if variable not in labels:
                labels.append(variable)
                parents.append(category)

    return labels, parents

# Function to create the sunburst chart
def create_sunburst_chart():
    labels, parents = generate_sunburst_data()
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        branchvalues="total",
        marker=dict(colors=plotly.colors.qualitative.Pastel)  # Applying a color scheme
    ))
    #fig.update_traces(textinfo='label+percent entry')
    fig.update_layout(
        margin=dict(t=50, l=0, r=0, b=0),
        title=dict(
            text="Available Datasets",
            x=0.5,  # Center the title
            xanchor='center',
            yanchor='top',
            font=dict(
                size=24  # Increase the font size
            )
        )
    )
    return fig

# Define the layout for the Dash application
def home_layout():
    return html.Div([
        # Header with background image
        html.Div([
            html.H1("Data Visualization Dashboard", className="display-3 text-white"),
            html.H5("Based on Satellite and MODEL Output", className="display-7 text-white"),
            html.P(
                "Explore the distribution of environmental datasets from agencies like NASA, ESA, UKMO, and MOI for the region of Cockburn Sound (CS).",
                className="lead text-white"
            ),
        ], style={
            "background-image": "url('/assets/back_ground.jpg')",
            "background-size": "cover",
            "padding": "15px",
            "text-align": "center",
            "height": "200px",
            "margin-bottom": "20px"
        }),

        # Main content
        dbc.Container([
            # Interactive map with title
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.H4("Dataset Position Map", className="text-center mb-4"), width=12)
                ]),
                dbc.Row([
                    dbc.Col(html.Div([
                        html.Iframe(
                            src="https://curtin.maps.arcgis.com/apps/instant/basic/index.html?appid=dd40758d043c4871bc6aedfc6bd178c8",
                            style={"border": "0", "width": "100%", "height": "600px"},
                        ),
                        html.P("iFrames are not supported on this page.", style={"display": "none"})
                    ]), width=12)
                ])
            ], style={"margin-bottom": "20px"}),

            # Cards for key information
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Datasets", className="card-title"),
                        html.P("17", className="card-text")
                    ])
                ], style={"background-color": "#f8f9fa", "border": "1px solid #dee2e6", "padding": "10px", "margin": "10px"}), width=4),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Agencies", className="card-title"),
                        html.P("4", className="card-text")
                    ])
                ], style={"background-color": "#f8f9fa", "border": "1px solid #dee2e6", "padding": "10px", "margin": "10px"}), width=4),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Variables", className="card-title"),
                        html.P("43", className="card-text")
                    ])
                ], style={"background-color": "#f8f9fa", "border": "1px solid #dee2e6", "padding": "10px", "margin": "10px"}), width=4),
            ], className="mb-4"),

            # Sunburst chart
            dbc.Row([
                dbc.Col(dcc.Graph(figure=create_sunburst_chart()), width=12)
            ], style={"margin-bottom": "20px"}),

            # Footer with contact information
            dbc.Container([
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        html.P("© 2024 Md Rony Golder. All rights reserved.", style={"text-align": "center"}),
                        html.A("MD RONY GOLDER", href="mailto:mdrony.golder@uwa.edu.au", style={"display": "block", "text-align": "center", "color": "blue"}),
                    ], width=12),
                ]),
            ], fluid=True, style={"padding": "20px 0", "background-color": "#f8f9fa"}),
        ])
    ])