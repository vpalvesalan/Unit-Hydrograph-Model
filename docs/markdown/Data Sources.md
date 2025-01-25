# Data types and sources

Data were gathered from public avialable repositories. Raster, shapefies and tabular data were used:

1. ### Shapefiles
    - **US boundary**: downloaded from [US Census Buerau TIGER/Line Shapefiles collection](https://www.census.gov/cgi-bin/geo/shapefiles/index.php). Used to visualize region of study.
      - States. [Clique here to access the data](https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2024&layergroup=States+%28and+equivalent%29). (Accessed on 01/08/2025).shp format
        - Attributes
      - Counties [Clique here to access the data](https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2024&layergroup=Counties+%28and+equivalent%29). (Accessed on 01/08/2025). shp format
        - Attributes
    - **H8 Watershed boundary**: used to delimit region of study
    
    - **Streamgauge stations**: downloaded from [USGS Watch Water Data Service](https://waterwatch.usgs.gov/?id=wwds_shp). (Accessed on 01/08/2025). shp format. 
    Used to select stations locations within the study region
        - Attributes
    - **Preciptation Gauge Stations** downloaded from the [National Center For Environmental Information](https://gis.ncdc.noaa.gov/kml/precip_15.kmz) - NOAA. `kmz` format Accessed on 01/08/2025.
     Used to study location within the studied region
        - Attibutes
2. ### Raster Data
    - **Digital Elevation Model**:  Void Filled from Shuttle Radar Topography Mission (SRTM) avialable on USGS Earth Explorer [click here](https://www.usgs.gov/centers/eros/science/usgs-eros-archive-digital-elevation-shuttle-radar-topography-mission-srtm-void?qt-science_center_objects=0#qt-science_center_objects). tiff format
    used to automatically delineate watershed boundaries and extract geomorphologic features
        - Resolution: 30m
        - Attributes:    
    - **Water Body** - also from from Shuttle Radar Topography Mission (SRTM)  [Click here](https://www.usgs.gov/centers/eros/science/usgs-eros-archive-digital-elevation-shuttle-radar-topography-mission-water?qt-science_center_objects=0#qt-science_center_objects) tiff format
    used as feature for modeling as percentage of water impoudements
    - **Historical Land Cover**  - downloaded from MRLC [available here](https://www.mrlc.gov/viewer/). Used to extract land use features
    for data documentation [click here](https://www.mrlc.gov/documentation)
        - Attributes
3. ### Historical Tabular Data
    - **Stream flow**: downloaded from USGS Data Service Using the Data Retrieval API. For a full documentantion on the API [click here](https://doi-usgs.github.io/dataRetrieval/). (Accessed on 01/08/25). Used as targets for optizing Time of concentration and Storage coefficents of Clarks Unit Hydrograph; used as target of neural network model
        - Attributes
    - **Precipitation height**: More information on the dataset [is avialable here](https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C00505/html). Main feature. Used to select storm evetns and input for model
        - Attributes
Token USGS API y47apaXWn2t869CbtILN@!3V2WVbsPAHzM6RgUi0hZHYkXRgK3Vd_9qJwb9TK0IS

