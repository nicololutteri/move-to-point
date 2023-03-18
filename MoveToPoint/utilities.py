class utilities(object):

    @staticmethod
    def printArray(point1 : (int, int), point2 : (int, int), action : int, reward : int) -> str:
        return str(point1[0]) + "-" + str(point1[1]) + ";" + str(point2[0]) + "-" + str(point2[1]) + ";" + str(action) + ";" + str(reward)

    @staticmethod
    def printStatus(point1 : (int, int), point2 : (int, int), action : int, reward : int) -> str:
        return str(point1[0]) + "-" + str(point1[1]) + ";" + str(point2[0]) + "-" + str(point2[1]) + ";" + str(action) + ";" + str(reward)

    @staticmethod
    def printStatusNonTrain(point1 : (int, int), point2 : (int, int), action : int) -> str:
        return str(point1[0]) + "-" + str(point1[1]) + ";" + str(point2[0]) + "-" + str(point2[1]) + ";" + str(action)
