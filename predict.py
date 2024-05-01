# -*- coding: utf-8 -*-

import tensorflow as tf 
classifierLoad = tf.keras.models.load_model('model.h5')

import numpy as np
# from keras.preprocessing import image
from keras_preprocessing.image import load_img
cwd="static/test/"

def predict_cancer():
    stage_detected=""
    test_image = load_img(cwd+'test.jpg', target_size = (200,200))
    test_image = np.expand_dims(test_image, axis=0)
    result = classifierLoad.predict(test_image)
    print(result)
    if result[0][0] == 1:
        return 0
    elif result[0][1] == 1:
        return 1


