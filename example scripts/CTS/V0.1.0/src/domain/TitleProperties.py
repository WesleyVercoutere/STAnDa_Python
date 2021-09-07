class TitleProperties:

    def __init__(self):
        self.__totalFFT = 0
        self.__usedFFT = 0

    @property
    def totalFFT(self):
        return self.__totalFFT

    @totalFFT.setter
    def totalFFT(self, value):
        self.__totalFFT = value

    @property
    def usedFFT(self):
        return self.__usedFFT

    @usedFFT.setter
    def usedFFT(self, value):
        self.__usedFFT = value
