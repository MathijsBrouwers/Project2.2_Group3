

import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam


X_train = np.load('DATASETS/X_train.npy')
X_test = np.load('DATASETS/X_test.npy')
X_validation = np.load('DATASETS/X_validation.npy')

y_train = np.load('DATASETS/y_train.npy')
y_test = np.load('DATASETS/y_test.npy')
y_validation = np.load('DATASETS/y_validation.npy')




class Network(Sequential):
    def __init__(self):
        super(Network, self).__init__()
        self.add(Dense(64, activation='relu', input_dim=6))
        self.add(Dense(1, activation='sigmoid'))
        self.compile(optimizer=Adam(lr=0.001), loss='binary_crossentropy', metrics=['accuracy'])


model = Network()

model.fit(X_train, y_train, epochs=5, batch_size=4, validation_data=(X_validation, y_validation))

loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')
