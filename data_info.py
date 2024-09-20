from dash import html
olci = html.Div([
    html.H3('Satellite OLCI Data'),
    html.Hr(),
    html.P("The Ocean and Land Colour Instrument (OLCI) data is sourced from the Copernicus Sentinel-3 satellite."),
    html.P("This dataset is visualized in two ways:"),
    html.Ul([
        html.Li([html.Code("points")]),
        html.Li([html.Code("polygons")])
    ]),
    html.P("Summary of the dataset:"),
    html.Ul([
        html.Li(["Total of six ", html.Code("polygons")]),
        html.Li(["Total of 32 ", html.Code("points")]),
        html.Li("Spatial resolution: 300 m"),
        html.Li("Data spans from 25/04/2016 to the present"),
        html.Li("Data is updated on a weekly basis"),
        html.Li("Processed data is available in CSV format")
    ]),
    html.P([
        "If you are interested in the raw data, you can access it ",
        html.A("here", href="https://sentinel.esa.int/web/sentinel/missions/sentinel-3"),
    ]),
    html.P([
        "If you need the processed data, kindly contact ",
        html.B("Brendan Busch"),
        " at ",
         html.A("brendan.busch@uwa.edu.au", href="mailto:brendan.busch@uwa.edu.au")
    ])
])

mur= html.Div([
        html.H3('Satellite GHRSST - The Group for High Resolution Sea Surface Temperature'),
    html.Hr(),
    html.P("A Group for High Resolution Sea Surface Temperature (GHRSST) Level 4 Multiscale Ultrahigh Resolution (MUR) sea surface temperature product is sourced from NASA Advanced Microwave Scanning Radiometer-EOS (AMSR-E), the JAXA Advanced Microwave Scanning Radiometer 2 on GCOM-W1, the Moderate Resolution Imaging Spectroradiometers (MODIS) on the NASA Aqua and Terra platforms, the US Navy microwave WindSat radiometer, the Advanced Very High Resolution Radiometer (AVHRR) on several NOAA satellites, and in situ SST observations from the NOAA iQuam project."),
    html.P("This dataset is visualized in two ways:"),
    html.Ul([
        html.Li([html.Code("points")]),
        html.Li([html.Code("polygons")])
    ]),
    html.P("Summary of the dataset:"),
    html.Ul([
        html.Li(["Total of six ", html.Code("polygons")]),
        html.Li(["Total of 32 ", html.Code("points")]),
        html.Li("Spatial resolution: 1 km"),
        html.Li("Data spans from 01/01/2024 to the present"),
        html.Li("Data is updated on a weekly basis"),
        html.Li("Processed data is available in CSV format")
    ]),
    html.P([
        "If you are interested in the raw data, you can access it ",
        html.A("here", href="https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1")
    ]),
    html.P([
        "If you need the processed data, kindly contact ",
        html.B("Brendan Busch"),
        " at ",
        html.A("brendan.busch@uwa.edu.au", href="mailto:brendan.busch@uwa.edu.au")
    ])
])
plankton= html.Div([
    html.H3('Satellite Plankton Data'),
    html.Hr(),
    html.P("The Plankton data is sourced from the MODIS satellite."),
    html.P("This dataset is visualized in two ways:"),
    html.Ul([
        html.Li([html.Code("points")]),
        html.Li([html.Code("polygons")])
    ]),
    html.P("Summary of the dataset:"),
    html.Ul([
        html.Li(["Total of six ", html.Code("polygons")]),
        html.Li(["Total of 13 ", html.Code("points")]),
        html.Li("Spatial resolution: 4 km"),
        html.Li("Data spans from 01/03/2022 to the present"),
        html.Li("Data is updated on a weekly basis"),
        html.Li("Processed data is available in CSV format")
    ]),
    html.P([
        "If you are interested in the raw data, you can access it ",
        html.A("here", href="https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMPICmday_R2022NRT.html")
    ]),
    html.P([
        "If you need the processed data, kindly contact ",
        html.B("Brendan Busch"),
        " at ",
        html.A("brendan.busch@uwa.edu.au", href="mailto:brendan.busch@uwa.edu.au")
    ])
])


reflectance=html.Div([
    html.H3('Satellite Reflectance Data'),
    html.Hr(),
    html.P("The Reflectance data is sourced from the Globcolour Copernicus merge product. This product is a merged product of the Globcolour project and the Copernicus Marine Environment Monitoring Service (CMEMS). This product is a combination of differnt satellite sensors including MERIS, MODIS, SeaWiFS, VIIRS, and Sentinel-3 OLCI. This dataset is visualized in two ways:"),
    html.Ul([
        html.Li([html.Code("points")]),
        html.Li([html.Code("polygons")])
    ]),
    html.P("Summary of the dataset:"),
    html.Ul([
        html.Li(["Total of six ", html.Code("polygons")]),
        html.Li(["Total of 13 ", html.Code("points")]),
        html.Li("Spatial resolution: 4km"),
        html.Li("Data spans from 04/09/1997 to the present"),
        html.Li("Data is updated on a daily basis"),
        html.Li("Processed data is available in CSV format")
    ]),

    html.P([
        "If you are interested in the raw data, you can access it ",
        html.A("here", href="https://data.marine.copernicus.eu/product/OCEANCOLOUR_GLO_BGC_L4_MY_009_104/description"),
    ]),
    html.P([
        "If you need the processed data, kindly contact ",
        html.B("Brendan Busch"),
        " at ",
        html.A("brendan.busch@uwa.edu.au", href="mailto:brendan.busch@uwa.edu.au")
    ])
])
               


