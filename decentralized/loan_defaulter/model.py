# Tensorflow Library Dependencies
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Dense,
    Dropout,
    Input,
)

def model_arch():
    model = Sequential()

    # input layer
    model.add(Input(117))
    print("[MODEL] After input layer")

    # hidden layer
    model.add(Dense(59, activation="relu"))
    model.add(Dropout(0.1))
    print("[MODEL] After 1st hidden layer")

    # hidden layer
    model.add(Dense(30, activation="relu"))
    model.add(Dropout(0.1))
    print("[MODEL] After 2nd hidden layer")

    # hidden layer
    model.add(Dense(15, activation="relu"))
    model.add(Dropout(0.1))
    print("[MODEL] After 3rd hidden layer")

    # output layer
    model.add(Dense(1, activation="sigmoid"))
    print("[MODEL] After output layer")

    # Compile model
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    print("[MODEL] After model.compile")

    return model