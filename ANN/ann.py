import random
from collections import deque

import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam


class Network(Sequential):
    def __init__(self):
        super(Network, self).__init__()
        self.add(Dense(64, activation='relu', input_dim=5))
        self.add(Dense(1, activation='sigmoid'))
        self.compile(optimizer=Adam(lr=0.001), loss='binary_crossentropy', metrics=['accuracy'])
