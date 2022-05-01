import os
from distutils.log import debug
from flask import Flask, jsonify, request, url_for, redirect
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api
from check.checker import PredictionAPI
from check.imageProcessing import ImageProcessingAPI
from flask_cors import CORS
# from resources.routes import initialize_routes
import json

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app=Flask(__name__)
api=Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# class CoreApi(Resource):
@app.route('/')
def home():
    return "UrHeart"


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
    return jsonify({'predResult':PredictionAPI(input_data)})

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            #flash('No image selected for uploading')
            return jsonify({'predResult': 'No image selected'})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('uploaded_image filename: ' + filename)
            #flash('Image successfully uploaded and displayed below')
            #return redirect(url_for('static', filename='uploads/' + filename), code=301)
            return jsonify({
                'predResult':ImageProcessingAPI(str(filename)),
                'fileloc': str(url_for('static', filename='uploads/' + filename))
            })
        else:
            #flash('Allowed image types are -> png, jpg, jpeg, gif')
            return jsonify({'predResult': 'Invalig image format'})
    

# initialize_routes(api)

if __name__ == "__main__":
    #app.secret_key = 'ur' #the secret_key can be anything
    app.env = "development"
    port = os.environ.get("PORT", 5000)
    app.run(debug = False, host = '0.0.0.0', port=port)
    #app.run(debug=True)

    #'0.0.0.0'
