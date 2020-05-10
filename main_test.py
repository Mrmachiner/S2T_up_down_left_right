import time

from sklearn.preprocessing import LabelEncoder

import nn

a = time.time()
print("Extracting features..")


le_test = LabelEncoder()
#1: back 2:left 3:right 4:stop 5:up 6:unknow
le_test.fit([1, 2, 3, 4, 5, 6])
# predicting using trained model with any test file in dataset
nn.predict("/home/minhhoang/Downloads/Lonton_STT/demo1.6955733272881335.ogg", le_test, "trained_cnn.h5")
print("time runcode:", time.time() - a)

