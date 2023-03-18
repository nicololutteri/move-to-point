from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
import tensorflow as tf
import numpy as np
from collections import deque

gpus = tf.config.experimental.list_physical_devices("GPU")
if gpus:
  try:
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
  except RuntimeError as e:
    print(e)

os.environ['TF_ENABLE_AUTO_MIXED_PRECISION'] = '1'

class boxia(object):

    def __init__(self, name : str, input_size : int, output_size : int, hidden_layer_size : int, hidden_layer_number : int, batch_size : int, episodes : int, epsilon_min : float, epsilon : float, gamma : float, train_after : int):
        self.name = name
        
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_layer_size = hidden_layer_size
        self.hidden_layer_number = hidden_layer_number

        self.batch_size = batch_size
        self.episodes = episodes

        self.epsilon_min = epsilon_min
        self.epsilon = epsilon

        self.gamma = gamma

        self.train_after = train_after

        self.create_model(self.input_size, self.output_size, self.hidden_layer_size, self.hidden_layer_number)
        memory = deque(maxlen=10000)

    def load_model(self, filename) -> bool:
        self.m = tf.keras.models.load_model(name)
        return True

    def save_model(self, filename) -> bool:
        self.m.save(filename)
        return True

    def create_model(self, input_size : int, output_size : int, hidden_layer_size : int, hidden_layer_number : int):
        model = Sequential()
        
        model.add(Dense(hidden_layer_size, input_dim = input_size, activation="relu"))
        for i in range(hidden_layer_number - 1):
            model.add(Dense(hidden_layer_size, activation="relu"))
        model.add(Dense(output_size, activation="linear"))

        model.compile(loss="mean_squared_error", optimizer="adam")
        self.m = model

    def train_model(self, model, memory, gamma=0.95):
        batch_size = BATCH_SIZE
    
        memory_sample = random.sample(memory, min(len(memory), batch_size))

        for batch in memory_sample:
            if len(batch) == 1: 
                batch = batch[0]
        
            s, a, s1, r, done = batch

            target = model.predict(np.array(s).reshape(1,INPUT_NUMBER))[0]
        
            if done:
                target[a] = r
            else:
                maxq = max(model.predict(np.array(s1).reshape(1,INPUT_NUMBER))[0])
                target[a] = r + (maxq * gamma)

            model.fit(s, np.array([target]), epochs=EPOCHS, verbose=0)  
 
        loss = model.evaluate(s, np.array([target]), verbose=0)
        return model, loss

    def predict_one(self, state):
        return np.argmax(self.m.predict(state))

    def predict_view(self, state):
        return self.m.predict(state)[0]

    def add_memory(self, value : (state1, action, state_next, reward, done)):
        self.memory.append(value)

        if len(self.memory) == self.train_after:
            self.m = train_model(self.m, self.memory, self.gamma)
            self.memory.clear()
