import random
import math
import numpy as np

class gameengine(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.me = (random.randint(0, 9), random.randint(0, 9))
        self.objective = (random.randint(0, 9), random.randint(0, 9))

        if self.me[0] == self.objective[0] and self.me[1] == self.objective[1]:
            self.reset()

    def set(self, pos1: int, pos2: int, pos3: int, pos4: int):
        self.me = (pos1, pos2)
        self.objective = (pos3, pos4)

    def distance(self, previous: (int, int), prevlist) -> int:
        # E ripassato su un punto che aveva gia visto
        #for x in prevlist:
        #    if self.me[0] == x[0] and self.me[1] == x[1]:
        #        return -2

        if previous[0] == self.me[0] and previous[1] == self.me[1]:
            return -1

        if self.me[0] == self.objective[0] + 1 and self.me[1] == self.objective[1]: 
            return 50
        elif self.me[0] == self.objective[0] - 1 and self.me[1] == self.objective[1]:
            return 50
        elif self.me[0] == self.objective[0] and self.me[1] == self.objective[1] + 1:
            return 50
        elif self.me[0] == self.objective[0] and self.me[1] == self.objective[1] - 1:
            return 50

        if self.objective[0] == self.me[0] and self.objective[1] == self.me[1]:
            return 100

        d1x = abs(self.me[0] - self.objective[0])
        d1y = abs(self.me[1] - self.objective[1])
        
        d2x = abs(previous[0] - self.objective[0])
        d2y = abs(previous[1] - self.objective[1])

        if ((d1x + d1y) > (d2x + d2y)):
            return -1
        else:
            return +1

    def distancetot(self, previous: (int, int), prevlist) -> int:
        d1x = abs(self.me[0] - self.objective[0])
        d1y = abs(self.me[1] - self.objective[1])
        
        d2x = abs(previous[0] - self.objective[0])
        d2y = abs(previous[1] - self.objective[1])

        return (d1x + d1y + d2x + d2y)

    def move(self, pos: int) -> (int, int):
        """
        pos = 0 -> left
        pos = 1 -> right
        pos = 2 -> up
        pos = 3 -> down
        """

        if pos == 0:
            if (self.me[1] - 1 < 0):
                return False
            else:
                self.me = (self.me[0], self.me[1] - 1)
        elif pos == 1:
            if (self.me[1] + 1 >= 10):
                return False
            else:
                self.me = (self.me[0], self.me[1] + 1)
        elif pos == 2:
            if (self.me[0] - 1 < 0):
                return False
            else:
                self.me = (self.me[0] - 1, self.me[1])
        elif pos == 3:
            if (self.me[0] + 1 >= 10):
                return False
            else:
                self.me = (self.me[0] + 1, self.me[1])

        return self.me[0] == self.objective[0] and self.me[1] == self.objective[1]

    def matrixforIA(self) -> int():
        return np.reshape([self.me[0] / 10, self.me[1] / 10, self.objective[0] / 10, self.objective[1] / 10], [1, 4])

    def getmoverandom(self) -> int:
        return random.randint(0, 3)

    def print(self) -> str:
        s = str(self.me[0]) + "," + str(self.me[1]) + " " + str(self.objective[0]) + "," + str(self.objective[1])
        return s
