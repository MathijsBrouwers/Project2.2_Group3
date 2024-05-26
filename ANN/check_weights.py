
from keras.models import load_model
import numpy as np
from sklearn.metrics import precision_score, recall_score

X_test = np.load('DATASETS/X_test.npy')
y_test = np.load('DATASETS/y_test.npy')


prop_model = load_model('ANN\\prop_model.h5')

for layer in prop_model.layers:
    weights = layer.get_weights()  # List of numpy arrays
    print(f"Layer: {layer.name}")
    print(f"Weights: {weights[0]}")  # Weight matrix
    if len(weights) > 1:
        print(f"Biases: {weights[1]}")  # Bias vector