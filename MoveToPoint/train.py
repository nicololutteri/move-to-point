import matplotlib.pyplot as plt 
import tensorflow as tf
import numpy as np
from timeit import default_timer as timer
from tqdm import tqdm as tqdm
from collections import deque
from os import system
import os

from memory import *
from model import model
from gameengine import gameengine
from utilities import *

BATCH_SIZE = 32
EPISODES = 1000
EPOCHS = 8

INPUT_NUMBER = 4
OUTPUT_NUMBER = 4

FOLDER = "data"

gpus = tf.config.experimental.list_physical_devices("GPU")
if gpus:
  try:
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
  except RuntimeError as e:
    print(e)

os.environ['TF_ENABLE_AUTO_MIXED_PRECISION'] = '1'

def train_model(model, memory, gamma=0.995):
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

def DQN(neural_network, trials, epsilon_decay=0.95):
    epsilon = 1.0
    #epsilon = 0.1
    epsilon_min = 0.01 
    
    memory = deque(maxlen=10000)
    score_queue = deque()

    m = model()

    f = open(os.path.join(FOLDER, "log.txt"), "w")

    win = 0
    loss = 0
    for trial in range(trials):
        g = gameengine()
        #g.set(1, 1, 9, 9)

        done = False
        score = 0
        step = 0

        trialfile = open(os.path.join(FOLDER, str(trial) + ".txt"), "w+")
        trialfile.write(str(g.me[0]) + "-" + str(g.me[1]) + ";" + str(g.objective[0]) + "-" + str(g.objective[1]) + "\n\n")

        prevlist = list()

        epsilon *= epsilon_decay
        epsilon = max(epsilon_min, epsilon)

        while not done:
            if np.random.random() < epsilon:
                action = g.getmoverandom()
            else:
                action = m.predict_one(neural_network, g.matrixforIA())

            prev = g.me
            prevlist.append(prev)

            state1 = g.matrixforIA()
            done = g.move(action)

            state_next = g.matrixforIA()
            reward = -1

            if g.me[0] == -1 or g.me[0] == 10 or g.me[1] == -1 or g.me[1] == 10:
                raise Exception()

            print(utilities.printArray(prev, g.me, action, reward))
            trialfile.write(utilities.printStatus(prev, g.me, action, reward) + "\n")

            memory.append([state1, action, state_next, reward, done]) 
            
            state1 = state_next

            score += reward
            step = step + 1

            if step > 100:
                break

        if done:
            win = win + 1

        if trial % 1000 == 0:
            neural_network.save(os.path.join(FOLDER, "model" + str(trials) + "-" + str(trial)))

        trialfile.close()

        print(trial, score, epsilon, loss)
        score_queue.append(score)

    neural_network, loss = train_model(neural_network, memory)
    #memory.clear()

    f.close()

    return neural_network, score_queue

def main():
    neural_network = model.create_model(INPUT_NUMBER, OUTPUT_NUMBER, 32, 2)
    neural_network, score = DQN(neural_network, trials=EPISODES) 

    #Save model
    save_path = neural_network.save(name)
    
    file1 = open(os.path.join(FOLDER, "score.txt"), "w")
    for x in score:
        file1.write(str(x) + "\n")
    file1.close()

if __name__ == "__main__":
    main()
