import json
from skimage.io import imread
from skimage import color
from skimage.filters import threshold_otsu,gaussian
from skimage.transform import resize
import numpy
from skimage.segmentation import slic
from skimage.color import label2rgb

import tensorflow as tf
import numpy as np
import glob
from matplotlib import pyplot as plt
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Loading the ML model
json_string = '{"class_name": "Sequential", "config": {"name": "sequential", "layers": [{"class_name": "InputLayer", "config": {"batch_input_shape": [null, 2073600], "dtype": "float32", "sparse": false, "ragged": false, "name": "dense_input"}}, {"class_name": "Dense", "config": {"name": "dense", "trainable": true, "batch_input_shape": [null, 2073600], "dtype": "float32", "units": 726, "activation": "relu", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}, {"class_name": "Dense", "config": {"name": "dense_1", "trainable": true, "dtype": "float32", "units": 128, "activation": "sigmoid", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}, {"class_name": "Dense", "config": {"name": "dense_2", "trainable": true, "dtype": "float32", "units": 128, "activation": "relu", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}, {"class_name": "Dense", "config": {"name": "dense_3", "trainable": true, "dtype": "float32", "units": 4, "activation": "softmax", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}]}, "keras_version": "2.8.0", "backend": "tensorflow"}'
from tensorflow.keras.models import model_from_json
model = model_from_json(json_string)

def ImageProcessingAPI(input_data):
    # image pre processing
    filepath = "static/uploads/"+input_data
    fig0 , ax0 = plt.subplots()
    fig0.set_size_inches(20, 20)
    image=imread(filepath)

    fig1 , ax1 = plt.subplots()
    fig1.set_size_inches(20, 20)
    # converting to gray scale
    grayscale = color.rgb2gray(image)
    # smoothening the image
    blurred_image = gaussian(grayscale, sigma=0.7)
    # thresholding to distinguish foreground and background
    # using otsu thresholding for getting threshold value
    global_thresh = threshold_otsu(blurred_image)
    # creating binary image based on threshold
    binary_global = blurred_image < global_thresh
    binary_global = numpy.invert(binary_global)
    image = binary_global

    # dividing the ECG leads from 1-13 from the above image
    Lead_1 = image[300:600, 150:643]
    Lead_2 = image[300:600, 646:1135]
    Lead_3 = image[300:600, 1140:1625]
    Lead_4 = image[300:600, 1630:2125]
    Lead_5 = image[600:900, 150:643]
    Lead_6 = image[600:900, 646:1135]
    Lead_7 = image[600:900, 1140:1625]
    Lead_8 = image[600:900, 1630:2125]
    Lead_9 = image[900:1200, 150:643]
    Lead_10 = image[900:1200, 646:1135]
    Lead_11 = image[900:1200, 1140:1625]
    Lead_12 = image[900:1200, 1630:2125]
    Lead_13 = image[1250:1480, 150:2125]
    Leads=[Lead_1,Lead_2,Lead_3,Lead_4,Lead_5,Lead_6,Lead_7,Lead_8,Lead_9,Lead_10,Lead_11,Lead_12,Lead_13]

    # plotting lead 1-12 & saving preprocessed image
    fig2 , ax2 = plt.subplots(4,3)
    fig2.set_size_inches(20, 20)
    x_counter=0
    y_counter=0
    for x,y in enumerate(Leads[:len(Leads)-1]):
        if (x+1)%3==0:
            ax2[x_counter][y_counter].imshow(y, cmap="gray")
            ax2[x_counter][y_counter].axis('off')
            ax2[x_counter][y_counter].set_title("Lead {}".format(x+1))
            x_counter+=1
            y_counter=0
        else:
            ax2[x_counter][y_counter].imshow(y, cmap="gray")
            ax2[x_counter][y_counter].axis('off')
            ax2[x_counter][y_counter].set_title("Lead {}".format(x+1))
            y_counter+=1
    fig2.savefig(filepath, dpi=72)

    # importing the pre processed image
    image=tf.keras.preprocessing.image.load_img(filepath, color_mode='grayscale')
    image=np.array(image)
    image=np.invert(image)
    print(image.shape)

    # reshape & normalization
    x_mean = 2.73714811267664
    x_std = 24.068791887587864
    epsilon = 1e-10
    input_reshaped = np.reshape(image, (1, 2073600))
    input_norm = (input_reshaped - x_mean) / (x_std + epsilon)

    # prediction
    prediction = model.predict(input_norm)
    print(prediction)
    print('shape of preds', prediction.shape)
    pred = np.argmax(prediction[0])
    print(pred)
 
    if pred == 0:
        print('Normal')
        NHDRes = {
            'output':'Normal',
            'status': 200
        }
        return NHDRes
    elif pred == 1:
        print('HB')
        NHDRes = {
            'output':'HB',
            'status': 200
        }
        return NHDRes
    elif pred == 2:
        print('MI')
        NHDRes = {
            'output':'MI',
            'status': 200
        }
        return NHDRes
    elif pred == 3:
        print('MI')
        NHDRes = {
            'output':'MI',
            'status': 200
        }
        return NHDRes
