# ----------------------------------------------------------------------
# This file simply checks the precision and recall of the original artificial neural network classifier. To use
# just run the file.
# ----------------------------------------------------------------------

from keras.models import load_model
import numpy as np
from sklearn.metrics import precision_score, recall_score

X_test = np.load('DATASETS/X_test.npy')
y_test = np.load('DATASETS/y_test.npy')


prop_model = load_model('ANN\\prop_model.h5')


y_pred_prob = prop_model.predict(X_test)
y_pred = (y_pred_prob > 0.5).astype(int)

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print(precision)
print(recall)