transp=html.Div([
    html.H3('Satellite Transparence Data'),
    html.Hr(),
    html.P("The Transparence data is sourced from the Globcolour Copernicus merge product. This product is a merged product of the Globcolour project and the Copernicus Marine Environment Monitoring Service (CMEMS). This product is a combination of differnt satellite sensors including MERIS, MODIS, SeaWiFS, VIIRS, and Sentinel-3 OLCI. This dataset is visualized in two ways:"),
    html.Ul([
        html.Li([html.Code("points")]),
        html.Li([html.Code("polygons")])
    ]), 
    html.P("Summary of the dataset:"),
    html.Ul([
        html.Li(["Total of six ", html.Code("polygons")]),
        html.Li(["Total of 13 ", html.Code("points")]),
        html.Li("Spatial resolution: 4km"),
        html.Li("Data spans from 04/09/1997 to the present"),
        html.Li("Data is updated on a daily basis"),
        html.Li("Processed data is available in CSV format")
    ]),
    html.P([
        "If you are interested in the raw data, you can access it ",
        html.A("here", href="https://data.marine.copernicus.eu/product/OCEANCOLOUR_GLO_BGC_L4_MY_009_104/description"),
    ]),
    html.P([
        "If you need the processed data, kindly contact ",
        html.B("Brendan Busch"),
        " at ",
        html.A("brendan.busch@uwa.edu.au", href="mailto:brendan.busch@uwa.edu.au")
    ])
])
               
optics=html.Div([
    html.H3('Satellite Optics Data'),
    html.Hr(),
    html.P("The Optics data is sourced from the Globcolour Copernicus merge product. This product is a merged product of the Globcolour project and the Copernicus Marine Environment Monitoring Service (CMEMS). This product is a combination of differnt satellite sensors including MERIS, MODIS, SeaWiFS, VIIRS, and Sentinel-3 OLCI. This dataset is visualized in two ways:"),
    html.Ul([
        html.Li([html.Code("points")]),
        html.Li([html.Code("polygons")])
    ]),
    html.P("Summary of the dataset:"),
    html.Ul([
        html.Li(["Total of six ", html.Code("polygons")]),
        html.Li(["Total of 13 ", html.Code("points")]),
        html.Li("Spatial resolution: 4km"),
        html.Li("Data spans from 04/09/1997 to the present"),
        html.Li("Data is updated on a daily basis"),
        html.Li("Processed data is available in CSV format")
    ]),
    html.P([
        "If you are interested in the raw data, you can access it ",
        html.A("here", href="https://data.marine.copernicus.eu/product/OCEANCOLOUR_GLO_BGC_L4_MY_009_104/description"),
    ]),
    html.P([
        "If you need the processed data, kindly contact ",
        html.B("Brendan Busch"),
        " at ",
        html.A("brendan.busch@uwa.edu.au", href="mailto:brendan.busch@uwa.edu.au")
    ])
])
               
pp=html.Div([
    html.H3('Satellite Primary Production Data'),
    html.Hr(),
    html.P("The Primary Production data is sourced from the Globcolour Copernicus merge product. This product is a merged product of the Globcolour project and the Copernicus Marine Environment Monitoring Service (CMEMS). This product is a combination of differnt satellite sensors including MERIS, MODIS, SeaWiFS, VIIRS, and Sentinel-3 OLCI. This dataset is visualized in two ways:"),
    html.Ul([
        html.Li([html.Code("points")]),
        html.Li([html.Code("polygons")])
    ]),
    html.P("Summary of the dataset:"),
    html.Ul([
        html.Li(["Total of six ", html.Code("polygons")]),
        html.Li(["Total of 13 ", html.Code("points")]),
        html.Li("Spatial resolution: 4km"),
        html.Li("Data spans from 04/09/1997 to the present"),
        html.Li("Data is updated on a daily basis"),
        html.Li("Processed data is available in CSV format")
    ]),
    html.P([
        "If you are interested in the raw data, you can access it ",
        html.A("here", href="https://data.marine.copernicus.eu/product/OCEANCOLOUR_GLO_BGC_L4_MY_009_104/description"),
    ]),
    html.P([
        "If you need the processed data, kindly contact ",
        html.B("Brendan Busch"),
        " at ",
        html.A("brendan.busch@uwa.edu.au", href="mailto:brendan.busch@uwa.edu.au")
    ])
])
               
