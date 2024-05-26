# ----------------------------------------------------------------------
# This file is for the creation and training of the artificial neural network. It is trained to be a binary
# classifier based on the feature vectors processed from our data.
# ----------------------------------------------------------------------

import numpy as np
from keras.layers import Dense
from keras.models import Sequential, load_model
from keras.optimizers import Adam


X_train = np.load('DATASETS/X_train.npy')
X_test = np.load('DATASETS/X_test.npy')
X_validation = np.load('DATASETS/X_validation.npy')

y_train = np.load('DATASETS/y_train.npy')
y_test = np.load('DATASETS/y_test.npy')
y_validation = np.load('DATASETS/y_validation.npy')



def create_model():
    model = Sequential()
    model.add(Dense(64, activation='relu', input_dim=6))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer=Adam(lr=0.001), loss='binary_crossentropy', metrics=['accuracy'])
    return model


model = create_model()

model.fit(X_train, y_train, epochs=5, batch_size=4, validation_data=(X_validation, y_validation))


model.summary()

model.save('ANN/prop_model.h5')

prop_model = load_model('ANN\\prop_model.h5')
prop_model.summary()

#loss, accuracy = model.evaluate(X_test, y_test)
#print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')
