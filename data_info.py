from dash import html

def create_dataset_div(title, description, points, polygons, sp_resolution, tp_resolution, date_range, raw_data_link, contact_email):
    return html.Div([
        html.H3(title),
        html.Hr(),
        html.P(description),
        html.P("This dataset is visualized in two ways:"),
        html.Ul([
            html.Li([html.Code("points")]),
            html.Li([html.Code("polygons")])
        ]),
        html.P("Summary of the dataset:"),
        html.Ul([
            html.Li([f"Total of {polygons} ", html.Code("polygons")]),
            html.Li([f"Total of {points} ", html.Code("points")]),
            html.Li(f"Spatial resolution: {sp_resolution}"),
            html.Li(f"Temporal resolution: {tp_resolution}"),
            html.Li(f"Data spans from {date_range}"),
            html.Li(f"Data is updated on a weekly basis in this dashboard"),
            html.Li("Processed data is available in CSV format")
        ]),
        html.P([
            "If you are interested in the raw data, you can access it ",
            html.A("here", href=raw_data_link, target="_blank")
        ]),
        html.P([
            "If you need the processed data, kindly contact ",
            html.B("Brendan Busch"),
            " at ",
            html.A(contact_email, href=f"mailto:{contact_email}")
        ])
    ])

olci = create_dataset_div(
    title='Satellite OLCI Data',
    description="The Ocean and Land Colour Instrument (OLCI) data is sourced from the Copernicus Sentinel-3 satellite.",
    points=32,
    polygons=6,
    sp_resolution="300 m",
    tp_resolution="Daily",
    date_range="25/04/2016 to the present",
    raw_data_link="https://sentinel.esa.int/web/sentinel/missions/sentinel-3",
    contact_email="brendan.busch@uwa.edu.au"
)

mur = create_dataset_div(
    title='Satellite GHRSST - The Group for High Resolution Sea Surface Temperature',
    description="A Group for High Resolution Sea Surface Temperature (GHRSST) Level 4 Multiscale Ultrahigh Resolution (MUR) sea surface temperature product is sourced from NASA Advanced Microwave Scanning Radiometer-EOS (AMSR-E), the JAXA Advanced Microwave Scanning Radiometer 2 on GCOM-W1, the Moderate Resolution Imaging Spectroradiometers (MODIS) on the NASA Aqua and Terra platforms, the US Navy microwave WindSat radiometer, the Advanced Very High Resolution Radiometer (AVHRR) on several NOAA satellites, and in situ SST observations from the NOAA iQuam project.",
    points=32,
    polygons=6,
    sp_resolution="1 km",
    tp_resolution="Daily",
    date_range="01/06/2002 to the present",
    raw_data_link="https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1",
    contact_email="brendan.busch@uwa.edu.au"
)

plankton = create_dataset_div(
    title='Satellite Plankton Data',
    description="The Reflectance data is sourced from the Globcolour Copernicus merge product. This product is a merged product of the Globcolour project and the Copernicus Marine Environment Monitoring Service (CMEMS). This product is a combination of different satellite sensors including MERIS, MODIS, SeaWiFS, VIIRS, and Sentinel-3 OLCI.",
    points=13,
    polygons=6,
    sp_resolution="4 km",
    tp_resolution="Daily",
    date_range="04/09/1997 to the present",
    raw_data_link="https://data.marine.copernicus.eu/product/OCEANCOLOUR_GLO_BGC_L3_MY_009_103/description",
    contact_email="brendan.busch@uwa.edu.au"
)

reflectance = create_dataset_div(
    title='Satellite Reflectance Data',
    description="The Reflectance data is sourced from the Globcolour Copernicus merge product. This product is a merged product of the Globcolour project and the Copernicus Marine Environment Monitoring Service (CMEMS). This product is a combination of different satellite sensors including MERIS, MODIS, SeaWiFS, VIIRS, and Sentinel-3 OLCI.",
    points=13,
    polygons=6,
    sp_resolution="4 km",
    tp_resolution="Daily",
    date_range="04/09/1997 to the present",
    raw_data_link="https://data.marine.copernicus.eu/product/OCEANCOLOUR_GLO_BGC_L3_MY_009_103/description",
    contact_email="brendan.busch@uwa.edu.au"
)

transp = create_dataset_div(
    title='Satellite Transparence Data',
    description="The Transparence data is sourced from the Globcolour Copernicus merge product. This product is a merged product of the Globcolour project and the Copernicus Marine Environment Monitoring Service (CMEMS). This product is a combination of different satellite sensors including MERIS, MODIS, SeaWiFS, VIIRS, and Sentinel-3 OLCI.",
    points=13,
    polygons=6,
    sp_resolution="4 km",
    tp_resolution="Daily",
    date_range="04/09/1997 to the present",
    raw_data_link="https://data.marine.copernicus.eu/product/OCEANCOLOUR_GLO_BGC_L3_MY_009_103/description",
    contact_email="brendan.busch@uwa.edu.au"
)

