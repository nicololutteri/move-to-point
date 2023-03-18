import tensorflow as tf
import numpy as np

from model import *
from utilities import utilities

gpus = tf.config.experimental.list_physical_devices("GPU")
if gpus:
  try:
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
  except RuntimeError as e:
    print(e)

class computeria():
    def __init__(self):
        self.m = None
        return

    def __init__(self, filename):
        # Load IA

        self.m = model.loadmodel(filename)
        return

    def importmodel(self, m):
        self.m = m
        return

    def move(self, g : gameengine):
        return model.predict_one(self.m, g.matrixforIA())
