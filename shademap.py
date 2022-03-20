import subprocess
import shutil

def createShademap(infile,outfile):
    #create mapset
    subprocess.call('grass78 -c data/84.tif -e /home/marek/pdal_service_flask/data/temp',shell=True)

    #import tiff file to mapset
    
    subprocess.call('grass78 /home/marek/pdal_service_flask/data/temp/PERMANENT/ -e -c --exec r.import input={} output=inputraster'.format(infile),shell=True)
    
    #set gregion from raster (for band 1)
    subprocess.call('grass78 /home/marek/pdal_service_flask/data/temp/PERMANENT/ -e -c --exec g.region -ap raster=inputraster.1',shell=True)
    
    #print raster stats
    subprocess.call('grass78 /home/marek/pdal_service_flask/data/temp/PERMANENT/ -e -c --exec r.univar map=inputraster.1',shell=True)

    #make sun map
    subprocess.call('grass78 /home/marek/pdal_service_flask/data/temp/PERMANENT/ -c -e --exec r.sunmask -g inputraster.1 year=2021 month=4 day=22 hour=14 minute=30 timezone=+2 output=shademap',shell=True)

    #export map to tiff
    subprocess.call('grass78 /home/marek/pdal_service_flask/data/temp/PERMANENT/ --exec r.out.gdal input=shademap output={} --overwrite'.format(outfile),shell=True)
    
    shutil.rmtree('/home/marek/pdal_service_flask/data/temp')

#createShademap('data/res.tif','data/outf.tif')