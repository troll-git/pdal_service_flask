from flask import Flask
from flask_restful import Api,Resource,reqparse

app=Flask(__name__)
api=Api(app)

pdal_args=reqparse.RequestParser()
pdal_args.add_argument("name",type=str,help="name whatever")

class PdalResourse(Resource):
    def get(self):
        args=pdal_args.parse_args()
        return{"data":"hi there","name":args}

api.add_resource(PdalResourse,"/pdal")

if __name__=="__main__":
    app.run(debug=True)