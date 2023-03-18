from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
import numpy as np

from gameengine import gameengine

class model(object):
    @staticmethod
    def create_model(input_size, output_size, hidden_layer_size, hidden_layer_number):
        model = Sequential()
        
        model.add(Dense(hidden_layer_size, input_dim = input_size, activation="relu"))
        for i in range(hidden_layer_number - 1):
            model.add(Dense(hidden_layer_size, activation="relu"))
        model.add(Dense(output_size, activation="linear"))

        model.compile(loss="mean_squared_error", optimizer="adam")
        return model

    @staticmethod
    def loadmodel(name):
        return tf.keras.models.load_model(name)

    @staticmethod
    def predict_one(neural_network, state):
        return np.argmax(neural_network.predict(state))

    @staticmethod
    def predict_view(neural_network, state):
        return neural_network.predict(state)[0]

    @staticmethod
    def predict_gameReal(neural_network, matrix, g):
        list = []
        v = neural_network.predict(matrix)[0]
        
        for x in range(7):
            list.append((x, v[x]))

        list.sort(key=lambda tup: tup[1], reverse=True)

        for x in range(len(list)):
            if (g.legalmove(list[x][0])):
                return list[x][0]
        
        raise Exception()