optics = create_dataset_div(
    title='Satellite Optics Data',
    description="The Optics data is sourced from the Globcolour Copernicus merge product. This product is a merged product of the Globcolour project and the Copernicus Marine Environment Monitoring Service (CMEMS). This product is a combination of different satellite sensors including MERIS, MODIS, SeaWiFS, VIIRS, and Sentinel-3 OLCI.",
    points=13,
    polygons=6,
    sp_resolution="4 km",
    tp_resolution="Daily",
    date_range="04/09/1997 to the present",
    raw_data_link="https://data.marine.copernicus.eu/product/OCEANCOLOUR_GLO_BGC_L3_MY_009_103/description",
    contact_email="brendan.busch@uwa.edu.au"
)

pp = create_dataset_div(
    title='Satellite Primary Production Data',
    description="The Primary Production data is sourced from the Globcolour Copernicus merge product. This product is a merged product of the Globcolour project and the Copernicus Marine Environment Monitoring Service (CMEMS). This product is a combination of different satellite sensors including MERIS, MODIS, SeaWiFS, VIIRS, and Sentinel-3 OLCI.",
    points=13,
    polygons=6,
    sp_resolution="4 km",
    tp_resolution="Monthly",
    date_range="04/09/1997 to the present",
    raw_data_link="https://data.marine.copernicus.eu/product/OCEANCOLOUR_GLO_BGC_L4_MY_009_104/description",
    contact_email="brendan.busch@uwa.edu.au"
)

ostia = create_dataset_div(
    title='Satellite OSTIA Data',
    description="The Operational Sea Surface Temperature and Sea Ice Analysis (OSTIA) data is sourced from the UK Met Office.",
    points=13,
    polygons=6,
    sp_resolution="5 km",
    tp_resolution="Daily",
    date_range="01/10/1981 to the present",
    raw_data_link="https://resources.marine.copernicus.eu/?option=com_csw&view=details&product_id=SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_047",
    contact_email="brendan.busch@uwa.edu.au"
)

pic = create_dataset_div(
    title='Satellite PIC Data',
    description="The Particulate Inorganic Carbon (PIC) data is sourced from the MODIS satellite.",
    points=13,
    polygons=6,
    sp_resolution="4 km",
    tp_resolution="Monthly",
    date_range="16/01/2003 to the present",
    raw_data_link="https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMPICmday_R2022NRT.html",
    contact_email="brendan.busch@uwa.edu.au"
)

poc = create_dataset_div(
    title='Satellite POC Data',
    description="The Particulate Organic Carbon (POC) data is sourced from the MODIS satellite.",
    points=13,
    polygons=6,
    sp_resolution="4 km",
    tp_resolution="Monthly",
    date_range="16/01/2003 to the present",
    raw_data_link="https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMPOCmday_R2022NRT.html",
    contact_email="brendan.busch@uwa.edu.au"
)

par = create_dataset_div(
    title='Satellite PAR Data',
    description="The Photosynthetically Available Radiation (PAR) data is sourced from the MODIS satellite.",
    points=13,
    polygons=6,
    sp_resolution="4 km",
    tp_resolution="Monthly",
    date_range="16/01/2003 to the present",
    raw_data_link="https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMH1par0mday_R2022NRT.html",
    contact_email="brendan.busch@uwa.edu.au"
)

model_bio = create_dataset_div(
    title='Modelled Biogeochemical Data',
    description="The modelled biogeochemical data is produced at Mercator Ocean International (Toulouse, France). This dataset is displayed with a 1/4 degree horizontal resolution with regular longitude/latitude equirectangular projection. The biogeochemical model used is PISCES which is a model of intermediate complexity designed for global ocean applications and is part of the NEMO modelling platform.",
    points=13,
    polygons=6,
    sp_resolution="0.25 degrees",
    tp_resolution="Daily",
    date_range="01/11/21 to the present",
    raw_data_link="https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_BGC_001_028/download?dataset=cmems_mod_glo_bgc-bio_anfc_0.25deg_P1D-m_202311",
    contact_email="brendan.busch@uwa.edu.au"
)

model_nut = create_dataset_div(
    title='Modelled Nutrient Data',
    description="The modelled nutrient data is produced at Mercator Ocean International (Toulouse, France). This dataset is displayed with a 1/4 degree horizontal resolution with regular longitude/latitude equirectangular projection. The nutrient model used is PISCES which is a model of intermediate complexity designed for global ocean applications and is part of the NEMO modelling platform.",
    points=13,
    polygons=6,
    sp_resolution="0.25 degrees",
    tp_resolution="Daily",
    date_range="01/11/21 to the present",
    raw_data_link="https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_BGC_001_028/download?dataset=cmems_mod_glo_bgc-nut_anfc_0.25deg_P1D-m_202311",
    contact_email="brendan.busch@uwa.edu.au"
)

