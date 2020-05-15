# -*- coding: utf-8 -*-
"""Image_Classification_HNSV_NN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14vwwiGFf6i-E9Ue_5c1jwY8giBozaMMj
"""



"""*Acknowledgement*

Yuval Netzer, Tao Wang, Adam Coates, Alessandro Bissacco, Bo Wu, Andrew Y. Ng Reading Digits in Natural Images with Unsupervised Feature Learning NIPS Workshop on Deep Learning and Unsupervised Feature Learning 2011. PDF

*URL*
http://ufldl.stanford.edu/housenumbers

STREET VIEW HOUSE NUMBERS

* DATA HAS BEEN OBTAINED FROM HOUSE NUMBERS IN GOOGLE STREET VIEW IMAGES
"""



"""IMAGES COME IN TWO FORMATS

1. ORIGINAL IMAGES:
  * CHARACTER LEVEL BOUNDING BOXES
  

2. 32 X 32 IMAGES
  * CENTERED AROUND SINGLE CHARACTER
"""



"""KEY FOCUS

* SIMPLE IMAGE CLASSIFICATION
* K-NEAREST NEIGHBOUR
* DEEP NEURAL NETWORK
"""

### MOUNT GOOGLE DRIVE
from google.colab import drive
drive.mount('/content/drive')

### WORKING DIRECTORY
import os

os.chdir('/content/drive/My Drive/GL/Introduction to Neural Networks/')
path = '.'

ls

### ACCESS DATA IN .H5 FILE
### IMPORT H5PY PACKAGE 
import h5py
import numpy as np

### OPEN FILE: READ ONLY
h5f = h5py.File('/content/drive/My Drive/GL/Introduction to Neural Networks/SVHN_single_grey1.h5', 'r')

### LOAD: TRAIN & TEST SETS
X_train = h5f['X_train'][:]
y_train1 = h5f['y_train'][:]
X_test = h5f['X_test'][:]
y_test1 = h5f['y_test'][:]

### CLOSE FILE
h5f.close()

### LIBRARIES
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils

### FIX RANDOM SEED: REPRODUCIBILITY 
seed = 7
np.random.seed(seed)

# Commented out IPython magic to ensure Python compatibility.
### VISUALIZE
### FIRST TEN IMAGES
### LABELS

# %matplotlib inline
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 1))
for i in range(10):
    plt.subplot(1, 10, i+1)
    plt.imshow(X_train[i], cmap="gray")
    plt.axis('off')
plt.show()
print('label for each of the above image: %s' % (y_train1[0:10]))

X_train = X_train.reshape(X_train.shape[0], 1024)
X_test = X_test.reshape(X_test.shape[0], 1024)

### NORMALIZE INPUTS
### 0-255 TO 0-1 
X_train = X_train / 255.0
X_test = X_test / 255.0

print('Training set', X_train.shape, y_train1.shape)
print('Test set', X_test.shape, y_test1.shape)

print(X_test.shape)
print(y_test1.shape)

### ONE HOT ENCODING - OUTPUTS
y_train = np_utils.to_categorical(y_train1)
y_test = np_utils.to_categorical(y_test1)

### NUMBER OF CLASSES
num_classes = y_test.shape[1]
num_hidden = 32

num_classes

x_tr = []
for i in range(42000):
    x_tr.append(X_train[i,:].flatten())
x_te = []
for i in range(18000):
    x_te.append(X_test[i,:].flatten())

x_tr =x_tr[:2000]
x_te =x_te[:2000]

y_tr = y_train1[0:2000]
y_te = y_test1[0:2000]

print(len(x_tr))
print(len(y_tr))
print(len(x_te))
print(len(y_tr))

a =[]
j = []
def knnvalue(k):
    from sklearn.neighbors import KNeighborsClassifier
    NNH = KNeighborsClassifier(n_neighbors= k , weights = 'uniform', metric='euclidean')
    NNH.fit(x_tr, y_tr)
    predicted_labels = NNH.predict(x_te)
    from sklearn.metrics import accuracy_score
    ascore = accuracy_score(y_te, predicted_labels)
    MSE = 1-ascore
    a.append(MSE)
    j.append(k)
    print(ascore)

for i in range(1,30,2):
    knnvalue(i)

### TRAIN MODEL: K VALUE 30
### PRINT METRICS

from sklearn.neighbors import KNeighborsClassifier
NNH = KNeighborsClassifier(n_neighbors= 11 , weights = 'uniform', metric='euclidean')
NNH.fit(x_tr, y_tr)
pred=NNH.predict(x_te)

pred[0]

y_test1[0]

### CONFUSION MATRIX
from sklearn.metrics import confusion_matrix

confusion_matrix(pred,y_te)

# KNN MODEL ACCURACY: POOR

#### NEURAL NETWORK MODEL ####

from keras.layers import BatchNormalization

### DEFINE MODEL

import keras
from keras import losses
from keras import optimizers
from keras.layers import Dropout, MaxPooling2D



### CREATE MODEL
def nn_model():

    model = Sequential()  

    ### BATCH_NORM LAYER
    model.add(BatchNormalization(input_shape = (1024,)))  
    
    ### DENSE UNITS
    ### RELU ACTIVATION
    model.add(Dense(256, activation='relu')) 
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    
    ### ADAM OPTIMIZER
    sgd = optimizers.Adam(lr=1e-3)
    
    ### COMPILE MODEL
    ### LOSS FUNCTION: CATEGORICAL_CROSSENTROPY
    model.compile(loss=losses.categorical_crossentropy, optimizer=sgd, metrics=['accuracy']) 
    return model

### MODEL
model = nn_model()

### FIT MODEL
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=30, batch_size=200, verbose=2)

### EVALUATE MODEL
scores = model.evaluate(X_test, y_test, verbose=0)

print("Error: %.2f%%" % (100-scores[1]*100))

### MODEL SUMMARY
model.summary()

"""CONCLUSION

* DEEP LEARNING MODEL SUCCEEDED IN WORKING WITH HUGE AMOUNTS OF DATA 
* DEEP LEARNING MODEL SUCCEEDED IN WORKING WITH MULTI-DIMENTIONAL DATA
* DEEP LEARNING PERFORMED VASTLY BETTER THAN KNN MODEL
"""