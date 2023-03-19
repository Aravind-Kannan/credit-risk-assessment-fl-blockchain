# Tensorflow Library Dependencies
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Dense,
    Dropout,
    Input,
    BatchNormalization,
)
from keras.optimizers import SGD
import warnings



def model_arch():
    warnings.filterwarnings("ignore")
    print("Started Model Building")
    model = Sequential()

    # input layer
    model.add(Input(105))
    # print("after input layer")

    # hidden layer
    model.add(BatchNormalization())
    model.add(Dense(53,  activation = 'relu'))
    model.add(Dropout(0.1))
    # print("after 1st hidden layer")

    # hidden layer
    model.add(BatchNormalization())
    model.add(Dense(27, activation='relu'))
    model.add(Dropout(0.1))
    # print("after 2nd hidden layer")

    # hidden layer
    model.add(BatchNormalization())
    model.add(Dense(14, activation='relu'))
    model.add(Dropout(0.1))
    # print("after 3rd hidden layer")

    # output layer
    model.add(Dense(1, activation="sigmoid"))
    print("Model is build")

    opt = SGD(learning_rate=0.00001)
    # Compile model
    model.compile(optimizer=opt, loss="binary_crossentropy", metrics=["accuracy"])
    # print("[MODEL] After model.compile")

    return model
