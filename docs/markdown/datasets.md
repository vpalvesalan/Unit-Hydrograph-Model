# Dataset

This documentation provides a detailed overview of the datasets and sources used in this study. Data were gathered from publicly available repositories and include raster, shapefiles, and tabular data. These datasets were essential for training machine learning models.

## 1. Overview of Data Sources

| Data Type         | Source                          | Format       | Description                                   |
|-------------------|---------------------------------|--------------|-----------------------------------------------|
| Shapefiles        | US Census Bureau, USGS, NOAA, Esri   | `.shp` `.kmz` `.GeoJSON` | Vector data for geographic boundaries, stream gages, precipitation stations and dam location. |
| Raster Data       | USGS (SRTM), MRLC              | `.tiff`       | Elevation, water body, land cover data, land cover confidence, impervious surface, impervious surface descriptor.    |
| Tabular Data      | USGS, NOAA                     | `.csv`, `.json` | Time-series data for streamflow and precipitation. |

## 2. Detailed Description of Data

### 2.1 Shapefiles
Shapefiles were used to represent boundaries, stream gauge locations, and precipitation gauge stations within the study region.

- **US Boundary Shapefiles:**
  - **States:** 
    - **Source**: Downloaded from the [US Census Bureau TIGER/Line Shapefiles collection](https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2024&layergroup=States+%28and+equivalent%29).  
    - **Format:** `.shp`  
    - **Purpose:** Visualize state boundaries within the region of study.  
    - **Relevant Attributes:** [`NAME`: state name]
    - **Documentation**: [Available here](https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2024/TGRSHP2024_TechDoc.pdf)

  - **Counties:**
    - **Source**: Downloaded from the [US Census Bureau TIGER/Line Shapefiles collection](https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2024&layergroup=Counties+%28and+equivalent%29).  
    - **Format:** `.shp`  
    - **Purpose:** Visualize county-level boundaries.  
    - **Relevant Attributes:** [`NAME`: county name]  

