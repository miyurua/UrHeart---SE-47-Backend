import pickle
import json
from sklearn.metrics import accuracy_score



def PredictionAPI(input_data):
    # checking using a ML algorithm
    
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
        return NHDRes, 200
    else:
        print('This Person is Likely to have a Heart Disease')
        HDRes = {
            'output':'This Person is Likely to have a Heart Disease',
            'status': 200
        }
        return HDRes, 200
