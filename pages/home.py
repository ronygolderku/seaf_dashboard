from dash import dcc, html

def home_layout():
    return html.Div([
        html.H2("Make Virtual Sensor with Satellite Data in Cockburn Sound (CS)"),
        html.P("Cockburn Sound (CS) is monitored by numerous sensors providing continuous data on oceanic and atmospheric parameters. "
               "These data streams are accessible through various agencies such as BOM, DWER, WAMSI, and UWA. However, in situ data may "
               "not always be available for specific areas of interest, especially for assessing the environmental impacts of ongoing "
               "development activities like WESTPORT."),
        html.P("Deploying sensors in such locations is costly, involving expenses for purchase, deployment, and maintenance. "
               "To overcome these challenges, virtual sensors using satellite data can be a viable solution. Satellite data provide "
               "comprehensive and continuous coverage, enabling effective environmental monitoring where physical sensors cannot be installed."),
        html.H3("About this Repo"),
        html.P("This repository contains Python scripts designed to automate the downloading and processing of data from several key agencies: "
               "the European Space Agency (ESA), UK Met Office (UKMO), NASA, Mercator Ocean International (MOI). The scripts are capable of "
               "retrieving long-term datasets for specified geographical areas [points, polygons] and time ranges, converting the data into "
               "CSV files, and scheduling the execution using GitHub Actions. The final processed data is then stored in the Pawsey S3 bucket."),
        html.H3("Data Source and Data Point Position"),
        html.P("Explore the data point positions on the interactive map: [Data point position in the Map](#)"),
        html.H3("Data Sources"),
        html.Ul([
            html.Li("ESA: GLOBCOLOR (resolution: 4km) and Sentinel (resolution: 300m) marine environment products."),
            html.Li("MOI: Numerous MODEL output."),
            html.Li("UKMO: Access data from OSTIA temperature (resolution: 0.05°) products."),
            html.Li("NASA: Access data from the Group for High-Resolution Sea Surface Temperature (GHRSST (resolution: 0.01°)) and MODIS (resolution: 4km) through ERDDAP."),
        ]),
    ])
