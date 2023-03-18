from os import system

from gameengine import gameengine
from computeria import computeria
from utilities import utilities

if __name__ == "__main__":
    g = gameengine()
    ia = computeria("model100.ckpt")

    win = 0
    lost = 0

    while True:
        system("title " + str(win) + "/" + str(win + lost))

        g.reset()
        print(utilities.printStatusNonTrain(g.me, g.objective, -1, -1))
    
        done = False

        step = 0
        while not done:
            step = step + 1

            if step > 100:
                lost = lost + 1
                break

            action = ia.move(g)
            done = g.move(action)
            if done:
                win = win + 1

            print(utilities.printStatus(g.me, g.objective, action, -1))

    exit(0)
