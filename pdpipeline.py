import pdal
import json
from osgeo import gdal,osr
#import rasterio
#from rasterio.warp import calculate_default_transform, reproject, Resampling
from datetime import datetime
import os
from shademap import createShademap

def createRaster(wkt):
    polygon=wkt['wkt']
    today=datetime.now()
    filelas="data/{}.las".format(today)
    fileras="data/{}.tif".format(today)
    fileras84="data/{}84.tif".format(today)
    shademap="data/{}shade.tif".format(today)
    jyson={"pipeline":[{
        "type":"readers.pgpointcloud",
        "connection":"host='localhost' dbname='pointclouds' user='postgres' password='postgres' port='5432'",
        "table":"sthsm3",
        "column":"points",
        "spatialreference":"EPSG:25832",
        "where":"PC_Intersects(points,ST_SetSRID(ST_Envelope(ST_GeomFromText('{}')),25832))".format(polygon)
    },
   {
        "type":"filters.crop",
        "polygon":polygon
   },
    {
        "type":"filters.hag_nn"
    },
    {
        "type":"filters.ferry",
        "dimensions":"HeightAboveGround=>Z"
    },
 #   {
 #       "type":"writers.las",
 #       "filename":filelas
 #   },
 #   {
 #       "type":"filters.reprojection",
 #       "in_srs":"EPSG:25832",
 #       "out_srs":"EPSG:4326"
 #   },
    {
    "type": "writers.gdal",
    "resolution":+0.25,
    "radius": 0.5,
    "filename":fileras,

    },
    ]}
    print(polygon)
    
    pipeline = pdal.Pipeline(json.dumps(jyson))
    count = pipeline.execute()
    arrays = pipeline.arrays
    metadata = pipeline.metadata
    log = pipeline.log
    print("done")

    input_raster = gdal.Open(fileras)
    warp = gdal.Warp(fileras84,input_raster,dstSRS='EPSG:4326')
    #createShademap(fileras84,shademap)
    return fileras84
'''
    with rasterio.open(fileras) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        with rasterio.open(fileras84, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)
        createShademap(fileras84,shademap)
'''
    