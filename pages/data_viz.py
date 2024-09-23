from dash import dcc, html, Input, Output, State, callback
import geopandas as gpd
import pandas as pd
import os
import dash_leaflet as dl
from dash import dcc, html
from data_info import olci, mur, plankton, reflectance, transp, optics, pp, ostia, par, pic, poc

# Load shapefiles and CSV
points_df = pd.read_csv("C:/Users/admin/Downloads/WAMSI/points.csv")
shapefiles = [
    "assets/shapefile/Polygons_1_MultiPolygon.shp",
    "assets/shapefile/Polygons_2_MultiPolygon.shp",
    "assets/shapefile/Polygons_3_MultiPolygon.shp",
    "assets/shapefile/Polygons_4_MultiPolygon.shp",
    "assets/shapefile/Polygons_5_MultiPolygon.shp",
    "assets/shapefile/Polygons_6_MultiPolygon.shp"
]

# Convert shapefiles to GeoJSON
geojson_data = {}
for shapefile in shapefiles:
    try:
        gdf = gpd.read_file(shapefile)
        geojson_data[os.path.basename(shapefile)] = gdf.__geo_interface__
    except Exception as e:
        print(f"Error reading {shapefile}: {e}")

# Create point markers
def create_points_layer(selected_point=None):
    points_layer = []
    for idx, row in points_df.iterrows():
        color = "red" if selected_point and selected_point == idx + 1 else "blue"
        points_layer.append(
            dl.Marker(
                position=[row['latitude'], row['longitude']],
                children=dl.Tooltip(f"Point: {row['Points']}, Location: {row['label']}")),
        )
    return points_layer


chl_layer = dl.TileLayer(
    url="https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=OCEANCOLOUR_GLO_BGC_L3_MY_009_103/cmems_obs-oc_glo_bgc-plankton_my_l3-olci-4km_P1D_202207/CHL&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&style=cmap:jet,logScale",
    opacity=0.7, attribution="Copernicus Marine Service"
)

sst_layer = dl.WMSTileLayer(
        url="https://polarwatch.noaa.gov/erddap/wms/jplMURSST41/request",
        layers="jplMURSST41:analysed_sst",
        format="image/png",
        transparent=True,
        version="1.3.0",
        crs="EPSG4326",
        attribution="NOAA PolarWatch"
)
ostia_layer = dl.TileLayer(
    url="https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001/METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2/analysed_sst&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&style=cmap:jet", opacity=0.7, attribution="Copernicus Marine Service"
)

reflectance_layer = dl.TileLayer(
    url="https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=OCEANCOLOUR_GLO_BGC_L3_MY_009_103/cmems_obs-oc_glo_bgc-reflectance_my_l3-multi-4km_P1D_202311/RRS412&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&style=cmap:jet", opacity=0.7, attribution="Copernicus Marine Service")

