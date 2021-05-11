import os
import pdal
import json




def uploadtopg(filename):

    jyson={
        "pipeline":[
        {
            "type":"readers.las",
            "filename":"{}".format(filename),
            "spatialreference":"EPSG:25832"
        },
        {
            "type":"filters.chipper",
            "capacity":400
        },
        {
            "type":"writers.pgpointcloud",
            "connection":"host='localhost' dbname='pointclouds' user='postgres' password='postgres' port='5432'",
            "table":"sthsm3",
            "compression":"dimensional",
            "column": "points",
            "srid":"25832"
        }
        ]
    }

    pipeline = pdal.Pipeline(json.dumps(jyson))
    count = pipeline.execute()
    arrays = pipeline.arrays
    metadata = pipeline.metadata
    log = pipeline.log

directory="/home/marek/Downloads/eksport_438613_20210504/1174/data"
for filename in os.listdir(directory):
    newfile=os.path.join(directory,filename)
    print ('uploading: '+filename)
    uploadtopg(newfile)