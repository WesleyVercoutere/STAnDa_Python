class OutputValues:

    def __init__(self):
        self.__averages = []
        self.__medians = []

    def getAverages(self):
        return self.__averages

    def getMedians(self):
        return self.__medians

    def appendAverage(self, val):
        self.__averages.append(val)

    def appendMedian(self, val):
        self.__medians.append(val)
