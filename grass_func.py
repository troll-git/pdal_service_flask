import os
import sys
import subprocess
'''

print(sys.platform)
# define GRASS Database
# add your path to grassdata (GRASS GIS database) directory
gisdb = os.path.join(os.path.expanduser("~"), "grassdata")
# the following path is the default path on MS Windows
# gisdb = os.path.join(os.path.expanduser("~"), "Documents/grassdata")

# specify (existing) Location and Mapset
location = "nc_spm_08"
mapset = "user1"

# path to the GRASS GIS launch script
# we assume that the GRASS GIS start script is available and on PATH
# query GRASS itself for its GISBASE
# (with fixes for specific platforms)
# needs to be edited by the user
grass7bin = 'grass78'
'''
if sys.platform.startswith('win'):
    # MS Windows
    grass7bin = r'C:\OSGeo4Win\grass74.bat'
    # uncomment when using standalone WinGRASS installer
    # grass7bin = r'C:\Program Files (x86)\GRASS GIS 7.2.0\grass74.bat'
    # this can be avoided if GRASS executable is added to PATH
elif sys.platform == 'darwin':
    # Mac OS X
    # TODO: this have to be checked, maybe unix way is good enough
    grass7bin = '/Applications/GRASS/GRASS-7.2.app/'
'''
# query GRASS GIS itself for its GISBASE
startcmd = [grass7bin, '--config', 'path']
try:
    p = subprocess.Popen(startcmd, shell=False,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
except OSError as error:
    sys.exit("ERROR: Cannot find GRASS GIS start script"
             " {cmd}: {error}".format(cmd=startcmd[0], error=error))
if p.returncode != 0:
    sys.exit("ERROR: Issues running GRASS GIS start script"
             " {cmd}: {error}"
             .format(cmd=' '.join(startcmd), error=err))

gisbase = out.decode("utf-8")

# set GISBASE environment variable
os.environ['GISBASE'] = gisbase

# define GRASS-Python environment
grass_pydir = os.path.join(gisbase, "etc", "python")
sys.path.append(grass_pydir)
'''
# import (some) GRASS Python bindings
import grass.script as gscript
import grass.script.setup as gsetup
from grass.script import raster as r


print(gscript.gisenv())
#print(r.raster_info("data/norm.tif"))
