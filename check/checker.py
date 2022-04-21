import pickle
import json
import numpy as np
from sklearn.metrics import accuracy_score

# Loading the ML model
model = pickle.load(open('ml_models/model.pkl', 'rb'))

# test data inputs
# input_data = (37, 1, 4, 140, 207, 0, 0, 130, 1, 1.5, 2)       # Likely
# input_data = (48, 0, 2, 120, 284, 0, 0, 120, 0, 0.0, 1)       # Unlikely

def PredictionAPI(input_data):
    
    # change the input data to a numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the numpy array as we are predicting for only on instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    prediction = model.predict(input_data_reshaped)
    print(prediction)

    if prediction[0] == 0:
        print('This Person is NOT Likely to have a Heart Disease')
        NHDRes = {
            'output':'This Person is NOT Likely to have a Heart Disease',
            'status': 200
        }
        return NHDRes
    else:
        print('This Person is Likely to have a Heart Disease')
        HDRes = {
            'output':'This Person is Likely to have a Heart Disease',
            'status': 200
        }
        return HDRes

# PredictionAPI(input_data)
