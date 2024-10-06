import os
import boto3
import pandas as pd
import plotly.express as px
import geopandas as gpd
from dash import Input, Output, State, dcc, html
from dash import Input, Output, State
from pages.home import home_layout
import dash_leaflet as dl
#ghrsst_mur_layout, reflectance_layout, plankton_layout
from pages.data_viz import olci_layout, ghrsst_mur_layout, plankton_layout, reflectance_layout, create_points_layer, points_df, geojson_data, transp_layout, optics_layout, pp_layout, ostia_layout, poc_layout, par_layout, pic_layout, mod_bio_layout, mod_nut_layout, mod_car_layout, mod_biomass_layout, mod_co2_layout, mod_optics_layout, mod_pfts_layout, mod_sal_layout
from s3_fetch import s3_client, fetch_data_from_s3

polygon_key_mapping = {str(i): f"Polygons_{i}_MultiPolygon.shp" for i in range(1, 7)}  # Ensure ".shp" extension
variable_info = {
    'CHL': {'label': 'Chlorophyll-a [mg/m³]', 'value': 'CHL'},
    'analysed_sst': {
        'label': {
            'celsius': 'Sea Surface Temperature [°C]',
            'kelvin': 'Sea Surface Temperature [°K]'
        },
        'value': 'analysed_sst'
    },
    'KD490': {'label': 'diffuse attenuation coefficient at 490 nm [m-¹]', 'value': 'KD490'},
    'ZSD': {'label': 'Secchi disk depth [m]', 'value': 'ZSD'},
    'SPM': {'label': 'Suspended particulate matter [g/m³]', 'value': 'SPM'},
    'DIATO': {'label': 'Diatoms [mg m⁻³]', 'value': 'DIATO'},
    'DINO': {'label': 'Dinoflagellates [mg m⁻³]', 'value': 'DINO'},
    'GREEN': {'label': 'Green Algae [mg m⁻³]', 'value': 'GREEN'},
    'HAPTO': {'label': 'Haptophytes [mg m⁻³]', 'value': 'HAPTO'},
    'MICRO': {'label': 'Microplankton [mg m⁻³]', 'value': 'MICRO'},
    'NANO': {'label': 'Nanoplankton [mg m⁻³]', 'value': 'NANO'},
    'PICO': {'label': 'Picoplankton [mg m⁻³]', 'value': 'PICO'},
    'PROCHLO': {'label': 'Prochlorococcus [mg m⁻³]', 'value': 'PROCHLO'},
    'PROKAR': {'label': 'Prokaryotes [mg m⁻³]', 'value': 'PROKAR'},
    'RRS412': {'label': 'RS reflectance at 412nm [sr⁻¹]', 'value': 'RRS412'},
    'RRS443': {'label': 'RS reflectance at 443nm [sr⁻¹]', 'value': 'RRS443'},
    'RRS490': {'label': 'RS reflectance at 490nm [sr⁻¹]', 'value': 'RRS490'},
    'RRS555': {'label': 'RS reflectance at 555nm [sr⁻¹]', 'value': 'RRS555'},
    'RRS670': {'label': 'RS reflectance at 670nm [sr⁻¹]', 'value': 'RRS670'},
    'BBP': {'label': 'Backscattering coefficient [m⁻¹]', 'value': 'BBP'},
    'CDM': {'label': 'Colored Dissolved Organic Matter [m⁻¹]', 'value': 'CDM'},
    'PP': {'label': 'Primary Production [mg C m⁻² day⁻¹]', 'value': 'PP'},
    'pic': {'label': 'Particulate Inorganic Carbon [mg m⁻³]', 'value': 'pic'},
    'poc': {'label': 'Particulate Organic Carbon [mg m⁻³]', 'value': 'poc'},
    'par': {'label': 'PAR [Einstein m⁻² d⁻¹]', 'value': 'par'},
    'nppv': {'label': 'Net Primary Production [mg C m⁻² day⁻¹]', 'value': 'nppv'},
    'o2': {'label': 'Dissolved Oxygen [mmol m⁻³]', 'value': 'o2'},
    'fe': {'label': 'Dissolved Iron [mmol m⁻³]', 'value': 'fe'},
    'si': {'label': 'Dissolved Silicate [mmol m⁻³]', 'value': 'si'},
    'no3': {'label': 'Nitrate [mmol m⁻³]', 'value': 'no3'},
    'po4': {'label': 'Phosphate [mmol m⁻³]', 'value': 'po4'},
    'kd': {'label': 'Volume attenuation coefficient [m⁻¹]', 'value': 'kd'},
    'talk': {'label': 'Total Alkalinity [mol m⁻³]', 'value': 'talk'},
    'dissic': {'label': 'Dissolved Inorganic Carbon [mol m⁻³]', 'value': 'dissic'},
    'spco2': {'label': 'Sea Surface pCO2 [Pa]', 'value': 'spco2'},
    'chl': {'label': 'Chlorophyll-a [mg m⁻³]', 'value': 'chl'},
    'phyc': {'label': 'Phytoplankton [mmol m⁻³]', 'value': 'phyc'},
    'zooc': {'label': 'Zooplankton [g m⁻³]', 'value': 'zooc'},
    'npp': {'label': 'Net Primary Production [mg C m⁻² day⁻¹]', 'value': 'npp'},
    'so': {'label': 'Salinity [PSU]', 'value': 'so'},
}