# Create a generic layout function
def create_layout(title, map_id, variable_options, dataset_type, geojson_data, point_range, dataset_info, wmts_layer):
    return html.Div([
        html.H2(f'{title} Data Visualization', className="heading"),
        html.Hr(),

        # Create a two-column layout
        html.Div([
            # Left side: Leaflet map
            html.Div([
                dl.Map(
                    [
                        # Ocean Basemap
                        dl.TileLayer(
                            url="https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}",
                            id="ocean-basemap"
                        ),
                        dl.LayerGroup(id="points-layer"),
                        dl.ScaleControl(position="bottomleft"),
                        dl.FullScreenControl(),

                        dl.LayerGroup(id="highlighted-layer"),  # For highlighted polygons
                        dl.LayersControl(
                            [
                                dl.BaseLayer(
                                    dl.TileLayer(
                                        url="https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}"
                                    ), name="Ocean Basemap", checked=True
                                ),
                                dl.BaseLayer(
                                    dl.TileLayer(
                                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                                    ), name="OpenStreetMap"
                                ),
                                dl.Overlay(dl.LayerGroup(id="points-layer"), name="Points", checked=False),
                                dl.Overlay(
                                    dl.LayerGroup(
                                        [dl.GeoJSON(data=geojson_data[name], id=f"geojson-{name}") for name in geojson_data]
                                    ), name="Polygon", checked=False
                                ),
                                # Add WMTS Layer
                                dl.Overlay(
                                     wmts_layer, name="WMTS Layer", checked=True
                                ),
                            ], position="topright"
                        )
                    ],
                    style={'width': '100%', 'height': '680px'},
                    center=[-32.1, 115.4], zoom=9, id=map_id
                )
            ], className='left-panel'),  # CSS class for map responsiveness

            # Right side: content (variable selector, AOI selector, date picker, plot button)
            html.Div([
                dcc.Tabs([
                    dcc.Tab(label=title, children=[
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Label("Select Variable"),
                                    dcc.Dropdown(
                                        id="variable-selector",
                                        options=variable_options,
                                        className="input-dropdown"  # Add a specific class
                                    )
                                ], className="input-group"),

                                html.Div([
                                    html.Label("Select AOI Type"),
                                    dcc.Dropdown(
                                        id="aoi-selector",
                                        options=[
                                            {'label': 'Point', 'value': 'point'},
                                            {'label': 'Polygon', 'value': 'polygon'}
                                        ],
                                        className="input-dropdown"
                                    )
                                ], className="input-group"),

                                # Conditional Point/Polygon Selector
                                html.Div([
                                    html.Div([
                                        html.Label("Select Point"),
                                        dcc.Dropdown(
                                            id="coordinate-input-point",
                                            options=[{'label': f'Point {i}', 'value': str(i)} for i in range(1, point_range + 1)],
                                            className="input-dropdown"
                                        )
                                    ], id='point-selector', style={'display': 'none'}),

                                    html.Div([
                                        html.Label("Select Polygon"),
                                        dcc.Dropdown(
                                            id="coordinate-input-polygon",
                                            options=[{'label': f'Polygon {i}', 'value': str(i)} for i in range(1, 7)],
                                            className="input-dropdown"
                                        )
                                    ], id='polygon-selector', style={'display': 'none'})
                                ], className="input-group"),

                                # Date Range Pickers
                                html.Div([
                                    html.Div([
                                        html.Label("From"),
                                        dcc.DatePickerSingle(
                                            id="start-date-picker",
                                            placeholder="Start Date",
                                            className="DatePickerSingle"
                                        )
                                    ], className="input-group"),

                                    html.Div([
                                        html.Label("To"),
                                        dcc.DatePickerSingle(
                                            id="end-date-picker",
                                            placeholder="End Date",
                                            className="DatePickerSingle"
                                        )
                                    ], className="input-group"),
                                ], className="input-date-range"),

                                # Hidden Input for Dataset Type
                                dcc.Input(id="dataset-type", type="hidden", value=dataset_type),

                                # Plot Button
                                html.Button('Plot', id='plot-button', className="plot-btn"),

                                # Graph Output
                                dcc.Graph(id='output-plot', className="graph-output"),
                            ], className="controls-container")
                        ]),

                        # Hidden div to store map update trigger
                        dcc.Store(id="highlight-data")
                    ]),
                    dcc.Tab(label='About', children=[
                        html.Div([
                            # html.H3('Dataset Information'),
                            dataset_info
                        ], style={'padding': '20px'})
                    ])
                ], className="tabs-container"),
            ], className='right-panel')  # CSS class for content responsiveness
        ], className='main-content')  # Flex container for main content
    ], className='layout-wrapper')

# Now use the generic function to create specific layouts
def olci_layout():
    variable_options = [{'label': 'Chlorophyll-a [mg/m³]', 'value': 'CHL'}]
    return create_layout("Sentinel OLCI", "olci-map", variable_options, "olci", geojson_data, 33, olci, chl_layer)

def ghrsst_mur_layout():
    variable_options = [{'label': 'Sea Surface Temperature [°C]', 'value': 'analysed_sst'}]
    return create_layout("GHRSST MUR", "mur-map", variable_options, "mur", geojson_data, 33, mur, sst_layer)

