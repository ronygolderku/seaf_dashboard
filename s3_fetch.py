import pandas as pd
import os
import boto3
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables
load_dotenv()

# Initialize S3 client
session = boto3.Session()
s3_client = session.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    endpoint_url=os.getenv('AWS_S3_ENDPOINT'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)

# Function to bind data from two S3 keys (for datasets that require it)
def bind_s3_data(s3_client, bucket, s3_key1, s3_key2):
    """Fetch and bind two datasets from S3."""
    try:
        # Fetch data from S3 key 1
        response1 = s3_client.get_object(Bucket=bucket, Key=s3_key1)
        data1 = response1['Body'].read()
        df1 = pd.read_csv(BytesIO(data1))

        # Fetch data from S3 key 2
        response2 = s3_client.get_object(Bucket=bucket, Key=s3_key2)
        data2 = response2['Body'].read()
        df2 = pd.read_csv(BytesIO(data2))

        # Convert 'time' column to datetime format
        df1['time'] = pd.to_datetime(df1['time'])
        df2['time'] = pd.to_datetime(df2['time'])

        # Reset the index to avoid issues with index alignment
        df1 = df1.reset_index(drop=True)
        df2 = df2.reset_index(drop=True)

        # Concatenate the two dataframes row-wise (axis=0)
        merged_df = pd.concat([df1, df2], axis=0, ignore_index=True)

        # Sort by time column
        merged_df = merged_df.sort_values(by='time')

        # Remove any duplicate entries (optional, but useful if there's overlap)
        merged_df = merged_df.drop_duplicates(subset=['time'])

        return merged_df
    except Exception as e:
        print(f"Error binding data from S3: {e}")
        return None

