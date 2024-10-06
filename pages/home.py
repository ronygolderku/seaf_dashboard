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
        ["ESA", "Sentinel", "OLCI", "Chl-a"],
        ["UKMO", "GHRSST", "OSTIA", "Temp"],
        ["NASA", "MODIS", "MODIS", "POC, PIC, PAR"],
        ["NASA", "GHRSST", "MUR", "SST"],
        ["MOI", "PISCES", "BIO", "NPPV, O₂"],
        ["MOI", "PISCES", "NUT", "Fe, NO₃, PO₄, Si"],
        ["MOI", "PISCES", "OPTICS", "KD"],
        ["MOI", "PISCES", "Car", "DIC, PH, Talk"],
        ["MOI", "PISCES", "CO₂", "spCO₂"],
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
                size=24,  # Increase the font size
                family="Times New Roman",  # Set the font to Times New Roman
                weight="bold",
                color="black"  # Set the font color to black
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
            "opacity": "1",
            "margin-top": "0px",
            "margin-bottom": "20px"
        }),
        # Add a button to open the guide modal
        html.Div([
            dbc.Button("🚀 How to Explore the Dashboard", 
                       id="open-guide-modal", 
                       className="bounce-animated delayed-start mb-4", 
                       color="primary", 
                       style={"font-size": "18px", "font-weight": "bold"}
            ),
        ], style={"text-align": "center"}),
        
        # Guide Modal
        dbc.Modal([
            dbc.ModalHeader("🌟 Dashboard Guide"),
            dbc.ModalBody([
                html.H5("Welcome to the Dashboard!"),
                html.P("This dashboard presents environmental datasets collected from various agencies. Here's how you can make the most out of it:"),
                        html.Ul([
                            html.Li([
                                "Use the sidebar to navigate different datasets by clicking the ", 
                                html.Span([
                                    html.I(className="fas fa-database", style={"margin-right": "5px"}),
                                    html.B("Datasets")
                                ], style={"color": "green"}), 
                                " button."
                            ]),
                            html.Li([
                                "In each dataset layout, click the ", 
                                html.B("About"), 
                                " section to learn more about the dataset properties, source, and data processing."
                            ]),
                            html.Li([
                                "Click on the map layer (left side) under each layout and explore dataset positions as well as the WMS layer."
                            ]),
                            html.Li([
                                "Use the dropdowns and filters to customize your view of the data."
                            ]),
                        ], className="custom-list"),
                html.P("Feel free to reach out for further assistance using the contact links below."),
                html.P([
                    html.I(className="fas fa-envelope", style={"color": "blue", "margin-right": "5px"}),
                    html.A("Md Rony Golder", href="mailto:mdrony.golder@uwa.edu.au", style={"color": "blue"})
                ])
            ]),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-guide-modal", className="ml-auto", color="secondary")
            ),
        ], id="guide-modal", is_open=False),

        # Cards for key information
        dbc.Container([
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Agencies", className="card-title", style={"text-align": "center", "font-weight": "bold"}),
                        html.P("4", className="card-text", style={
                            "font-size": "2em",
                            "background-color": "white",
                            "border-radius": "50%",
                            "width": "50px",
                            "height": "50px",
                            "line-height": "50px",
                            "text-align": "center",
                            "margin": "0 auto"
                        })
                    ])
                ], style={"background-color": "#a4c126", "border": "1px solid #dee2e6", "padding": "10px", "margin": "10px"}), width=12, md=4),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Datasets", className="card-title", style={"text-align": "center", "font-weight": "bold"}),
                        html.P("17", className="card-text", style={
                            "font-size": "2em",
                            "background-color": "white",
                            "border-radius": "50%",
                            "width": "50px",
                            "height": "50px",
                            "line-height": "50px",
                            "text-align": "center",
                            "margin": "0 auto"
                        })
                    ])
                ], style={"background-color": "#008bad", "border": "1px solid #dee2e6", "padding": "10px", "margin": "10px"}), width=12, md=4),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Variables", className="card-title", style={"text-align": "center", "font-weight": "bold"}),
                        html.P("43", className="card-text", style={
                            "font-size": "2em",
                            "background-color": "white",
                            "border-radius": "50%",
                            "width": "50px",
                            "height": "50px",
                            "line-height": "50px",
                            "text-align": "center",
                            "margin": "0 auto"
                        })
                    ])
                ], style={"background-color": "#f3bc00", "border": "1px solid #dee2e6", "padding": "10px", "margin": "10px"}), width=12, md=4),
            ], className="mb-4"),
        ]),

        # Sunburst chart and agencies description
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Agencies", style={"font-weight": "bold"}),  # Heading
                        html.Ul([  # Unordered list
                            html.Li([html.Span("ESA: ", style={"font-weight": "bold"}), "European Space Agency"]),
                            html.Li([html.Span("NASA: ", style={"font-weight": "bold"}), "National Aeronautics and Space Administration"]),
                            html.Li([html.Span("UKMO: ", style={"font-weight": "bold"}), "United Kingdom Meteorological Office"]),
                            html.Li([html.Span("MOI: ", style={"font-weight": "bold"}), "Mercator Ocean International"])
                        ], style={"margin-bottom": "20px"}),  # Add space between lists
                        html.H4("Programs", style={"font-weight": "bold"}),  # Heading
                        html.Ul([  # Unordered list
                            html.Li([html.Span("GlobColour: ", style={"font-weight": "bold"}), "Global Ocean Colour"]),
                            html.Li([html.Span("GHRSST: ", style={"font-weight": "bold"}), "Group for High Resolution Sea Surface Temperature"]),
                            html.Li([html.Span("NEMO: ", style={"font-weight": "bold"}), "Nucleus for European Modelling of the Ocean"]),
                            html.Li([html.Span("PISCES: ", style={"font-weight": "bold"}), "Pelagic Interactions Scheme for Carbon and Ecosystem Studies"]),
                            html.Li([html.Span("SEAPODYM: ", style={"font-weight": "bold"}), "Spatial Ecosystem and Population Dynamics Model"]),
                            html.Li([html.Span("MODIS: ", style={"font-weight": "bold"}), "Moderate Resolution Imaging Spectroradiometer"]),
                            html.Li([html.Span("OLCI: ", style={"font-weight": "bold"}), "Ocean and Land Colour Instrument"]),
                            html.Li([html.Span("OSTIA: ", style={"font-weight": "bold"}), "Operational Sea Surface Temperature and Sea Ice Analysis"]),
                        ], style={"margin-bottom": "20px"})  # Add space between lists
                    ], style={"padding": "10px", "flex": "1"})  # Right column with the full forms
                ], width=12, md=6),
                dbc.Col([
                    dcc.Graph(figure=create_sunburst_chart()),  # Left column with the figure
                ], width=12, md=6)
            ], style={"margin-bottom": "20px"}),
        ]),

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

        # Footer with contact information
        dbc.Container([
            # Central container for left and right parts
            dbc.Row([
                dbc.Col([
                    # Left: WAMSI logo and social icons
                    html.Div([
                        html.A(
                            html.Img(
                                src="assets/wamsi-logo.png",  # Replace with actual WAMSI logo URL
                                height="50px", style={"margin-right": "15px"}
                            ),
                            href="https://www.wamsi.org.au", target="_blank"
                        ),
                        html.Div([
                            html.A(
                                html.I(className="fab fa-facebook-f fa-lg"),
                                href="https://www.facebook.com/WesternAustralianMarineScience", target="_blank",
                                style={"margin-right": "15px", "color": "#4267B2"}
                            ),
                            html.A(
                                html.I(className="fab fa-youtube fa-lg"),
                                href="https://www.youtube.com/user/WAMSIHQ", target="_blank",
                                style={"margin-right": "15px", "color": "#FF0000"}
                            ),
                            html.A(
                                html.I(className="fab fa-linkedin fa-lg"),
                                href="https://www.linkedin.com/company/wamsi/", target="_blank",
                                style={"margin-right": "15px", "color": "#0A66C2"}
                            ),
                            html.A(
                                html.I(className="fab fa-instagram fa-lg"),
                                href="https://www.instagram.com/westernaustralianmarinescience", target="_blank",
                                style={"color": "#E1306C"}
                            ),
                        ], style={"display": "flex", "align-items": "center"})
                    ], style={"display": "flex", "align-items": "center", "justify-content": "flex-end"})
                ], width=5, style={"text-align": "right"}),
        
                # Vertical black line
                dbc.Col(html.Div(style={"border-right": "3px solid black", "height": "60px"}), width=1, style={"padding": "30px"}),
        
                # Right: GitHub link, copyright, email
                dbc.Col([
                    html.Div([
                        # GitHub link
                        html.A(
                            html.I(className="fab fa-github fa-lg"),
                            href="https://github.com/ronygolderku/seaf_dashboard", target="_blank",
                            style={"color": "#000000", "display": "inline-block", "margin-right": "5px"}
                        ),
                        html.A("View Source Code", href="https://github.com/ronygolderku/seaf_dashboard", target="_blank",
                               style={"font-size": "12px", "color": "#000000", "display": "inline-block", "margin-right": "15px"}),
        
                        # Email
                        html.Div([
                            html.I(className="fas fa-envelope", style={"color": "blue", "margin-right": "5px"}),
                            html.A("Md Rony Golder", href="mailto:mdrony.golder@uwa.edu.au", style={"color": "blue", "font-size": "12px"})
                        ], style={"display": "inline-block", "margin-right": "15px"}),
        
                        # Copyright
                        html.P("© 2024 Md Rony Golder. All rights reserved.", style={"font-size": "12px", "display": "inline-block", "margin-bottom": "0"})
                    ], style={"display": "flex", "align-items": "center", "justify-content": "flex-start"})
                ], width=5, style={"padding-left": "0"})
            ], style={"display": "flex", "align-items": "center", "justify-content": "center"}),
        
            # Bottom: Acknowledgment text
            dbc.Row([
                dbc.Col([
                    html.P(
                        "WAMSI acknowledges the traditional custodians of Country throughout Western Australia and their "
                        "continuing connection to land, culture and community. We pay our respects to elders past and present.",
                        style={"font-size": "10px", "text-align": "center"}
                    ),
                ], width=12, style={"display": "flex", "align-items": "center", "justify-content": "center"})
            ]),
        
        ], fluid=True, style={"padding": "5px 0", "background-color": "#f8f9fa", "border-top": "1px solid #dee2e6", "border-bottom": "1px solid #dee2e6"})
    ])