ostia = html.Div([
    html.H3('Satellite OSTIA Data'),
    html.Hr(),
    html.P("The Operational Sea Surface Temperature and Sea Ice Analysis (OSTIA) data is sourced from the UK Met Office."),
    html.P("This dataset is visualized in two ways:"),
    html.Ul([
        html.Li([html.Code("points")]),
        html.Li([html.Code("polygons")])
    ]),
    html.P("Summary of the dataset:"),
    html.Ul([
        html.Li(["Total of six ", html.Code("polygons")]),
        html.Li(["Total of 13 ", html.Code("points")]),
        html.Li("Spatial resolution: 5 km"),
        html.Li("Data spans from 01/01/2006 to the present"),
        html.Li("Data is updated on a daily basis"),
        html.Li("Processed data is available in CSV format")
    ]),
    html.P([
        "If you are interested in the raw data, you can access it ",
        html.A("here", href="https://resources.marine.copernicus.eu/?option=com_csw&view=details&product_id=SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_047"),
    ]),
    html.P([
        "If you need the processed data, kindly contact ",
        html.B("Brendan Busch"),
        " at ",
        html.A("brendan.busch@uwa.edu.au", href="mailto:brendan.busch@uwa.edu.au")
    ])
])

pic= html.Div([
        html.H3('Satellite PIC Data'),
    html.Hr(),
    html.P("The Particulate Inorganic Carbon (PIC) data is sourced from the MODIS satellite."),
    html.P("This dataset is visualized in two ways:"),
    html.Ul([
        html.Li([html.Code("points")]),
        html.Li([html.Code("polygons")])
    ]),
    html.P("Summary of the dataset:"),
    html.Ul([
        html.Li(["Total of six ", html.Code("polygons")]),
        html.Li(["Total of 13 ", html.Code("points")]),
        html.Li("Spatial resolution: 4 km"),
        html.Li("Data spans from 01/03/2022 to the present"),
        html.Li("Data is updated on a weekly basis"),
        html.Li("Processed data is available in CSV format")
    ]),
    html.P([
        "If you are interested in the raw data, you can access it ",
        html.A("here", href="https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMPICmday_R2022NRT.html")
    ]),
    html.P([
        "If you need the processed data, kindly contact ",
        html.B("Brendan Busch"),
        " at ",
        html.A("brendan.busch@uwa.edu.au", href="mailto:brendan.busch@uwa.edu.au")
    ])
])
poc= html.Div([
    html.H3('Satellite POC Data'),
    html.Hr(),
    html.P("The Particulate Organic Carbon (POC) data is sourced from the MODIS satellite."),
    html.P("This dataset is visualized in two ways:"),
    html.Ul([
        html.Li([html.Code("points")]),
        html.Li([html.Code("polygons")])
    ]),
    html.P("Summary of the dataset:"),
    html.Ul([
        html.Li(["Total of six ", html.Code("polygons")]),
        html.Li(["Total of 13 ", html.Code("points")]),
        html.Li("Spatial resolution: 4 km"),
        html.Li("Data spans from 01/03/2022 to the present"),
        html.Li("Data is updated on a weekly basis"),
        html.Li("Processed data is available in CSV format")
    ]),
    html.P([
        "If you are interested in the raw data, you can access it ",
        html.A("here", href="https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMPOCmday_R2022NRT.html")
    ]),
    html.P([
        "If you need the processed data, kindly contact ",
        html.B("Brendan Busch"),
        " at ",
        html.A("brendan.busch@uwa.edu.au", href="mailto:brendan.busch@uwa.edu.au")
    ])
])
par = html.Div([
    html.H3('Satellite PAR Data'),
    html.Hr(),
    html.P("The Photosynthetically Available Radiation (PAR) data is sourced from the MODIS satellite."),
    html.P("This dataset is visualized in two ways:"),
    html.Ul([
        html.Li([html.Code("points")]),
        html.Li([html.Code("polygons")])
    ]),
    html.P("Summary of the dataset:"),
    html.Ul([
        html.Li(["Total of six ", html.Code("polygons")]),
        html.Li(["Total of 13 ", html.Code("points")]),
        html.Li("Spatial resolution: 4 km"),
        html.Li("Data spans from 01/03/2022 to the present"),
        html.Li("Data is updated on a weekly basis"),
        html.Li("Processed data is available in CSV format")
    ]),
    html.P([
        "If you are interested in the raw data, you can access it ",
        html.A("here", href="https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMH1par0mday_R2022NRT.html")
    ]),
    html.P([
        "If you need the processed data, kindly contact ",
        html.B("Brendan Busch"),
        " at ",
        html.A("brendan.busch@uwa.edu.au", href="mailto:brendan.busch@uwa.edu.au")
    ])
])