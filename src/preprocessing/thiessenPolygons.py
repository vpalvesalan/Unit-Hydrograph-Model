import geopandas as gpd
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
from scipy.spatial import Voronoi
import numpy as np

def voronoi_finite_polygons_2d(vor, radius=None, center=None):
    """
    Reconstruct infinite Voronoi regions in a 2D diagram to finite regions.
    
    Parameters
    ----------
    vor : scipy.spatial.Voronoi instance
        Input Voronoi diagram.
    radius : float, optional
        Distance to 'points at infinity'. If None, a default value based on the
        point set extent will be used.
    center : array-like, optional
        The center to use for determining the direction of infinite ridges.
        If None, the mean of the Voronoi points is used.
    
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
    
    # Use the provided center or the mean of the points
    if center is None:
        center = vor.points.mean(axis=0)
    else:
        center = np.asarray(center)
    
    if radius is None:
        radius = vor.points.ptp().max() * 2
    
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))
    
    for p1, region_index in enumerate(vor.point_region):
        vertices_indices = vor.regions[region_index]
        if all(v >= 0 for v in vertices_indices):
            new_regions.append(vertices_indices)
            continue
        
        region = [v for v in vertices_indices if v >= 0]
        for p2, v1, v2 in all_ridges.get(p1, []):
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                continue
            
            tangent = vor.points[p2] - vor.points[p1]
            tangent /= np.linalg.norm(tangent)
            normal = np.array([-tangent[1], tangent[0]])
            
            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, normal)) * normal
            far_point = vor.vertices[v2] + direction * radius
            
            region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())
        
        vs = np.asarray([new_vertices[v] for v in region])
        angles = np.arctan2(vs[:, 1] - center[1], vs[:, 0] - center[0])
        region = np.array(region)[np.argsort(angles)]
        new_regions.append(region.tolist())
    
    return new_regions, np.asarray(new_vertices)

def derive_thiessen_polygons(gdf_points: gpd.GeoDataFrame, 
                             clipping_gdf: gpd.GeoDataFrame, 
                             preserve_attribute: str) -> gpd.GeoDataFrame:
    """
    Derive and clip Thiessen polygons using the clipping polygon's centroid for direction.
    """
    if gdf_points.empty:
        raise ValueError("The input GeoDataFrame 'gdf_points' is empty.")
    if not all(gdf_points.geometry.geom_type == 'Point'):
        raise TypeError("All geometries in 'gdf_points' must be of type 'Point'.")
    if gdf_points.crs is None or clipping_gdf.crs is None:
        raise ValueError("Both GeoDataFrames must have a defined CRS.")
    
    clipping_gdf = clipping_gdf.to_crs(gdf_points.crs)
    clipping_union = unary_union(clipping_gdf.geometry)
    if not clipping_union.is_valid:
        clipping_union = clipping_union.buffer(0)
    
    minx, miny, maxx, maxy = clipping_union.bounds
    radius = max(maxx - minx, maxy - miny) * 4
    clipping_center = clipping_union.centroid
    center_coords = (clipping_center.x, clipping_center.y)
    
    points = np.array([[pt.x, pt.y] for pt in gdf_points.geometry])
    vor = Voronoi(points)
    
    regions, vertices = voronoi_finite_polygons_2d(vor, radius=radius, center=center_coords)
    
    polygons = []
    for region in regions:
        polygon = Polygon(vertices[region])
        polygons.append(polygon.buffer(0))
    
    thiessen_gdf = gpd.GeoDataFrame(
        gdf_points[[preserve_attribute]].reset_index(drop=True),
        geometry=polygons,
        crs=gdf_points.crs
    )
    
    thiessen_gdf['geometry'] = thiessen_gdf.geometry.intersection(clipping_union)
    thiessen_gdf = thiessen_gdf[~thiessen_gdf.geometry.is_empty]
    
    return thiessen_gdf.reset_index(drop=True)