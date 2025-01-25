import geopandas as gpd
from shapely.geometry import Polygon
from scipy.spatial import Voronoi
import numpy as np
from shapely.ops import unary_union

def derive_thiessen_polygons(gdf_points: gpd.GeoDataFrame, clipping_gdf: gpd.GeoDataFrame, preserve_attribute: str) -> gpd.GeoDataFrame:
    """
    Derive Thiessen (Voronoi) polygons from a GeoDataFrame of points using scipy,
    clipped by another GeoDataFrame, and preserve a specified attribute.

    Parameters:
    -----------
    gdf_points : geopandas.GeoDataFrame
        GeoDataFrame containing point geometries.
    clipping_gdf : geopandas.GeoDataFrame
        GeoDataFrame containing the geometry to clip the Voronoi polygons to.
    preserve_attribute : str
        The name of the column in gdf_points to preserve in the output polygons.

    Returns:
    --------
    geopandas.GeoDataFrame
        GeoDataFrame containing the Thiessen polygons with the preserved attribute.
    """
    # Validate input GeoDataFrames
    if gdf_points.empty:
        raise ValueError("The input GeoDataFrame 'gdf_points' is empty.")
    
    if not all(gdf_points.geometry.type == 'Point'):
        raise TypeError("All geometries in 'gdf_points' must be of type 'Point'.")
    
    if gdf_points.crs is None:
        raise ValueError("The GeoDataFrame 'gdf_points' must have a defined CRS.")
    
    if clipping_gdf.crs is None:
        raise ValueError("The GeoDataFrame 'clipping_gdf' must have a defined CRS.")
    
    # Ensure both GeoDataFrames use the same CRS
    if clipping_gdf.crs != gdf_points.crs:
        clipping_gdf = clipping_gdf.to_crs(gdf_points.crs)
    
    # Warn if CRS is geographic
    if gdf_points.crs.is_geographic:
        import warnings
        warnings.warn(
            "The CRS is geographic. For accurate Voronoi polygons, consider projecting to a planar CRS.",
            UserWarning
        )
    
    # Extract point coordinates
    points = np.array([[point.x, point.y] for point in gdf_points.geometry])
    
    # Compute Voronoi diagram
    vor = Voronoi(points)
    
    # Function to construct polygon from Voronoi region
    def construct_polygon(region):
        if -1 in region:
            return None  # Infinite region, cannot construct a finite polygon
        polygon = [vor.vertices[i] for i in region]
        return Polygon(polygon)
    
    # Generate polygons corresponding to each point
    polygons = []
    for point_idx, region_idx in enumerate(vor.point_region):
        region = vor.regions[region_idx]
        poly = construct_polygon(region)
        polygons.append(poly)
    
    # Create GeoDataFrame with preserved attribute
    thiessen_gdf = gpd.GeoDataFrame(
        gdf_points[[preserve_attribute]].reset_index(drop=True),
        geometry=polygons,
        crs=gdf_points.crs
    )
    
    # Remove polygons that couldn't be constructed
    thiessen_gdf = thiessen_gdf[thiessen_gdf.geometry.notnull()].reset_index(drop=True)
    
    # Clip Thiessen polygons using the provided clipping shapefile
    clipping_union = unary_union(clipping_gdf.geometry)
    thiessen_gdf['geometry'] = thiessen_gdf.geometry.intersection(clipping_union)
    
    # Remove any resulting empty geometries after clipping
    thiessen_gdf = thiessen_gdf[~thiessen_gdf.geometry.is_empty].reset_index(drop=True)
    
    return thiessen_gdf