def register_callbacks(app):
    @app.callback(
        Output("datasets-collapse", "is_open"),
        [Input("datasets-button", "n_clicks")],
        [State("datasets-collapse", "is_open")]
    )
    def toggle_datasets_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("globcolor-collapse", "is_open"),
        [Input("globcolor-button", "n_clicks")],
        [State("globcolor-collapse", "is_open")]
    )
    def toggle_globcolor_collapse(n, is_open):
        if n:
            return not is_open
        return is_open
    
    @app.callback(
        Output("sentinel-collapse", "is_open"),
        [Input("sentinel-button", "n_clicks")],
        [State("sentinel-collapse", "is_open")]
    )
    def toggle_sentinel_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("ghrsst-collapse", "is_open"),
        [Input("ghrsst-button", "n_clicks")],
        [State("ghrsst-collapse", "is_open")]
    )
    def toggle_ghrsst_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("modis-collapse", "is_open"),
        [Input("modis-button", "n_clicks")],
        [State("modis-collapse", "is_open")]
    )
    def toggle_modis_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("model-collapse", "is_open"),
        [Input("model-button", "n_clicks")],
        [State("model-collapse", "is_open")]
    )
    def toggle_model_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("pisces-collapse", "is_open"),
        [Input("pisces-link", "n_clicks")],
        [State("pisces-collapse", "is_open")]
    )
    def toggle_pisces_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("seapodym-collapse", "is_open"),
        [Input("seapodym-link", "n_clicks")],
        [State("seapodym-collapse", "is_open")]
    )
    def toggle_seapodym_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("nemo-collapse", "is_open"),
        [Input("nemo-link", "n_clicks")],
        [State("nemo-collapse", "is_open")]
    )
    def toggle_nemo_collapse(n, is_open):
        if n:
            return not is_open
        return is_open
    @app.callback(
        Output("guide-modal", "is_open"),
        [Input("open-guide-modal", "n_clicks"), Input("close-guide-modal", "n_clicks")],
        [State("guide-modal", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open


    # Page routing
    @app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")]
    )
    def display_page(pathname):
        if pathname == "/esa/sentinel/olci":
            return olci_layout()
        elif pathname == "/nasa/ghrsst/mur":
            return ghrsst_mur_layout()
        elif pathname == "/esa/globcolor/reflectance":
            return reflectance_layout()
        elif pathname == "/esa/globcolor/plankton":
            return plankton_layout()
        elif pathname == "/esa/globcolor/transp":
            return transp_layout()
        elif pathname == "/esa/globcolor/optics":
            return optics_layout()
        elif pathname == "/esa/globcolor/pp":
            return pp_layout()
        elif pathname == "/ukmo/ostia":
            return ostia_layout()
        elif pathname == "/nasa/modis/poc":
            return poc_layout()
        elif pathname == "/nasa/modis/par":
            return par_layout()
        elif pathname == "/nasa/modis/pic":
            return pic_layout()
        elif pathname == "/moi/model/pisces/bio":
            return mod_bio_layout()
        elif pathname == "/moi/model/pisces/nut":
            return mod_nut_layout()
        elif pathname == "/moi/model/pisces/car":
            return mod_car_layout()
        elif pathname == "/moi/model/seapodym/biomass":
            return mod_biomass_layout()
        elif pathname == "/moi/model/pisces/co2":
            return mod_co2_layout()
        elif pathname == "/moi/model/pisces/optics":
            return mod_optics_layout()
        elif pathname == "/moi/model/pisces/pfts":
            return mod_pfts_layout()
        elif pathname == "/moi/model/nemo/salinity":
            return mod_sal_layout()      
        return home_layout()
    
    @app.callback(
        [Output('point-selector', 'style'),
        Output('polygon-selector', 'style')],
        [Input('aoi-selector', 'value')]
    )
    def update_aoi_input(aoi_type):
        if aoi_type == 'point':
            return {'display': 'block'}, {'display': 'none'}
        elif aoi_type == 'polygon':
            return {'display': 'none'}, {'display': 'block'}
        return {'display': 'none'}, {'display': 'none'}
    
    @app.callback(
        [Output("start-date-picker", "date"),
        Output("end-date-picker", "date")],
        [Input("aoi-selector", "value"),
        Input("coordinate-input-point", "value"),
        Input("coordinate-input-polygon", "value"),
        Input("variable-selector", "value"),
        Input("dataset-type", "value")]
    )
    def update_date_pickers(aoi_type, point_coordinate, polygon_coordinate, variable, dataset_type):
        # Determine the coordinate based on AOI type
        coordinate = point_coordinate if aoi_type == 'point' else polygon_coordinate

        # Fetch data from S3 and process it
        try:
            df, _ = fetch_data_from_s3(s3_client, 'wamsi-westport-project-1-1', dataset_type, aoi_type, coordinate, variable)
            if df is None:
                return None, None
        except Exception as e:
            print(f"Error fetching data from S3: {e}")
            return None, None

        # Extract start and end dates
        start_date = df['time'].min()
        end_date = df['time'].max()

        return start_date, end_date
    @app.callback(
        Output("output-plot", "figure"),
        [Input("plot-button", "n_clicks")],
        [State("coordinate-input-point", "value"),
        State("coordinate-input-polygon", "value"),
        State("variable-selector", "value"),
        State("start-date-picker", "date"),
        State("end-date-picker", "date"),
        State("aoi-selector", "value"),
        State("dataset-type", "value")]
    )

    def update_plot(n_clicks, point_coordinate, polygon_coordinate, variable, start_date, end_date, aoi_type, dataset_type):
        if n_clicks is None:
            return {}

        # Determine the coordinate based on AOI type
        coordinate = point_coordinate if aoi_type == 'point' else polygon_coordinate

        # Fetch data from S3 and process it
        try:
            df, title = fetch_data_from_s3(s3_client, 'wamsi-westport-project-1-1', dataset_type, aoi_type, coordinate, variable)
            if df is None or title is None:
                return {}
        except Exception as e:
            print(f"Error fetching data from S3: {e}")
            return {}

        # Convert 'time' column to datetime if it exists
        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'])

        # Filter data by date range
        if start_date and end_date:
            df = df[(df['time'] >= start_date) & (df['time'] <= end_date)]

    # Retrieve the correct label for the variable based on dataset_type
        if variable == 'analysed_sst':
            # Check dataset type (celsius or kelvin)
            if dataset_type == 'mur':
                variable_label = variable_info['analysed_sst']['label']['celsius']
            elif dataset_type == 'ostia':
                variable_label = variable_info['analysed_sst']['label']['kelvin']
            else:
                variable_label = variable.capitalize()  # Fallback if dataset_type is unknown
            # Since the data column remains 'analysed_sst' for both cases
            variable_value = 'analysed_sst'
        else:
            # For other variables, retrieve the label normally
            variable_info_entry = variable_info.get(variable, {})
            variable_label = variable_info_entry.get('label', variable.capitalize())
            variable_value = variable_info_entry.get('value', variable)

        # Create the line chart
        fig = px.line(df, x='time', y=variable_value, title=title)

        # Update the layout to set the font, axis labels, and formatting
        fig.update_layout(
            font=dict(
                family="Times New Roman",
                size=18,  # Adjust font size as needed
                color="Black"  # Adjust color as needed
            ),
            title=dict(
                font=dict(size=24, color="#2c3e50"),  # Customize title font and color
                x=0.5,  # Center the title
                xanchor='center',
                yanchor='top'
            ),
            xaxis_title="Time",  # Customize X-axis label
            yaxis_title=variable_label,  # Y-axis label from `variable_info`
            xaxis=dict(showgrid=False),  # Hide gridlines for cleaner look
            yaxis=dict(showgrid=True, gridcolor='#dddddd'),  # Lighter gridlines for Y-axis
            template="plotly_white",  # Apply a cleaner, modern template
            plot_bgcolor='#fafafa',  # Light background color
            hovermode="x unified",  # Unified hover tooltip for a cleaner display
            margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins for better spacing
        )

        # Add hover text format (optional, for extra info on hover)
        fig.update_traces(hovertemplate='%{x}: %{y:.2f}')

        return fig

    
     # Highlight point/polygon on the map when plot button is clicked
    @app.callback(
        Output("highlight-data", "data"),
        [Input("plot-button", "n_clicks")],
        [State("coordinate-input-point", "value"),
         State("coordinate-input-polygon", "value"),
         State("aoi-selector", "value")]
    )
    def highlight_feature(n_clicks, point, polygon, aoi_type):
        if n_clicks is None:
            return {}
        if aoi_type == 'polygon':
            # Get the GeoJSON data of the selected polygon
            polygon_key = polygon_key_mapping.get(polygon)
            geojson = geojson_data.get(polygon_key)
            if geojson:
                return {'type': 'polygon', 'geojson': geojson}
        elif aoi_type == 'point':
            # Highlight the selected point
            lat = points_df.loc[int(point) - 1, 'latitude']
            lon = points_df.loc[int(point) - 1, 'longitude']
            return {'type': 'point', 'lat': lat, 'lon': lon}
        return {}

    # Update the map to highlight the selected point or polygon
    @app.callback(
    [Output("points-layer", "children"), Output("highlighted-layer", "children")],
    [Input("highlight-data", "data"),
     Input("dataset-type", "value")]  # Add dataset-type input
)
    def update_map_highlight(data, dataset_type):
        # Set point limit based on dataset_type
        if dataset_type in ['olci', 'mur']:
            point_limit = 32
        else:
            point_limit = 13

        # Create points layer with point limit
        points_layer = create_points_layer(point_limit)

        # Initialize highlighted layer
        highlighted_layer = []

        if data:
            if data['type'] == 'point':
                # Highlight the point
                highlighted_layer.append(dl.Marker(
                    position=[data['lat'], data['lon']],
                    id="highlighted-point",
                    children=dl.Tooltip("Selected Point"),
                    icon={
                        "iconUrl": "/assets/location-pin.png",  # Path to the custom icon
                        "iconSize": [40, 41],  # Size of the icon
                        "iconAnchor": [20, 41],  # Anchor point of the icon
                        "popupAnchor": [1, -34],  # Popup anchor point
                        "tooltipAnchor": [0, -28]  # Tooltip anchor point
                    }
                ))
            elif data['type'] == 'polygon':
                # Highlight the polygon using GeoJSON
                highlighted_layer.append(dl.GeoJSON(
                    data=data['geojson'],
                    id="highlighted-polygon",
                    options=dict(style=dict(color="red", weight=5, fillOpacity=0.1))
                ))

        # Return updated points and highlighted layers
        return points_layer, highlighted_layer
