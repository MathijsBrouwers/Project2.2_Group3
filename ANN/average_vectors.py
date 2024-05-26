import numpy as np

X_train = np.load('DATASETS/X_train.npy')
X_test = np.load('DATASETS/X_test.npy')
X_validation = np.load('DATASETS/X_validation.npy')

y_train = np.load('DATASETS/y_train.npy')
y_test = np.load('DATASETS/y_test.npy')
y_validation = np.load('DATASETS/y_validation.npy')

X_all = np.concatenate((X_train, X_test, X_validation), axis=0)
y_all = np.concatenate((y_train, y_test, y_validation), axis=0)

X_class_0 = X_all[y_all == 0]
X_class_1 = X_all[y_all == 1]

avg_vector_class_0 = np.mean(X_class_0, axis=0)
avg_vector_class_1 = np.mean(X_class_1, axis=0)

print("Average vector for class 0:", avg_vector_class_0)
print("Average vector for class 1:", avg_vector_class_1)
