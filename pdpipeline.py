import pdal
import json
from osgeo import gdal,osr
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

polygon='MULTIPOLYGON (((618182.427 189812.596998469,618191.585 189812.62099847,618206.333 189815.261998474,618220.691 189817.54399847,618229.365 189818.493998475,618234.25 189819.033998476,618251.828 189820.920998465,618265.928 189821.985998465,618276.754 189823.222998474,618274.207 189811.096998475,618275.269 189800.865998475,618277.378 189780.573998475,618279.717 189765.527998466,618280.836 189758.418998468,618282.173 189751.394998468,618284.642 189738.611998464,618284.698 189738.412998475,618285.41 189733.422998472,618287.564 189718.58199847,618289.501 189710.423998471,618282.627 189707.201998468,618275.653 189706.275998472,618270.761 189705.627098467,618258.789 189703.838998477,618247.64 189702.361998471,618233.904 189699.987998473,618209.989 189696.881998473,618201.689 189695.802098477,618200.905 189702.349998474,618198.657 189716.968998478,618196.152 189731.850998475,618194.117 189744.824998466,618191.945 189758.835998471,618190.758 189765.873998471,618189.945 189770.870998472,618188.601 189779.694998467,618186.433 189793.516098469,618186.623 189793.540998473,618185.367 189802.035998476,618182.427 189812.596998469)))'

jyson={"pipeline":[{
        "type":"readers.pgpointcloud",
        "connection":"host='localhost' dbname='pointclouds' user='postgres' password='postgres' port='5432'",
        "table":"sthsm",
        "column":"points",
        "spatialreference":"EPSG:2180",
        "where":"PC_Intersects(points,ST_SetSRID(ST_Envelope(ST_GeomFromText('{}')),2180))".format(polygon)
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
{
    "type":"writers.las",
    "filename":"data/whatever3.las"
},
{
   "type": "writers.gdal",
   "resolution":0.1,
   "radius": 0.25,
   "filename":"data/norm66.tif",

}
]}


pipeline = pdal.Pipeline(json.dumps(jyson))
count = pipeline.execute()
arrays = pipeline.arrays
metadata = pipeline.metadata
log = pipeline.log


dst_crs = 'EPSG:4326'

with rasterio.open('data/norm66.tif') as src:
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds)
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height
    })

    with rasterio.open('data/norm84.tif', 'w', **kwargs) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest)