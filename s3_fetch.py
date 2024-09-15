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

def fetch_data_from_s3(s3_client, bucket, dataset_type, aoi_type, coordinate, variable):
    s3_key = None
    title = None

    if dataset_type == "olci":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/Sentinel/Points/CMEMS_OLCI_CHL_point_{coordinate}.csv'
                title = f'{variable} Timeseries for Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/Sentinel/Polygon_offshore/CMEMS_OLCI_CHL_polygon_{coordinate}.csv'
                title = f'{variable} Timeseries for Polygon {coordinate}'
    elif dataset_type == "ghrsst":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/NASA/GHRSST/Points/ghrsst_sst_point_{coordinate}.csv'
                title = f'{variable} Timeseries for Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/NASA/GHRSST/Polygon_offshore/ghrsst_sst_polygon_{coordinate}.csv'
                title = f'{variable} Timeseries for Polygon {coordinate}'
    elif dataset_type == "plankton":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/GlobColor/Plankton/Points/CMEMS_planktons_point_{coordinate}.csv'
                title = f'{variable} Timeseries for Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/GlobColor/Plankton/Polygon/CMEMS_planktons_polygon_{coordinate}.csv'
                title = f'{variable} Timeseries for Polygon {coordinate}'
    elif dataset_type == "reflectance":
        if aoi_type == 'point':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/GlobColor/Reflectance/Point/CMEMS_reflectance_point_{coordinate}.csv'
                title = f'{variable} Timeseries for Point {coordinate}'
        elif aoi_type == 'polygon':
            if coordinate is not None:
                s3_key = f'csiem-data/data-lake/ESA/GlobColor/Reflectance/Polygon/CMEMS_reflectance_polygon_{coordinate}.csv'
                title = f'{variable} Timeseries for Polygon {coordinate}'    

    if s3_key is None or title is None:
        return None, None

    response = s3_client.get_object(Bucket=bucket, Key=s3_key)
    data = response['Body'].read()
    df = pd.read_csv(BytesIO(data))
    return df, title