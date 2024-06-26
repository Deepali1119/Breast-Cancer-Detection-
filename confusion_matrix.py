import matplotlib.pyplot as plt
import numpy as np
import itertools
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# -*- coding: utf-8 -*-

import tensorflow as tf
classifierLoad = tf.keras.models.load_model('model.h5')
import numpy as np
import os
import matplotlib.pyplot as plt
from keras_preprocessing.image import load_img
folder_dir = "INbreast-MIAS-DDSM-Dataset-Testing/"
cancer_or_normal = ['Benign Masses','Malignant Masses']
test_accuraccy_per_folder = []
total_sample = 0


# def accuraccy_test_manually():
#     total_sample=0
#     for image_ in cancer_or_normal:
#         temp = 0
#         print(folder_dir + image_)
#         for image1_ in os.listdir(folder_dir + image_)[:100]:
#             test_image = load_img(folder_dir + image_ +"/"+image1_ , target_size=(200, 200))
#             test_image = np.expand_dims(test_image, axis=0)
#             result = classifierLoad.predict(test_image)
#             print(cancer_or_normal.index(image_))
#             if result[0][cancer_or_normal.index(image_)] == 1:
#                 temp += 1
#             total_sample += 1
#         test_accuraccy_per_folder.append(temp)
#     print(sum(test_accuraccy_per_folder),test_accuraccy_per_folder,total_sample)
#     final_accuracy = ((sum(test_accuraccy_per_folder)) / total_sample) * 100
#     print(final_accuracy)  # 86.40
#
#     accuraccy = [88.70, final_accuracy]
#     title = ["Training", "Testing"]
#     c = ['green', 'red']
#     plt.bar(title, height=accuraccy, color=c)
#     plt.title('Title')
#     plt.xlabel('Training_vs_Testing')
#     plt.ylabel('Accuraccy in %')
#     plt.show()


def fun_confusion_matrix():
    actual_values=[]
    predicted_values=[]
    for dir_ in cancer_or_normal:
        for image_ in os.listdir(folder_dir + dir_ + "/")[:100]:
            test_image = load_img(folder_dir + dir_ + "/" + image_, target_size=(200, 200))
            test_image = np.expand_dims(test_image, axis=0)
            result = classifierLoad.predict(test_image)
            actual_values.append(cancer_or_normal.index(dir_))
            if result[0][0] == 1:
                predicted_values.append(0)
            elif result[0][1] == 1:
                predicted_values.append(1)
    return actual_values,predicted_values



def plot_confusion_matrix(cm, target_names, title='Confusion matrix', cmap=None, normalize=False):
    """
    arguments
    ---------
    cm:           confusion matrix from sklearn.metrics.confusion_matrix

    target_names: given classification classes such as [0, 1, 2]
                  the class names, for example: ['high', 'medium', 'low']

    title:        the text to display at the top of the matrix

    cmap:         the gradient of the values displayed from matplotlib.pyplot.cm
                  see http://matplotlib.org/examples/color/colormaps_reference.html

    normalize:    If False, plot the raw numbers
                  If True, plot the proportions
    """

    if cmap is None:
        cmap = plt.get_cmap('Oranges')

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylim(len(target_names) - 0.5, -0.5)
    plt.ylabel('True labels')
    plt.xlabel('Predicted labels')
    plt.savefig(title + '.png', dpi=500, bbox_inches='tight')
    plt.show()



def plot_accuraccy(train,test):
    accuraccy=[train,test]
    title = ["Training", "Testing"]
    c = ['green', 'red']
    plt.bar(title, height=accuraccy, color=c)
    plt.title('Title')
    plt.xlabel('Training_vs_Testing')
    plt.ylabel('Accuraccy in %')
    plt.show()
    plt.savefig('accuraccy.png')



y_true,y_pred = fun_confusion_matrix()
y_true=y_true[:len(y_pred)]
correct_predicted=0
for i in range(len(y_true)):
    if y_pred[i] == y_true[i]:
        correct_predicted=correct_predicted+1
print("Total Number of testing sample:",len(y_true))
print("Total Number of correct prediction: ",correct_predicted)
print("Testing accuracy: "+str((correct_predicted/len(y_true))*100)+"%")
plot_accuraccy(88.70, (correct_predicted/len(y_true))*100)

confusion_martix_value = confusion_matrix(y_true, y_pred)
print(confusion_martix_value)

# a tuple for all the class names
target_names = ('Benign Masses','Malignant Masses')
print(classification_report(y_true, y_pred, target_names=target_names))
print(classification_report(y_true, y_pred, labels=[1, 2, 3]))
plot_confusion_matrix(confusion_martix_value, target_names, title='Confusion matrix')






