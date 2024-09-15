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
from pages.data_viz import olci_layout, ghrsst_mur_layout, plankton_layout, reflectance_layout, create_points_layer, points_df, geojson_data
from s3_fetch import s3_client, fetch_data_from_s3

polygon_key_mapping = {str(i): f"Polygons_{i}_MultiPolygon.shp" for i in range(1, 7)}  # Ensure ".shp" extension


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

        # Create the line chart
        fig = px.line(df, x='time', y=variable, title=title)

        # Update the layout to set the font
        fig.update_layout(
            font=dict(
                family="Times New Roman",
                size=18,  # You can adjust the size as needed
                color="Black"  # You can adjust the color as needed
            ),
            template="simple_white"  # Change the template as needed
        )

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
        Input("highlight-data", "data")
    )
    def update_map_highlight(data):
        points_layer = create_points_layer()
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
        return points_layer, highlighted_layer