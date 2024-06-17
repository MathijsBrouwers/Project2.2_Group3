# ----------------------------------------------------------------------
# This file is for the creation and training of the artificial neural network with slight modification. This one
# eliminated the last feature entirely and saves the resulting ann under a different name. Used by running the file.
# ----------------------------------------------------------------------

import numpy as np
from keras.layers import Dense
from keras.models import Sequential, load_model
from keras.optimizers import Adam
from sklearn.metrics import precision_score, recall_score


X_train = np.load('DATASETS/X_train.npy')
X_test = np.load('DATASETS/X_test.npy')
X_validation = np.load('DATASETS/X_validation.npy')

y_train = np.load('DATASETS/y_train.npy')
y_test = np.load('DATASETS/y_test.npy')
y_validation = np.load('DATASETS/y_validation.npy')


X_train = X_train[:, :-1]
X_test = X_test[:, :-1]
X_validation = X_validation[:, :-1]



def create_model():
    model = Sequential()
    model.add(Dense(64, activation='relu', input_dim=5, name="HiddenLayer"))
    model.add(Dense(1, activation='sigmoid', name = "OutputLayer"))
    model.compile(optimizer=Adam(lr=0.001), loss='binary_crossentropy', metrics=['accuracy'])
    return model


model = create_model()

model.fit(X_train, y_train, epochs=5, batch_size=4, validation_data=(X_validation, y_validation))



model.save('ANN/prop_weight_model.h5')

