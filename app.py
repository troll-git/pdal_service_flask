from flask import Flask,jsonify,send_from_directory
from flask_restful import Api,Resource,reqparse
from flask_cors import CORS,cross_origin
from pdpipeline import createRaster
import os
#from shademap import createShademap


UPLOAD_DIRECTORY = "data"


app=Flask(__name__)

api=Api(app)
CORS(app)

@app.route("/data")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)

@app.route("/data/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


#CORS(app,resorces={r'/*': {"origins": '*'}})
pdal_args=reqparse.RequestParser()
pdal_args.add_argument("wkt",type=str,help="extent of clip polygon")

class PdalResourse(Resource):
    def get(self):
        args=pdal_args.parse_args()
        rasterurl=createRaster(args)
        return{"data":"hi there","url":rasterurl}


api.add_resource(PdalResourse,"/pdal")

if __name__=="__main__":
    app.run(debug=True)