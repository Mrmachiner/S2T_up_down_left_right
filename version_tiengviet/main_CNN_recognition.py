import time

from sklearn.preprocessing import LabelEncoder

import nn_CNN_recognition as nn

a = time.time()
print("Extracting features..")


le_test = LabelEncoder()
le_test.fit([1, 2, 3, 4, 5, 6])
# predicting using trained model with any test file in dataset
nn.predict("dataSet/Back/demo9.484276840927278.wav.ogg", le_test, "trained_cnn.h5")
print("time runcode:", time.time() - a)

