from distutils.log import debug
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from check.checker import PredictionAPI
# from resources.routes import initialize_routes
import json


app=Flask(__name__)
api=Api(app)


# class CoreApi(Resource):

@app.route('/predict', methods=['POST'])
def predict():
    test_data = request.json
    s1 = json.dumps(test_data)
    print_json = json.loads(s1)
    list = print_json['body']
    input_data = (  float(list['age']), 
                    float(list['sex']), 
                    float(list['chestPainType']),	
                    float(list['restingBP']), 
                    float(list['cholestrol']), 
                    float(list['fastingBloodSugar']), 
                    float(list['restingECG']), 
                    float(list['maxHeartRate']), 
                    float(list['exerciseAngina']),	
                    float(list['oldpeak']), 
                    float(list['STslope']))
    return jsonify({'predResult':str(PredictionAPI(input_data))})


# initialize_routes(api)
app.run(debug=True)