- **U2 and U4 Watershed Boundary:** 
    - **Source**: USGS. Downloaded through TNM (The National Map) Rest API.
    - **Format:** `.shp`
    - **Purpose:** Used to delimit the region of study.  
    - **Relevant Attributes:** [`NAME` / `name`: watershed name]
    - **Documentation**: 
      - Rest API: [available here](https://tnmaccess.nationalmap.gov/api/v1/docs).
      - U2 and U4 WB: [available here](https://www.sciencebase.gov/catalog/item/5a1632b3e4b09fc93dd171de).  

- **Stream Gauge Stations:**  
  - **Source:** Downloaded from [USGS here](https://www.sciencebase.gov/catalog/item/63140610d34e36012efa3836).  
  - **Format:** `.shp`  
  - **Purpose:** Identify stream gauge locations within the study region.  
  - **Relevant Attributes:** [Provide specific Relevant Attributes here]  

- **Precipitation Gauge Stations:**  
  - **Source:** Downloaded from the [National Center For Environmental Information](https://gis.ncdc.noaa.gov/kml/precip_15.kmz) - NOAA.
  - **Format:** `.kmz`  
  - **Purpose:** Study precipitation station locations within the region.  
  - **Relevant Attributes:** [Provide specific Relevant Attributes here]

- **Dam Location:**  
  - **Source:** [National Inventory of Dams](https://nid.sec.usace.army.mil/), from U.S. Army Corps of Engineers [available here](https://nid.sec.usace.army.mil/#/downloads).
  - **Format:** `.gpkg` 
  - **Purpose:** Identify which watershed flow is regulated by dam and how it might influes Clark's UH parameters.
  - **Relevant Attributes:** ['name', 'nidId', 'riverName','damHeight', 'damLength', 'volume', 'maxStorage', 'normalStorage', 'surfaceArea', 'drainageArea','maxDischarge', 'geometry']
  - **Documentation:** [available here](https://resilience.climate.gov/datasets/fedmaps::national-inventory-of-dams-1/about).

- **World UTM Grid**:
  - **Source:** [Esri](https://hub.arcgis.com/datasets/esri::world-utm-grid/explore)
  - **Format:** `.GeoJSON`
  - **Purpose:** Identify which UTM zone the study region falls on.
  - **Relevant Attributes:**

### 2.2 Raster Data
Raster datasets provided spatial information for elevation, land cover, and water body characteristics.

- **Digital Elevation Model (DEM):**  
  - **Source:** Void-Filled Shuttle Radar Topography Mission (SRTM), available on [USGS Earth Explorer](https://earthexplorer.usgs.gov/).  
  - **Format:** `.tiff`  
  - **Resolution:** ~30m  
  - **Purpose:** Automatically delineate watershed boundaries and extract geomorphological features.  
  - **Relevant Attributes:** [Provide specific Relevant Attributes here] 
  -**Documentation**: [Available here](https://www.usgs.gov/centers/eros/science/usgs-eros-archive-digital-elevation-shuttle-radar-topography-mission-srtm-void). 

- **Water Body Raster:**  
  - **Source:** Shuttle Radar Topography Mission (SRTM), available on [USGS](https://www.usgs.gov/centers/eros/science/usgs-eros-archive-digital-elevation-shuttle-radar-topography-mission-water).
  - **Resolution**:   
  - **Format:** `.tiff`  
  - **Purpose:** Used as a modeling feature to calculate water body percentages.  

- **Historical Land Cover Raster:**  
  - **Source:** Downloaded from the [MRLC Viewer](https://www.mrlc.gov/viewer/).  
  - **Format:** `.GeoTIFF`  
  - **Resolution:** 30m
  - **Purpose:** Extract land use features.  
  - **Relevant Attributes:** `Pixel Value`: indicates the type of Land Cover.
  - **Documentation:** [Available here](../pdf/LSDS-2103_Annual_National_Land_Cover_Database_(NLCD)_Collection_1_Science_Product_User_Guide-v1.0_2024_10_15.pdf) or [here](https://www.mrlc.gov/documentation).

- **Land Cover Confidence Raster:**  
  - **Source:** Downloaded from the [MRLC Viewer](https://www.mrlc.gov/viewer/).  
  - **Format:** `.GeoTIFF`  
  - **Resolution:** 30m
  - **Purpose:** Extract level of confidence for the Land Cover dataset.  
  - **Relevant Attributes:** `Pixel Value`: level of confidence. Varies from 1 to 100. 250 are no data values.
  - **Documentation:** [Available here](../pdf/LSDS-2103_Annual_National_Land_Cover_Database_(NLCD)_Collection_1_Science_Product_User_Guide-v1.0_2024_10_15.pdf) or [here](https://www.mrlc.gov/documentation).

- **Fractional Impervious Surface Raster:**  
  - **Source:** Downloaded from the [MRLC Viewer](https://www.mrlc.gov/viewer/).  
  - **Format:** `.GeoTIFF`  
  - **Resolution:** 30m
  - **Purpose:** Extract percentage of impervious area.  
  - **Relevant Attributes:** `Pixel Value`: percentage of impervious area. Varies from 1 to 100. 250 are no data values. 
  - **Documentation:** [Available here](../pdf/LSDS-2103_Annual_National_Land_Cover_Database_(NLCD)_Collection_1_Science_Product_User_Guide-v1.0_2024_10_15.pdf) or [here](https://www.mrlc.gov/documentation).  

- **Impervious Descriptor Raster:**  
  - **Source:** Downloaded from the [MRLC Viewer](https://www.mrlc.gov/viewer/).  
  - **Format:** `.GeoTIFF`  
  - **Resolution:** 30m
  - **Purpose:** Extract the type of impervious surface.  
  - **Relevant Attributes:** `Pixel Value`: discrete values: 0 (non-urban), 1 (roads), 2 (urban). 250 are no data values. 
  - **Documentation:** [Available here](../pdf/LSDS-2103_Annual_National_Land_Cover_Database_(NLCD)_Collection_1_Science_Product_User_Guide-v1.0_2024_10_15.pdf) or [here](https://www.mrlc.gov/documentation).

### 2.3 Historical Tabular Data
Tabular datasets were used to analyze temporal dynamics and provide targets for model training.

- **Streamflow Data:**  
  - **Source:** Downloaded from USGS Data Service using the [Data Retrieval API](https://doi-usgs.github.io/dataRetrieval/), which is an R package.  
  - **Format:** `.json` 
  - **Purpose:** Target data for optimizing time of concentration and storage coefficients of Clark's Unit Hydrograph; target data for neural network models.  
  - **Relevant Attributes:** [Provide specific Relevant Attributes here]  

- **Precipitation Data:**  
  - **Source:** NOAA, avialable through Rest API. [Documentation available here](https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted).
  - **Format:** `.json`
  - **Resolution:** 15min and 24h.  
  - **Purpose:** Main input feature used to select storm events for modeling.  
  - **Relevant Attributes:**
    - `date`: date of end of observation in local time. Format: YYYY-MM-DDTHH:MM:SS.
    - `value`: the precipitation amount.
    - `datatype`: indicates wether `value` is the volume of precipitation accumulated as recorded in the station for the 15min period (QGAG) or the amount of precipitation recorded for the 15 minute period (QPCP).
    - `attributes`: flags. _HT_: tenths of inches. _HI_: hundredths of inches. _MM_: tenths of millimeters.
  - **Documentation**: [Available here](https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C00505/html), [and here](../pdf/PRECIP_15_documentation.pdf).

## 3. Integration into Machine Learning Workflow

- **Data Harmonization:**  
  - Standardized spatial extents and resolutions for raster datasets.  
  - Aligned time-series data for streamflow and precipitation.  

- **Feature Engineering:**  
  - Extracted geomorphological features from DEM.  
  - Derived land cover statistics from historical land cover data.  

- **Event Selection**
    - Selected storm events

- **Parameters optmization**
    - Optmized _T<sub>c</sub>_ and _R_ coefficents for Clark's Unit Hydrograph

- **Targets:**
  - _T<sub>c</sub>_, _R_ optmized parameters served as the primary target variable for training and validation. 
  - Streamflow data served as the target variable for training ANN model.  

## 4. Glossary of Terms and Acronyms

| Term/Acronym | Full Name                                    | Description/Details                                 |
|--------------|---------------------------------------------|----------------------------------------------------|
| **USGS**     | United States Geological Survey             | A scientific agency of the U.S. government that provides data on natural resources, hazards, and geography. |
|**TNM** | The National Map | The National Map is a suite of products and services that provide access to base geospatial information.|
| **NOAA**     | National Oceanic and Atmospheric Administration | A U.S. federal agency focused on the conditions of the oceans and the atmosphere. |
|**MRLC** | Multi-Resolution Land Characteristics Consortium |  Group of federal agencies that create and coordinate digital land cover data for the United States. |
| **DEM**      | Digital Elevation Model                     | A raster representation of the Earth's surface used to analyze terrain and extract features like slope and elevation. |
| **SRTM**     | Shuttle Radar Topography Mission            | A NASA mission that produced high-resolution topographic data of the Earth's surface. |
| **NCEI**     | National Centers for Environmental Information | A NOAA division responsible for preserving and providing access to environmental data. |
| **_T<sub>c</sub>_, _R_** | Time of Concentration and Storage Coefficient | Coefficients for generating Clark's Unit Hydrographs |


## 5. References

- USGS Earth Explorer: [Visit Site](https://earthexplorer.usgs.gov/).  
- NOAA National Centers for Environmental Information: [Visit Site](https://www.ncei.noaa.gov/).  
- MRLC Viewer: [Visit Site](https://www.mrlc.gov/viewer/).  
- USGS Data Retrieval API: [Visit Site](https://doi-usgs.github.io/dataRetrieval/).  

---

For further details, please contact Alan Alves at vpalvesalan@gmail.com.
