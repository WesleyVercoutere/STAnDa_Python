class Settings:

    def __init__(self, folder, st, nbrOfSections, sectionMask, minFFT, nbrOfValuesForRefAvg, nbrOfValuesForMonAvg, nbrOfValuesForMed1, nbrOfValuesForMed2, boundary):
        self.__folder = folder
        self.__st = st
        self.__nbrOfSections = nbrOfSections
        self.__sectionMask = sectionMask
        self.__minFFT = minFFT
        self.__nbrOfValuesForRefAvg = nbrOfValuesForRefAvg
        self.__nbrOfValuesForMonAvg = nbrOfValuesForMonAvg
        self.__nbrOfValuesForMed1 = nbrOfValuesForMed1
        self.__nbrOfValuesForMed2 = nbrOfValuesForMed2
        self.__boundary = boundary
        self.speeds = ("Turtle", "Buffer", "Full")

    @property
    def folder(self):
        return self.__folder

    @property
    def st(self):
        return self.__st

    @property
    def nbrOfSections(self):
        return self.__nbrOfSections

    @property
    def sectionMask(self):
        return self.__sectionMask

    @property
    def minFFT(self):
        return self.__minFFT

    @property
    def nbrOfValuesForRefAvg(self):
        return self.__nbrOfValuesForRefAvg

    @property
    def nbrOfValuesForMonAvg(self):
        return self.__nbrOfValuesForMonAvg

    @property
    def nbrOfValuesForMed1(self):
        return self.__nbrOfValuesForMed1

    @property
    def nbrOfValuesForMed2(self):
        return self.__nbrOfValuesForMed2

    @property
    def boundary(self):
        return self.__boundary
