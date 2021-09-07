class OutputValues:

    def __init__(self):
        self.__averageAll = 0
        self.__averageStart = 0
        self.__average15 = 0
        self.__average15All = 0

        self.__medianAll = 0
        self.__medianStart = 0
        self.__median15 = 0
        self.__median15All = 0

    @property
    def averageAll(self):
        return self.__averageAll

    @averageAll.setter
    def averageAll(self, value):
        self.__averageAll = value

    @property
    def averageStart(self):
        return self.__averageStart

    @averageStart.setter
    def averageStart(self, value):
        self.__averageStart = value

    @property
    def average15(self):
        return self.__average15

    @average15.setter
    def average15(self, value):
        self.__average15 = value

    @property
    def average15All(self):
        return self.__average15All

    @average15All.setter
    def average15All(self, value):
        self.__average15All = value

    @property
    def medianAll(self):
        return self.__medianAll

    @medianAll.setter
    def medianAll(self, value):
        self.__medianAll = value

    @property
    def medianStart(self):
        return self.__medianStart

    @medianStart.setter
    def medianStart(self, value):
        self.__medianStart = value

    @property
    def median15(self):
        return self.__median15

    @median15.setter
    def median15(self, value):
        self.__median15 = value

    @property
    def median15All(self):
        return self.__median15All

    @median15All.setter
    def median15All(self, value):
        self.__median15All = value