def transp_layout():
    variable_options = [{'label': 'diffuse attenuation coefficient at 490 nm [m-¹]', 'value': 'KD490'},
                        {'label': 'Secchi disk depth [m]', 'value': 'ZSD'},
                        {'label': 'Suspended particulate matter [g/m³]', 'value': 'SPM'}
                        ]
    return create_layout("Globecolor Transparency", "transp-map", variable_options, "transp", geojson_data, 14, transp)

def plankton_layout():
    variable_options = [
        {'label': 'Chlorophyll-a [mg m⁻³]', 'value': 'CHL'},
        {'label': 'Diatoms [mg m⁻³]', 'value': 'DIATO'},
        {'label': 'Dinoflagellates [mg m⁻³]', 'value': 'DINO'},
        {'label': 'Green Algae [mg m⁻³]', 'value': 'GREEN'},
        {'label': 'Haptophytes [mg m⁻³]', 'value': 'HAPTO'},
        {'label': 'Microplankton [mg m⁻³]', 'value': 'MICRO'},
        {'label': 'Nanoplankton [mg m⁻³]', 'value': 'NANO'},
        {'label': 'Picoplankton [mg m⁻³]', 'value': 'PICO'},
        {'label': 'Prochlorococcus [mg m⁻³]', 'value': 'PROCHLO'},
        {'label': 'Prokaryotes [mg m⁻³]', 'value': 'PROKAR'},
    ]
    return create_layout("Globecolor Plankton", "plankton-map", variable_options, "plankton", geojson_data, 14, plankton)

def reflectance_layout():
    variable_options = [
        {'label': 'RS reflectance at 412nm [sr⁻¹]', 'value': 'RRS412'},
        {'label': 'RS reflectance at 443nm [sr⁻¹]', 'value': 'RRS443'},
        {'label': 'RS reflectance at 490nm [sr⁻¹]', 'value': 'RRS490'},
        {'label': 'RS reflectance at 555nm [sr⁻¹]', 'value': 'RRS510'},
        {'label': 'RS reflectance at 670nm [sr⁻¹]', 'value': 'RRS670'},
    ]
    return create_layout("Globecolor reflectance", "reflectance-map", variable_options, "reflectance", geojson_data, 14, reflectance, reflectance_layer)

def optics_layout():
    variable_options = [
        {'label': 'Backscattering coefficient [m⁻¹]', 'value': 'BBP'},
        {'label': 'Colored Dissolved Organic Matter [m⁻¹]', 'value': 'CDM'}
    ]
    return create_layout("Globecolor optics", "optics-map", variable_options, "optics", geojson_data, 14, optics)

def pp_layout():
    variable_options = [
        {'label': 'Primary Production [mg C m⁻² day⁻¹]', 'value': 'PP'}
    ]
    return create_layout("Globecolor PP", "pp-map", variable_options, "pp", geojson_data, 14, pp)

def ostia_layout():
    variable_options = [
        {'label': 'Sea Surface Temperature [°K]', 'value': 'analysed_sst'}
    ]
    return create_layout("UKMO OSTIA", "ostia-map", variable_options, "ostia", geojson_data, 14, ostia, ostia_layer)

def pic_layout():
    variable_options = [
        {'label': 'Particulate Inorganic Carbon [mg m⁻³]', 'value': 'pic'}
    ]
    return create_layout("NASA MODIS PIC", "pic-map", variable_options, "pic", geojson_data, 14, pic)

def poc_layout():
    variable_options = [
        {'label': 'Particulate Organic Carbon [mg m⁻³]', 'value': 'poc'}
    ]
    return create_layout("NASA MODIS POC", "poc-map", variable_options, "poc", geojson_data, 14, poc)

def par_layout():
    variable_options = [
        {'label': 'Photosynthetically Available Radiation [Einstein m⁻² d⁻¹]', 'value': 'par'}
    ]
    return create_layout("NASA MODIS PAR", "par-map", variable_options, "par", geojson_data, 14, par)
