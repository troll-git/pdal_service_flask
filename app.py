from flask import Flask
from flask_restful import Api,Resource,reqparse
from flask_cors import CORS,cross_origin
from pdpipeline import createRaster




app=Flask(__name__)

api=Api(app)
CORS(app)

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