def fetch_data_from_s3(s3_client, bucket, dataset_type, aoi_type, coordinate, variable):
    """Fetch data from a single S3 key or bind datasets when necessary."""
    s3_key = None
    title = None

    # Handle datasets that require data binding (e.g., mur)
    if dataset_type == "mur":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key1 = f'csiem-data/data-lake/NASA/GHRSST/Points/ghrsst_sst_point_{coordinate}.csv'
                s3_key2 = f'csiem-data/data-lake/NASA/GHRSST/Points/2002-2023/GHRSST_sst_point_{coordinate}.csv'

                # Use the binding function to combine data
                df = bind_s3_data(s3_client, bucket, s3_key1, s3_key2)
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
                return df, title
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key1 = f'csiem-data/data-lake/NASA/GHRSST/Polygon_offshore/ghrsst_sst_polygon_{coordinate}.csv'
                s3_key2 = f'csiem-data/data-lake/NASA/GHRSST/Polygon_offshore/2002-2023/ghrsst_offshore_sst_polygon_{coordinate}.csv'

                # Use the binding function to combine data
                df = bind_s3_data(s3_client, bucket, s3_key1, s3_key2)
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
                return df, title
    elif dataset_type == "poc":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key1 = f'csiem-data/data-lake/NASA/MODIS/POC/Points/MODIS_POC_point_{coordinate}.csv'
                s3_key2 = f'csiem-data/data-lake/NASA/MODIS/POC/Points/2003-2022/Aq-MODIS_POC_point_{coordinate}.csv'

                # Use the binding function to combine data
                df = bind_s3_data(s3_client, bucket, s3_key1, s3_key2)
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
                return df, title
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key1 = f'csiem-data/data-lake/NASA/MODIS/POC/Polygon/MODIS_POC_polygon_{coordinate}.csv'
                s3_key2 = f'csiem-data/data-lake/NASA/MODIS/POC/Polygon/2003-2022/MODIS_POC_polygon_{coordinate}.csv'

                # Use the binding function to combine data
                df = bind_s3_data(s3_client, bucket, s3_key1, s3_key2)
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
                return df, title
            
    elif dataset_type == "pic":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key1 = f'csiem-data/data-lake/NASA/MODIS/PIC/Points/MODIS_PIC_point_{coordinate}.csv'
                s3_key2 = f'csiem-data/data-lake/NASA/MODIS/PIC/Points/2003-2022/Aq-MODIS_PIC_point_{coordinate}.csv'

                # Use the binding function to combine data
                df = bind_s3_data(s3_client, bucket, s3_key1, s3_key2)
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
                return df, title
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key1 = f'csiem-data/data-lake/NASA/MODIS/PIC/Polygon/MODIS_PIC_polygon_{coordinate}.csv'
                s3_key2 = f'csiem-data/data-lake/NASA/MODIS/PIC/Polygon/2003-2022/MODIS_PIC_polygon_{coordinate}.csv'

                # Use the binding function to combine data
                df = bind_s3_data(s3_client, bucket, s3_key1, s3_key2)
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
                return df, title
    elif dataset_type == "par":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key1 = f'csiem-data/data-lake/NASA/MODIS/PAR/Points/MODIS_PAR_point_{coordinate}.csv'
                s3_key2 = f'csiem-data/data-lake/NASA/MODIS/PAR/Points/2003-2022/Aq-MODIS_PAR_point_{coordinate}.csv'

                # Use the binding function to combine data
                df = bind_s3_data(s3_client, bucket, s3_key1, s3_key2)
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
                return df, title
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key1 = f'csiem-data/data-lake/NASA/MODIS/PAR/Polygon/MODIS_PAR_polygon_{coordinate}.csv'
                s3_key2 = f'csiem-data/data-lake/NASA/MODIS/PAR/Polygon/2003-2022/MODIS_PAR_polygon_{coordinate}.csv'

                # Use the binding function to combine data
                df = bind_s3_data(s3_client, bucket, s3_key1, s3_key2)
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
                return df, title
    elif dataset_type == "ostia":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key1 = f'csiem-data/data-lake/UKMO/OSTIA/Temperature/Points/CMEMS_SST_point_{coordinate}.csv'
                s3_key2 = f'csiem-data/data-lake/UKMO/OSTIA/Temperature/Points/1981-2006/SST_19811001_20061231_point_{coordinate}.csv'

                # Use the binding function to combine data
                df = bind_s3_data(s3_client, bucket, s3_key1, s3_key2)
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
                return df, title
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key1 = f'csiem-data/data-lake/UKMO/OSTIA/Temperature/Polygon/CMEMS_SST_polygon_{coordinate}.csv'
                s3_key2 = f'csiem-data/data-lake/UKMO/OSTIA/Temperature/Polygon/1981-2006/CMEMS_SST_polygon_{coordinate}.csv'

                # Use the binding function to combine data
                df = bind_s3_data(s3_client, bucket, s3_key1, s3_key2)
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
                return df, title

    # Handle datasets that do not require binding
    elif dataset_type == "plankton":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/GlobColor/Plankton/Points/CMEMS_planktons_point_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/GlobColor/Plankton/Polygon/CMEMS_planktons_polygon_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
    if dataset_type == "olci":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/Sentinel/Points/CMEMS_OLCI_CHL_point_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/Sentinel/Polygon_offshore/CMEMS_OLCI_CHL_polygon_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
    elif dataset_type == "reflectance":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/GlobColor/Reflectance/Point/CMEMS_reflectance_point_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/GlobColor/Reflectance/Polygon/CMEMS_reflectance_polygon_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
    elif dataset_type == "transp":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/GlobColor/Transp/Point/CMEMS_transp_point_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/GlobColor/Transp/Polygon/CMEMS_transp_polygon_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
    elif dataset_type == "optics":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/GlobColor/Optics/Point/CMEMS_optics_point_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/GlobColor/Optics/Polygon/CMEMS_optics_polygon_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
    elif dataset_type == "pp":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/GlobColor/PP/Point/CMEMS_PP_point_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/GlobColor/PP/Polygon/CMEMS_PP_polygon_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
    ## update the code for here
    elif dataset_type == "mod_bio":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/PISCES/Model_bio/Points/CMEMS_bio_point_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/PISCES/Model_bio/Polygon/CMEMS_bio_polygon_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
    elif dataset_type == "mod_nut":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/PISCES/Model_Nut/Points/CMEMS_nut_point_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/PISCES/Model_Nut/Polygon/CMEMS_nut_polygon_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
    elif dataset_type == "mod_optics":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/PISCES/Model_optics/Points/CMEMS_optics_point_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/PISCES/Model_optics/Polygon/CMEMS_optics_polygon_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
    elif dataset_type == "mod_car":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/PISCES/Model_car/Points/CMEMS_car_point_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/PISCES/Model_car/Polygon/CMEMS_car_polygon_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
    elif dataset_type == "mod_co2":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/PISCES/Model_co2/Points/CMEMS_co2_point_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/PISCES/Model_co2/Polygon/CMEMS_co2_polygon_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
    elif dataset_type == "mod_pfts":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/PISCES/Model_pft/Points/CMEMS_pft_point_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/PISCES/Model_pft/Polygon/CMEMS_pft_polygon_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
    elif dataset_type == "mod_biomass":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/SEAPODYM/Model_PP_ZO/Points/CMEMS_npp_zooc_point_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/SEAPODYM/Model_PP_ZO/Polygon/CMEMS_npp_zooc_polygon_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
    elif dataset_type == "mod_sal":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/NEMO/Model_salinity/Points/CMEMS_Salt_point_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/MOI/NEMO/Model_salinity/Polygon/CMEMS_Salt_polygon_{coordinate}.csv'
                title = f'Timeseries Analysis of {variable} for the Polygon {coordinate}'
    
    if s3_key is None or title is None:
        return None, None

    response = s3_client.get_object(Bucket=bucket, Key=s3_key)
    data = response['Body'].read()
    df = pd.read_csv(BytesIO(data))
    return df, title