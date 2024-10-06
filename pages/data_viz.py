from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import geopandas as gpd
import pandas as pd
import fiona
import os
import dash_leaflet as dl
from dash import dcc, html
from data_info import olci, mur, plankton, reflectance, transp, optics, pp, ostia, par, pic, poc, model_bio, model_nut, model_car, model_co2, model_pfts, model_biomass, model_sal, model_optics

# Load shapefiles and CSV
points_df = pd.read_csv("assets/points.csv")
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
        with fiona.open(shapefile) as src:
            gdf = gpd.GeoDataFrame.from_features(src)
            geojson_data[os.path.basename(shapefile)] = gdf.__geo_interface__
    except Exception as e:
        print(f"Error reading {shapefile}: {e}")

# Create point markers
def create_points_layer(point_limit, selected_point=None):
    points_layer = []
    for idx, row in points_df.iterrows():
        if idx >= point_limit:
            break  # Stop when the point limit is reached
        color = "red" if selected_point and selected_point == idx + 1 else "blue"
        points_layer.append(
            dl.Marker(
                position=[row['latitude'], row['longitude']],
                children=dl.Tooltip(f"Point: {row['Points']}, Location: {row['label']}"),
            ),
        )
    return points_layer

# Create a generic layout function
def create_layout(title, map_id, variable_options, dataset_type, geojson_data, point_range, dataset_info, wmts_layers, layer_name):
    # set point limit: 32 for olci and ghrsst, 13 for others
    if dataset_type in ['olci', 'mur']:
        point_limit = 32
    else:
        point_limit = 13
    
    points_layer = dl.LayerGroup(create_points_layer(point_limit), id="points-layer")

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
                        # dl.LayerGroup(id="points-layer"),
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
                                dl.Overlay(points_layer, name="Points", checked=False),
                                # dl.Overlay(dl.LayerGroup(id="points-layer"), name="Points", checked=False),
                                dl.Overlay(
                                    dl.LayerGroup(
                                        [dl.GeoJSON(data=geojson_data[name], id=f"geojson-{name}") for name in geojson_data]
                                    ), name="Polygon", checked=False
                                ),
                                # Add WMTS Layer (single or multiple layers)
                                *wmts_layers # Unpack the list of layers
                            ], position="topright"
                        )
                    ],
                    style={'width': '100%', 'height': '100%'},
                    center=[-32.1, 115.4], zoom=9, id=map_id
                )
            ], className='left-panel'),  # CSS class for map responsiveness

            # Right side: content (variable selector, AOI selector, date picker, plot button)
            html.Div([
                dbc.Tabs([
                    dbc.Tab(
                        label=title,
                        tab_id="tab-1",
                        children=[
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Label("Select Variable"),
                                        dcc.Dropdown(
                                            id="variable-selector",
                                            options=variable_options,
                                            className="input-dropdown",
                                             style={'width': '300px'}
                                        )
                                    ], className="input-group", style={'flex': '1'}),
            
                                    html.Div([
                                        html.Label("Select AOI Type"),
                                        dcc.Dropdown(
                                            id="aoi-selector",
                                            options=[
                                                {'label': 'Point', 'value': 'point'},
                                                {'label': 'Polygon', 'value': 'polygon'}
                                            ],
                                            className="input-dropdown", style={'width': '270px'}
                                        )
                                    ], className="input-group", style={'flex': '1'}),
            
                                    # Conditional Point/Polygon Selector
                                    html.Div([
                                        html.Div([
                                            html.Label("Select Point"),
                                            dcc.Dropdown(
                                                id="coordinate-input-point",
                                                options=[{'label': f'Point {i}', 'value': str(i)} for i in range(1, point_range)],
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
                                    ], className="input-group", style={'flex': '1'}),
            
                                    # Date Range Pickers
                                    html.Div([
                                        html.Div([
                                            html.Label("From"),
                                            dcc.DatePickerSingle(
                                                id="start-date-picker",
                                                display_format="DD/MM/YYYY",
                                                placeholder="Start Date",
                                                className="DatePickerSingle"
                                            )
                                        ], className="input-group"),
            
                                        html.Div([
                                            html.Label("To"),
                                            dcc.DatePickerSingle(
                                                id="end-date-picker",
                                                display_format="DD/MM/YYYY",
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
                        ],
                    ),
                    dbc.Tab(
                        label='About',
                        tab_id="tab-2",
                        children=[
                            html.Div([
                                dataset_info
                            ], style={'padding': '20px'})
                        ],
                    )
                ], id="tabs", active_tab="tab-1", className="tabs-container"),
            ], className='right-panel')  # CSS class for content responsiveness
            ], className='main-content')  # Flex container for main content
            ], className='layout-wrapper')


# Now use the generic function to create specific layouts
def olci_layout():
    variable_options = [{'label': 'Chlorophyll-a [mg/m³]', 'value': 'CHL'}]

    chl_layer = [
        dl.Overlay(
            dl.TileLayer(
        url="https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=OCEANCOLOUR_GLO_BGC_L3_MY_009_103/cmems_obs-oc_glo_bgc-plankton_my_l3-olci-4km_P1D_202207/CHL&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&style=cmap:jet,logScale",
        opacity=0.7, attribution="Copernicus Marine Service"
    ), name="Chlorophyll-a", checked=False)
    ]

    return create_layout(
        title="Sentinel Chlorophyll-a",
        map_id="olci-map",
        variable_options=variable_options,
        dataset_type="olci",
        geojson_data=geojson_data,
        point_range=33,
        dataset_info=olci,
        wmts_layers=chl_layer,  # Single layer for CHL
        layer_name="Chlorophyll-a"  # Dynamic layer name
    )


def ghrsst_mur_layout():
    variable_options = [{'label': 'Sea Surface Temperature [°C]', 'value': 'analysed_sst'}]

    # WMSTileLayer for Sea Surface Temperature
    sst_layer = [
        dl.Overlay(
            dl.WMSTileLayer(
                url="https://polarwatch.noaa.gov/erddap/wms/jplMURSST41/request",
                layers="jplMURSST41:analysed_sst",
                format="image/png",
                transparent=True,
                version="1.3.0",
                crs="EPSG4326",
                attribution="NOAA PolarWatch"
            ),
            name="GHRSST SST",
            checked=False  # Set to False if you want the layer off by default
        )
    ]

    return create_layout(
        title="GHRSST SST",
        map_id="mur-map",
        variable_options=variable_options,
        dataset_type="mur",
        geojson_data=geojson_data,
        point_range=33,
        dataset_info=mur,
        wmts_layers=sst_layer,  # Single WMS layer for SST
        layer_name="Sea Surface Temperature"  # Dynamic layer name
    )


def transp_layout():
    variable_options = [
        {'label': 'diffuse attenuation coefficient at 490 nm [m⁻¹]', 'value': 'KD490'},
        {'label': 'Secchi disk depth [m]', 'value': 'ZSD'},
        {'label': 'Suspended particulate matter [g/m³]', 'value': 'SPM'}
    ]
    
    # Create WMTS layers for transparency variables with respective colormaps
    wmts_layers = [
        dl.Overlay(
            dl.TileLayer(
                url=f"https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=OCEANCOLOUR_GLO_BGC_L3_MY_009_103/cmems_obs-oc_glo_bgc-transp_my_l3-multi-4km_P1D_202311/{variable}&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}&style=cmap:{cmap}",
                opacity=0.7,
                attribution="Copernicus Marine Service"
            ),
            name=f"{variable}",  # Unique name for each layer
            checked=False  # Layers are unchecked by default
        ) for variable, cmap in zip(["KD490", "SPM", "ZSD"], ["dense", "dense", "viridis"])
    ]

    return create_layout(
        title="GlobColour Transparency",
        map_id="transp-map",
        variable_options=variable_options,
        dataset_type="transp",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=transp,
        wmts_layers=wmts_layers,  # Pass the generated wmts layers
        layer_name="Transparency Layers"  # Dynamic layer name
    )


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
    
    # Create WMTS layers for each plankton variable
    wmts_layers = [
        dl.Overlay(
            dl.TileLayer(
                url=f"https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=OCEANCOLOUR_GLO_BGC_L3_MY_009_103/cmems_obs-oc_glo_bgc-plankton_my_l3-multi-4km_P1D_202311/{variable}&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}&style=cmap:algae",
                opacity=0.7,
                attribution="Copernicus Marine Service"
            ),
            name=f"{variable}",  # Unique name for each layer
            checked=False  # Layers are unchecked by default
        ) for variable in ['CHL', 'DIATO', 'DINO', 'GREEN', 'HAPTO', 'MICRO', 'NANO', 'PICO', 'PROCHLO', 'PROKAR']
    ]

    return create_layout(
        title="GlobColour Plankton",
        map_id="plankton-map",
        variable_options=variable_options,
        dataset_type="plankton",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=plankton,
        wmts_layers=wmts_layers,  # Pass the generated WMTS layers
        layer_name="Plankton Layers"  # Dynamic layer name
    )


def reflectance_layout():
    variable_options = [
        {'label': 'RS reflectance at 412nm [sr⁻¹]', 'value': 'RRS412'},
        {'label': 'RS reflectance at 443nm [sr⁻¹]', 'value': 'RRS443'},
        {'label': 'RS reflectance at 490nm [sr⁻¹]', 'value': 'RRS490'},
        {'label': 'RS reflectance at 555nm [sr⁻¹]', 'value': 'RRS555'},
        {'label': 'RS reflectance at 670nm [sr⁻¹]', 'value': 'RRS670'},
    ]

    # Create WMTS layers for each reflectance band
    wmts_layers = [
        dl.Overlay(
            dl.TileLayer(
                url=f"https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=OCEANCOLOUR_GLO_BGC_L3_MY_009_103/cmems_obs-oc_glo_bgc-reflectance_my_l3-multi-4km_P1D_202311/{variable}&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}&style=cmap:jet",
                opacity=0.7,
                attribution="Copernicus Marine Service"
            ),
            name=f"{variable}",  # Unique name for each layer
            checked=False  # Layers are unchecked by default
        ) for variable in ['RRS412', 'RRS443', 'RRS490', 'RRS555', 'RRS670']
    ]

    return create_layout(
        title="GlobColour Reflectance",
        map_id="reflectance-map",
        variable_options=variable_options,
        dataset_type="reflectance",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=reflectance,
        wmts_layers=wmts_layers,  # Multiple layers for reflectance
        layer_name="Reflectance Layers"  # Dynamic layer name
    )



def optics_layout():
    variable_options = [
        {'label': 'Backscattering coefficient [m⁻¹]', 'value': 'BBP'},
        {'label': 'Colored Dissolved Organic Matter [m⁻¹]', 'value': 'CDM'}
    ]

    # Create WMTS layers for optics variables with respective colormaps
    wmts_layers = [
        dl.Overlay(
            dl.TileLayer(
                url=f"https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=OCEANCOLOUR_GLO_BGC_L3_MY_009_103/cmems_obs-oc_glo_bgc-optics_my_l3-multi-4km_P1D_202311/{variable}&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}&style=cmap:{cmap}",
                opacity=0.7,
                attribution="Copernicus Marine Service"
            ),
            name=f"{variable}",  # Unique name for each layer
            checked=False  # Layers are unchecked by default
        ) for variable, cmap in zip(['BBP', 'CDM'], ['solar', 'dense'])
    ]

    return create_layout(
        title="GlobColour Optics",
        map_id="optics-map",
        variable_options=variable_options,
        dataset_type="optics",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=optics,
        wmts_layers=wmts_layers,  # Pass the generated wmts layers
        layer_name="Optics Layers"  # Dynamic layer name
    )


def pp_layout():
    variable_options = [
        {'label': 'Primary Production [mg C m⁻² day⁻¹]', 'value': 'PP'}
    ]

    # WMTS layer for Primary Production
    wmts_layers = [
        dl.Overlay(
            dl.TileLayer(
                url="https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=OCEANCOLOUR_GLO_BGC_L4_NRT_009_102/cmems_obs-oc_glo_bgc-pp_nrt_l4-multi-4km_P1M_202311/PP&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&style=cmap:matter",
                opacity=0.7,
                attribution="Copernicus Marine Service"
            ),
            name="Primary Production",  # Unique name for the layer
            checked=False  # Set to False if you want the layer off by default
        )
    ]

    return create_layout(
        title="GlobColour Primary Productivity",
        map_id="pp-map",
        variable_options=variable_options,
        dataset_type="pp",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=pp,
        wmts_layers=wmts_layers,  # Single layer for Primary Production
        layer_name="Primary Production Layer"  # Dynamic layer name
    )


def ostia_layout():
    variable_options = [{'label': 'Sea Surface Temperature [°K]', 'value': 'analysed_sst'}]

    ostia_layer = [
        dl.Overlay(
            dl.TileLayer(
                url="https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001/METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2/analysed_sst&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&style=cmap:jet",
                opacity=0.7,
                attribution="Copernicus Marine Service"
            ),
            name="UKMO SST",
            checked=False  # Set to False if you want the layer off by default
        )
    ]

    return create_layout(
        title="UKMO SST",
        map_id="ostia-map",
        variable_options=variable_options,
        dataset_type="ostia",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=ostia,
        wmts_layers=ostia_layer,  # Single layer for SST
        layer_name="Sea Surface Temperature"  # Dynamic layer name
    )


def poc_layout():
    variable_options = [
        {'label': 'Particulate Organic Carbon [mg m⁻³]', 'value': 'poc'}
    ]

    # WMTS layer for Particulate Organic Carbon (POC)
    poc_layer = [
        dl.Overlay(
            dl.WMSTileLayer(
                url="https://coastwatch.pfeg.noaa.gov/erddap/wms/erdMPOCmday_R2022NRT/request",
                layers="erdMPOCmday_R2022NRT:poc",
                format="image/png",
                transparent=True,
                version="1.3.0",
                crs="EPSG4326",
                attribution="NOAA PolarWatch"
            ),
            name="MODIS POC",  # Name for the layer
            checked=False  # Set to False if you want the layer off by default
        )
    ]

    return create_layout(
        title="MODIS POC",
        map_id="poc-map",
        variable_options=variable_options,
        dataset_type="poc",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=poc,
        wmts_layers=poc_layer,  # Single layer for POC
        layer_name="Particulate Organic Carbon Layer"  # Dynamic layer name
    )


def par_layout():
    variable_options = [
        {'label': 'Photosynthetically Available Radiation [Einstein m⁻² d⁻¹]', 'value': 'par'}
    ]

    # WMSTileLayer for Photosynthetically Available Radiation (PAR)
    par_layer = [
        dl.Overlay(
            dl.WMSTileLayer(
                url="https://coastwatch.pfeg.noaa.gov/erddap/wms/erdMH1par0mday_R2022NRT/request",
                layers="erdMH1par0mday_R2022NRT:par",
                format="image/png",
                transparent=True,
                version="1.3.0",
                crs="EPSG4326",
                attribution="NOAA PolarWatch"
            ),
            name="MODIS PAR",  # Name for the PAR layer
            checked=False  # Set to False if you want the layer off by default
        )
    ]

    return create_layout(
        title="MODIS PAR",
        map_id="par-map",
        variable_options=variable_options,
        dataset_type="par",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=par,
        wmts_layers=par_layer,  # Single layer for PAR
        layer_name="Photosynthetically Available Radiation Layer"  # Dynamic layer name
    )
def pic_layout():
    variable_options = [
        {'label': 'Particulate Inorganic Carbon [mg m⁻³]', 'value': 'pic'}
    ]

    # WMSTileLayer for Particulate Inorganic Carbon (PIC)
    pic_layer = [
        dl.Overlay(
            dl.WMSTileLayer(
                url="https://coastwatch.pfeg.noaa.gov/erddap/wms/erdMPICmday_R2022NRT/request",
                layers="erdMPICmday_R2022NRT:pic",
                format="image/png",
                transparent=True,
                version="1.3.0",
                crs="EPSG4326",
                attribution="NOAA PolarWatch"
            ),
            name="MODIS PIC",  # Name for the PIC layer
            checked=False  # Set to False if you want the layer off by default
        )
    ]

    return create_layout(
        title="MODIS PIC",
        map_id="pic-map",
        variable_options=variable_options,
        dataset_type="pic",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=pic,
        wmts_layers=pic_layer,  # Single layer for PIC
        layer_name="Particulate Inorganic Carbon Layer"  # Dynamic layer name
    )

def mod_bio_layout():
    variable_options = [
        {'label': 'Total Primary Production of Phyto [mg m⁻³ d⁻¹]', 'value': 'nppv'},
        {'label': 'Dissolved Oxygen [mmol m⁻³]', 'value': 'o2'},
 
    ]

# Create WMTS layers for transparency variables with respective colormaps
    wmts_layers = [
        dl.Overlay(
            dl.TileLayer(
                url=f"https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=GLOBAL_ANALYSISFORECAST_BGC_001_028/cmems_mod_glo_bgc-bio_anfc_0.25deg_P1D-m_202311/{variable}&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}&style=cmap:matter",
                opacity=0.7,
                attribution="Copernicus Marine Service"
            ),
            name=f"{variable}",  # Unique name for each layer
            checked=False  # Layers are unchecked by default
        ) for variable in ["nppv", "o2"] 
    ]


    return create_layout(
        title="Model Biogeochemistry",
        map_id="mod-bio-map",
        variable_options=variable_options,
        dataset_type="mod_bio",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=model_bio,
        wmts_layers=wmts_layers,
        layer_name="Model Biogeochemistry")

def mod_nut_layout():
    variable_options = [
        {'label': 'Nitrate [mmol m⁻³]', 'value': 'no3'},
        {'label': 'Phosphate [mmol m⁻³]', 'value': 'po4'},
        {'label': 'Dissolved Silicate [mmol m⁻³]', 'value': 'si'},
        {'label': 'Dissolved Iron [mmol m⁻³]', 'value': 'fe'}
    ]

    # Create WMTS layers for nutrient variables with respective colormaps
    wmts_layers = [
        dl.Overlay(
            dl.TileLayer(
                url=f"https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=GLOBAL_ANALYSISFORECAST_BGC_001_028/cmems_mod_glo_bgc-nut_anfc_0.25deg_P1D-m_202311/{variable}&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}&style=cmap:{cmap}",
                opacity=0.7,
                attribution="Copernicus Marine Service"
            ),
            name=f"{variable}",  # Unique name for each layer
            checked=False  # Layers are unchecked by default
        ) for variable, cmap in zip(["no3", "po4", "si", "fe"], ["matter", "dense", "dense", "dense"])
    ]

    return create_layout(
        title="Model Nutrients",
        map_id="mod-nut-map",
        variable_options=variable_options,
        dataset_type="mod_nut",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=model_nut,  # Ensure this is the correct dataset info
        wmts_layers=wmts_layers,
        layer_name="Model Nutrient Layers"
    )

def mod_car_layout():
    variable_options = [
        {'label': 'Total Alkalinity [mol m⁻³]', 'value': 'talk'},
        {'label': 'Dissolved Inorganic Carbon [mol m⁻³]', 'value': 'dissic'},
        {'label': 'pH', 'value': 'ph'},
    ]

    # Create WMTS layers for carbonate variables with respective colormaps
    wmts_layers = [
        dl.Overlay(
            dl.TileLayer(
                url=f"https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=GLOBAL_ANALYSISFORECAST_BGC_001_028/cmems_mod_glo_bgc-car_anfc_0.25deg_P1D-m_202311/{variable}&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}&style=cmap:{cmap}",
                opacity=0.7,
                attribution="Copernicus Marine Service"
            ),
            name=f"{variable}",  # Unique name for each layer
            checked=False  # Layers are unchecked by default
        ) for variable, cmap in zip(["talk", "dissic", "ph"], ["matter", "dense", "viridis"])
    ]

    return create_layout(
        title="Model Carbonate",
        map_id="mod-car-map",
        variable_options=variable_options,
        dataset_type="mod_car",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=model_car,  # Ensure this is the correct dataset info
        wmts_layers=wmts_layers,
        layer_name="Model Carbonate Chemistry"
    )

def mod_co2_layout():
    variable_options = [
        {'label': 'Surface partial pressure of CO₂ [Pa]', 'value': 'spco2'},
    ]

    # Create WMTS layers for CO₂ variables with respective colormaps
    wmts_layers = [
        dl.Overlay(
            dl.TileLayer(
                url=f"https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=GLOBAL_ANALYSISFORECAST_BGC_001_028/cmems_mod_glo_bgc-co2_anfc_0.25deg_P1D-m_202311/spco2&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}&style=cmap:matter",
                opacity=0.7,
                attribution="Copernicus Marine Service"
            ),
            name="spco2",  # Unique name for each layer
            checked=False  # Layers are unchecked by default
        )
    ]

    return create_layout(
        title="Model CO₂",
        map_id="mod-co2-map",
        variable_options=variable_options,
        dataset_type="mod_co2",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=model_co2,  # Ensure this is the correct dataset info
        wmts_layers=wmts_layers,
        layer_name="Model CO₂ Layers"
    )
def mod_optics_layout():
    variable_options = [
        {'label': 'Volume attenuation coefficient [m⁻¹]', 'value': 'kd'},
    ]
    # Create WMTS layers for optics variables with respective colormaps
    wmts_layers = [
        dl.Overlay(
            dl.TileLayer(
                url=f"https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=GLOBAL_ANALYSISFORECAST_BGC_001_028/cmems_mod_glo_bgc-optics_anfc_0.25deg_P1D-m_202311/kd&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}&style=cmap:viridis",
                opacity=0.7,
                attribution="Copernicus Marine Service"
            ),
            name="kd",  # Unique name for each layer
            checked=False  # Layers are unchecked by default
        )
    ]

    return create_layout(
        title="Model Optics",
        map_id="mod-optics-map",
        variable_options=variable_options,
        dataset_type="mod_optics",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=model_optics,
        wmts_layers=wmts_layers,
        layer_name="Model Optics Layers"
    )

def mod_pfts_layout():
    variable_options = [
        {'label': 'chlorophyll-a [mg m⁻³]', 'value': 'chl'},
        {'label': 'Phytoplankton [mmol m⁻³]', 'value': 'phyc'},
    ]

    # Create WMTS layers for plankton functional types with respective colormaps
    wmts_layers = [
        dl.Overlay(
            dl.TileLayer(
                url=f"https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=GLOBAL_ANALYSISFORECAST_BGC_001_028/cmems_mod_glo_bgc-pft_anfc_0.25deg_P1D-m_202311/{variable}&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}&style=cmap:{camp}",
                opacity=0.7,
                attribution="Copernicus Marine Service"
            ),
            name=f"{variable}",  # Unique name for each layer
            checked=False  # Layers are unchecked by default
        ) for variable, camp in zip(["chl", "phyc"], ["algae", "matter"])
    ]

    return create_layout(
        title="Model PFTs",
        map_id="mod-pfts-map",
        variable_options=variable_options,
        dataset_type="mod_pfts",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=model_pfts,
        wmts_layers=wmts_layers,
        layer_name="Model PFTs Layers"
    )

def mod_sal_layout():
    variable_options = [
        {'label': 'Salinity [PSU]', 'value': 'so'},
    ]

    # Create WMTS layers for salinity with respective colormaps
    wmts_layers = [
        dl.Overlay(
            dl.TileLayer(
                url=f"https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=GLOBAL_ANALYSISFORECAST_PHY_001_024/cmems_mod_glo_phy-so_anfc_0.083deg_P1D-m_202406/so&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}&style=cmap:haline",
                opacity=0.7,
                attribution="Copernicus Marine Service"
            ),
            name="Salinity",  # Unique name for each layer
            checked=False  # Layers are unchecked by default
        )
    ]

    return create_layout(
        title="Model Salinity",
        map_id="mod-sal-map",
        variable_options=variable_options,
        dataset_type="mod_sal",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=model_sal,
        wmts_layers=wmts_layers,
        layer_name="Model Salinity Layers"
    )

def mod_biomass_layout():
    variable_options = [
        {'label': 'Zooplankton [g m²]', 'value': 'zooc'},
        {'label': 'Net primary productivity [mg m⁻² day⁻¹]', 'value': 'npp'},
    ]
    # Create WMTS layers for biomass variables with respective colormaps
    wmts_layers = [
        dl.Overlay(
            dl.TileLayer(
                url=f"https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=GLOBAL_MULTIYEAR_BGC_001_033/cmems_mod_glo_bgc_my_0.083deg-lmtl_PT1D-i_202211/{variable}&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}&style=cmap:{camp}",
                opacity=0.7,
                attribution="Copernicus Marine Service"
            ),
            name=f"{variable}",  # Unique name for each layer
            checked=False  # Layers are unchecked by default
        ) for variable, camp in zip(["zooc", "npp"], ["matter", "algae"])
    ]
    return create_layout(
        title="Model Biomass",
        map_id="mod-biomass-map",
        variable_options=variable_options,
        dataset_type="mod_biomass",
        geojson_data=geojson_data,
        point_range=14,
        dataset_info=model_biomass,
        wmts_layers=wmts_layers,
        layer_name="Model Biomass Layers"
    )
