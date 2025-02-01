import geopandas as gpd
from shapely.geometry import Polygon
from shapely.ops import unary_union
from scipy.spatial import Voronoi
import numpy as np

def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite Voronoi regions in a 2D diagram to finite regions.
    
    Parameters
    ----------
    vor : scipy.spatial.Voronoi instance
        Input Voronoi diagram.
    radius : float, optional
        Distance to 'points at infinity'. If None, a default value based on the
        point set extent will be used.
    
    Returns
    -------
    regions : list of lists
        Indices of vertices in each finite Voronoi region.
    vertices : ndarray
        Coordinates for the vertices.
    """
    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")
    
    new_regions = []
    new_vertices = vor.vertices.tolist()
    
    # Use the mean of the points as the center
    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max() * 2
    
    # Map ridge vertices to all ridges for a point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))
    
    # Reconstruct each Voronoi region
    for p1, region_index in enumerate(vor.point_region):
        vertices_indices = vor.regions[region_index]
        if all(v >= 0 for v in vertices_indices):
            # finite region
            new_regions.append(vertices_indices)
            continue
        
        # Reconstruct a non-finite region
        region = [v for v in vertices_indices if v >= 0]
        for p2, v1, v2 in all_ridges[p1]:
            # If one of the vertices is infinite
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                continue  # finite ridge already in region
            # Compute the missing endpoint
            tangent = vor.points[p2] - vor.points[p1]
            tangent /= np.linalg.norm(tangent)
            normal = np.array([-tangent[1], tangent[0]])
            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, normal)) * normal
            far_point = vor.vertices[v2] + direction * radius
            region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())
        
        # Order region vertices in a counterclockwise fashion
        vs = np.asarray([new_vertices[v] for v in region])
        angles = np.arctan2(vs[:, 1] - center[1], vs[:, 0] - center[0])
        region = np.array(region)[np.argsort(angles)]
        new_regions.append(region.tolist())
    
    return new_regions, np.asarray(new_vertices)

def derive_thiessen_polygons(gdf_points: gpd.GeoDataFrame, 
                              clipping_gdf: gpd.GeoDataFrame, 
                              preserve_attribute: str) -> gpd.GeoDataFrame:
    """
    Derive Thiessen (Voronoi) polygons from a GeoDataFrame of points using scipy,
    clip them with a provided polygon, and preserve a specified attribute.
    
    Parameters
    ----------
    gdf_points : geopandas.GeoDataFrame
        GeoDataFrame containing point geometries.
    clipping_gdf : geopandas.GeoDataFrame
        GeoDataFrame containing the geometry to clip the Voronoi polygons to.
    preserve_attribute : str
        The name of the column in gdf_points whose values will be kept with the
        resulting polygons.
    
    Returns
    -------
    geopandas.GeoDataFrame
        GeoDataFrame containing the clipped Thiessen polygons with the preserved
        attribute.
    """
    # Validate inputs
    if gdf_points.empty:
        raise ValueError("The input GeoDataFrame 'gdf_points' is empty.")
    if not all(gdf_points.geometry.geom_type == 'Point'):
        raise TypeError("All geometries in 'gdf_points' must be of type 'Point'.")
    if gdf_points.crs is None:
        raise ValueError("The GeoDataFrame 'gdf_points' must have a defined CRS.")
    if clipping_gdf.crs is None:
        raise ValueError("The GeoDataFrame 'clipping_gdf' must have a defined CRS.")
    
    # Ensure both GeoDataFrames use the same CRS
    if clipping_gdf.crs != gdf_points.crs:
        clipping_gdf = clipping_gdf.to_crs(gdf_points.crs)
    
    # Warn if using a geographic CRS
    if gdf_points.crs.is_geographic:
        import warnings
        warnings.warn(
            "The CRS is geographic. For accurate Voronoi polygons, consider projecting to a planar CRS.",
            UserWarning
        )
    
    # Extract point coordinates
    points = np.array([[pt.x, pt.y] for pt in gdf_points.geometry])
    
    # Compute the Voronoi diagram
    vor = Voronoi(points)
    
    # Determine a radius based on the clipping polygon's extent
    clipping_union = unary_union(clipping_gdf.geometry)
    # Clean the clipping union if it is invalid
    if not clipping_union.is_valid:
        clipping_union = clipping_union.buffer(0)
    
    minx, miny, maxx, maxy = clipping_union.bounds
    radius = max(maxx - minx, maxy - miny) * 2
    
    # Convert the Voronoi regions into finite polygons
    regions, vertices = voronoi_finite_polygons_2d(vor, radius)
    
    # Create polygons from the regions and clean them with buffer(0)
    polygons = []
    for region in regions:
        polygon_coords = vertices[region]
        poly = Polygon(polygon_coords)
        # Clean the polygon (fix potential invalidities)
        poly = poly.buffer(0)
        polygons.append(poly)
    
    # Create a GeoDataFrame preserving the desired attribute
    thiessen_gdf = gpd.GeoDataFrame(
        gdf_points[[preserve_attribute]].reset_index(drop=True),
        geometry=polygons,
        crs=gdf_points.crs
    )
    
    # Clip the Thiessen polygons using the cleaned clipping union
    thiessen_gdf['geometry'] = thiessen_gdf.geometry.intersection(clipping_union)
    
    # Remove any empty geometries after clipping
    thiessen_gdf = thiessen_gdf[~thiessen_gdf.geometry.is_empty].reset_index(drop=True)
    
    return thiessen_gdf