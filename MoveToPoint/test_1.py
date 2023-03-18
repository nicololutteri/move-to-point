import unittest
from gameengine import gameengine

class Test_test_1(unittest.TestCase):
    def test_move_1(self):
        g = gameengine()
        g.set(1, 1, 9, 9)
        g.move(0)

        self.assertTrue(g.me[0] == 1, g.me[1] == 0)

    def test_move_2(self):
       g = gameengine()
       g.set(1, 1, 9, 9)
       g.move(1)

       self.assertTrue(g.me[0] == 1, g.me[1] == 2)

    def test_move_3(self):
        g = gameengine()
        g.set(1, 1, 9, 9)
        g.move(2)

        self.assertTrue(g.me[0] == 0, g.me[1] == 1)

    def test_move_4(self):
        g = gameengine()
        g.set(1, 1, 9, 9)
        g.move(3)

        self.assertTrue(g.me[0] == 2, g.me[1] == 1)

    def test_reward_1(self):
        g = gameengine()
        g.set(1, 1, 9, 9)
        g.move(0)

        r = g.distance((1, 1), [])
        self.assertTrue(r == -1)

    def test_reward_2(self):
        g = gameengine()
        g.set(1, 1, 9, 9)
        g.move(1)

        r = g.distance((1, 1), [])
        self.assertTrue(r == +1)

if __name__ == '__main__':
    unittest.main()