model_optics = create_dataset_div(
    title='Modelled Optics Data',
    description="The modelled optics data is produced at Mercator Ocean International (Toulouse, France). This dataset is displayed with a 1/4 degree horizontal resolution with regular longitude/latitude equirectangular projection. The optics model used is PISCES which is a model of intermediate complexity designed for global ocean applications and is part of the NEMO modelling platform.",
    points=13,
    polygons=6,
    sp_resolution="0.25 degrees",
    tp_resolution="Daily",
    date_range="01/11/21 to the present",
    raw_data_link="https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_BGC_001_028/download?dataset=cmems_mod_glo_bgc-optics_anfc_0.25deg_P1D-m_202311",
    contact_email="brendan.busch@uwa.edu.au"
)

model_car= create_dataset_div(
    title='Modelled Carbon Data',
    description="The modelled carbon data is produced at Mercator Ocean International (Toulouse, France). This dataset is displayed with a 1/4 degree horizontal resolution with regular longitude/latitude equirectangular projection. The carbon model used is PISCES which is a model of intermediate complexity designed for global ocean applications and is part of the NEMO modelling platform.",
    points=13,
    polygons=6,
    sp_resolution="0.25 degrees",
    tp_resolution="Daily",
    date_range="01/11/21 to the present",
    raw_data_link="https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_BGC_001_028/download?dataset=cmems_mod_glo_bgc-car_anfc_0.25deg_P1D-m_202311",
    contact_email="brendan.busch@uwa.edu.au"
)

model_co2 = create_dataset_div(
    title='Modelled CO2 Data',
    description="The modelled CO2 data is produced at Mercator Ocean International (Toulouse, France). This dataset is displayed with a 1/4 degree horizontal resolution with regular longitude/latitude equirectangular projection. The CO2 model used is PISCES which is a model of intermediate complexity designed for global ocean applications and is part of the NEMO modelling platform.",
    points=13,
    polygons=6,
    sp_resolution="0.25 degrees",
    tp_resolution="Daily",
    date_range="01/11/21 to the present",
    raw_data_link="https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_BGC_001_028/download?dataset=cmems_mod_glo_bgc-co2_anfc_0.25deg_P1D-m_202311",
    contact_email="brendan.busch@uwa.edu.au"
)

model_pfts= create_dataset_div(
    title='Modelled PFTs Data',
    description="The modelled PFTs data is produced at Mercator Ocean International (Toulouse, France). This dataset is displayed with a 1/4 degree horizontal resolution with regular longitude/latitude equirectangular projection. The PFTs model used is PISCES which is a model of intermediate complexity designed for global ocean applications and is part of the NEMO modelling platform.",
    points=13,
    polygons=6,
    sp_resolution="0.25 degrees",
    tp_resolution="Daily",
    date_range="01/11/21 to the present",
    raw_data_link="https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_BGC_001_028/download?dataset=cmems_mod_glo_bgc-pft_anfc_0.25deg_P1D-m_202311",
    contact_email="brendan.busch@uwa.edu.au"
)

model_biomass= create_dataset_div(
    title='Modelled Biomass Data',
    description="The modelled biomass data is produced at Mercator Ocean International (Toulouse, France). This dataset is displayed with a 1/4 degree horizontal resolution with regular longitude/latitude equirectangular projection. The biomass model used is SEAPODYM which is a model of intermediate complexity designed for global ocean applications and is part of the NEMO modelling platform.",
    points=13,
    polygons=6,
    sp_resolution="0.083 degrees",
    tp_resolution="Daily",
    date_range="01/01/1998 to 31/12/2022",
    raw_data_link="https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_BGC_001_033/download?dataset=cmems_mod_glo_bgc_my_0.083deg-lmtl_PT1D-i_202211",
    contact_email="brendan.busch@uwa.edu.au"
)
model_sal= create_dataset_div(
    title='Modelled Salinity Data',
    description="The modelled salinity data is produced at Mercator Ocean International (Toulouse, France). This dataset is displayed with a 1/4 degree horizontal resolution with regular longitude/latitude equirectangular projection. The salinity model used is NEMO which is a model of intermediate complexity designed for global ocean applications",
    points=13,
    polygons=6,
    sp_resolution="0.083 degrees",
    tp_resolution="6 hourly",
    date_range="01/11/21 to the present",
    raw_data_link="https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/download?dataset=cmems_mod_glo_phy-so_anfc_0.083deg_PT6H-i_202406",
    contact_email="brendan.busch@uwa.edu.au"
)