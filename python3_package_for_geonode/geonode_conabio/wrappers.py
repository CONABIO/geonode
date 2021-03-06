import os

import numpy as np

import fiona
import rasterio
from rasterio.crs import CRS as CRS_rio
from rasterio.warp import transform_geom, \
                          calculate_default_transform, reproject, Resampling
from pyproj import Proj

from geonode_conabio.utils_text import normalize_name_classes

def reproj_normalize_and_write_large_vector(feature_collection, feature_collection_schema,
                                            list_name_attributes,
                                            layer_name,
                                            output_filename,
                                            source_crs,
                                            driver = "ESRI Shapefile",
                                            destiny_crs = "4326",
                                            is_geographic = True):
    """
    Reprojection, normalizing of fields using name of attributes in list and
    write to file. Function used for large size vectors.
    Args:
        feature_collection (geojson): GeoJSON like dict object or iterable of GeoJSON like objects.
        feature_collection_schema (dict): dictionary holding schema of feature_collection.
        list_name_attributes (list): attributes of type text that will be searched for to be normalized.
        layer_name (str): name of layer that will be in output_filename.
        output_filename (str): filename that will be written in filesystem.
        source_crs (str): string of source coordinate reference system.
        
    """
    dst = fiona.open(output_filename, 'w',
                     driver = driver,
                     layer = layer_name,
                     crs = CRS_rio.from_epsg(destiny_crs).to_proj4(),
                     schema = feature_collection_schema)
    dst.close()
    with fiona.open(output_filename, 'a',
                    driver = driver,
                    layer = layer_name,
                    crs = CRS_rio.from_epsg(destiny_crs).to_proj4(),
                    schema = feature_collection_schema) as dst:
        for feature in feature_collection:
            if not is_geographic:
                feature['geometry'] = transform_geom(CRS_rio.from_proj4(source_crs), 
                                                     CRS_rio.from_epsg(destiny_crs),
                                                     feature['geometry'])
            for att in list_name_attributes:
                feature['properties'][att] = normalize_name_classes(feature['properties'][att])
            dst.write(feature)

def reproj_normalize_and_write_small_medium_size_vector(geodataframe,
                                                        list_name_attributes,
                                                        layer_name,
                                                        input_directory,
                                                        output_filename,
                                                        destiny_crs="EPSG:4326"):
    """
    Reprojection, normalizing of fields using name of attributes in list and
    write to file. Function used for small-medium size vectors.
    Args:
        geodataframe (GeoDataFrame): tablular data structure that contains a column called geometry which contains a GeoSeries.
        list_name_attributes (list): attributes of type text that will be searched for to be normalized.
        layer_name (str): name of layer that will be in output_filename.
        input_directory (str): path of input filename that will hold temporary shapefile that will be registered in geonode.
        output_filename (str): filename without extension that will be written in filesystem. Will be used to create dir with same name. Includes path.
    Rerturn:
        output_filename_geonode (str): path of shapefile in file system that will be registered in geonode.
    """
    #reproject
    crs_src = geodataframe.crs
    src_crs = crs_src.to_string()
    proj_src_crs = Proj(src_crs)    
    if not proj_src_crs.crs.is_geographic:
        gdf_reproj = geodataframe.to_crs(destiny_crs)
    else:
        gdf_reproj = geodataframe
    #normalize
    if list_name_attributes[0]:
        gdf_reproj[gdf_reproj.columns & list_name_attributes] = gdf_reproj[gdf_reproj.columns & list_name_attributes].apply(lambda s: s.apply(normalize_name_classes))
    #write shapefile
    output_filename_geonode = os.path.join(input_directory, os.path.basename(output_filename))
    os.makedirs(output_filename_geonode)
    output_filename_geonode = os.path.join(output_filename_geonode, os.path.basename(output_filename))
    output_filename_geonode = output_filename_geonode + ".shp"
    gdf_reproj.to_file(output_filename_geonode,
                       layer=layer_name,
                       driver = "ESRI Shapefile")
    #write geopackage
    gdf_reproj.to_file(output_filename + ".gpkg",
                       layer=layer_name,
                       driver = "GPKG")    
    return output_filename_geonode

def reproj_and_write_one_band_raster(source_dataset, output_filename,
                                     destiny_crs = "EPSG:4326"):
    """
    Reprojection, compression, tiling and writing of one band raster to file.
    Args:
        source_dataset (ndarray or Band): The source is a 2 ndarray, or Rasterio one band object. 
        output_filename (str): filename that will be written in filesystem.
    """
    source_meta = source_dataset.meta.copy()
    source_transform = source_dataset.transform
    source_width = source_dataset.width
    source_height = source_dataset.height
    source_crs = source_dataset.crs
    
    source_crs_string = source_crs.to_string()
    proj_crs = Proj(source_crs_string)
            
    if not proj_crs.crs.is_geographic:
        transform, width, height = calculate_default_transform(source_crs, destiny_crs, 
                                                               source_width, source_height, 
                                                               *source_dataset.bounds)
        source_meta.update({'crs': destiny_crs,
                           'transform': transform,
                           'width': width,
                           'height': height
                            })
    else:
        transform, width, height = source_transform, source_width, source_height
    
    source_meta.update({'driver': 'GTiff',
                        'count': 1,
                        'dtype': rasterio.uint8,
                        'compress': 'lzw',
                        'tiled': True
                        })
    with rasterio.open(output_filename, 'w', **source_meta,
                       ) as dst:
        array = np.zeros((height, width), dtype=rasterio.uint8)
        reproject(source=rasterio.band(source_dataset, 1),
                  destination=array,
                  src_transform=source_transform,
                  src_crs=source_crs,
                  dst_transform=transform,
                  dst_crs=destiny_crs,
                  resampling=Resampling.nearest
                  )  
        dst.write(array, 1)
        
def write_raster_with_cmap_in_dir(source_path_layer, destiny_path_layer, rgba_dict,
                                  nocmap):
    """
    Tiling, compression and cmap writing of one band raster to file.
    Args:
        source_path_layer (str): path of source layer already registered in geonode
        destiny_path_layer (str): destiny path that will have raster
        rgba_dict (dict): rgb mapping of classes to colors in rgba values
        nocmap (boolean): if true dont write cmap
    """
    with rasterio.open(source_path_layer) as src:
        arr = src.read(1)
        meta = src.meta
    meta["compress"] = "lzw"
    meta["tiled"] = True
    
    with rasterio.open(destiny_path_layer, 'w', **meta) as dst:
        dst.write(arr, indexes=1)
        if not nocmap: #write cmap
            dst.write_colormap(1,rgba_dict)
            cmap_result = dst.colormap(1)