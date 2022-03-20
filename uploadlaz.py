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
            "connection":"host='159.65.197.227' dbname='pointclouds' user='postgres' password='gunt1234' port='5433'",
            "table":"Oslo2019",
            "compression":"dimensional",
            "column": "points",
            "srid":"25832"
        }
        ]
    }

    pipeline = pdal.Pipeline(json.dumps(jyson))
    count = pipeline.execute()
    #arrays = pipeline.arrays
    #metadata = pipeline.metadata
    #log = pipeline.log

directory="/home/marek/Downloads/eksport_438613_20210504/1174/data"
length=len(os.listdir(directory))
for index,filename in enumerate(os.listdir(directory)):
    newfile=os.path.join(directory,filename)
    print ('uploading: {} ,{} of {}'.format(filename,index+1,length))
    uploadtopg(newfile)