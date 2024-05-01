import os
from flask import Flask,render_template,request
import cv2
import numpy as np
import imutils
import predict as pdt
from PIL import Image
import base64
import time
import os
import json
app = Flask(__name__)
msg='welcome user'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    imageData = request.form['imageData']
    imgdata = base64.b64decode(imageData)
    path1 = 'static/medicine_test'
    if not os.path.exists(path1):
        os.makedirs(path1)
    filename = path1 + "/test_pill.jpg"
    with open(filename, 'wb') as f:
        f.write(imgdata)
    name,usage,info = pdt.predict_herb()
    x = {"name":name,'usage':usage,'info':info}
    return json.dumps(x)


if __name__=="__main__":
    app.run(port=5000, host = '0.0.0.0')


