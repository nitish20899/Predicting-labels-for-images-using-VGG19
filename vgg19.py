# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 21:33:26 2020

@author: nitish hulk
"""
import numpy as np
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask ,redirect ,url_for ,request ,render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import sys
import os
import glob
import re

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

app = Flask(__name__)
model_path = 'vgg19.h5'

# load model
model =load_model(model_path)
model.make_predict_function()

def model_predict(img_path,model):
    img = image.load_img(img_path,target_size=(224,224))

    # preprocessing the image
    # converting the image to array
    x = image.img_to_array(img)
    x = np.expand_dims(x,axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    return preds

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')
    # rendering the html page

@app.route('/predict',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        # GET the file from the host
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath,'uploads',secure_filename(f.filename))
        # saving the uploaded file into a folder
        f.save(file_path)

        # here we are making prediciton by using the model_predict function
        pred = model_predict(file_path,model)
        pred_class = decode_predictions(pred,top=1)
        # decoding the predictions ( mapping the class number to class name )
        result = str(pred_class[0][0][1])
        return result
    return None



if __name__ == '__main__':
     app.run(debug=True)