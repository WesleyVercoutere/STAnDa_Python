from pandas import DataFrame


class ChartItem:

    def __init__(self):
        self.__dfSignalData = DataFrame()
        self.__dfMonitorAvg = DataFrame()
        self.__dfReferenceAvg = DataFrame()
        self.__dfReferenceMed = DataFrame()
        self.__dfMonitorMed1 = DataFrame()
        self.__dfMonitorMed2 = DataFrame()
        self.__dfAvgFFT = DataFrame()

    @property
    def dfSignalData(self):
        return self.__dfSignalData

    @dfSignalData.setter
    def dfSignalData(self, value):
        self.__dfSignalData = value

    @property
    def dfMonitorAvg(self):
        return self.__dfMonitorAvg

    @dfMonitorAvg.setter
    def dfMonitorAvg(self, value):
        self.__dfMonitorAvg = value

    @property
    def dfReferenceAVg(self):
        return self.__dfReferenceAvg

    @dfReferenceAVg.setter
    def dfReferenceAVg(self, value):
        self.__dfReferenceAvg = value

    @property
    def dfMonitorMed1(self):
        return self.__dfMonitorMed1

    @dfMonitorMed1.setter
    def dfMonitorMed1(self, value):
        self.__dfMonitorMed1 = value

    @property
    def dfMonitorMed2(self):
        return self.__dfMonitorMed2

    @dfMonitorMed2.setter
    def dfMonitorMed2(self, value):
        self.__dfMonitorMed2 = value

    @property
    def dfReferenceMed(self):
        return self.__dfReferenceMed

    @dfReferenceMed.setter
    def dfReferenceMed(self, value):
        self.__dfReferenceMed = value

    @property
    def dfAvgFFT(self):
        return self.__dfAvgFFT

    @dfAvgFFT.setter
    def dfAvgFFT(self, value):
        self.__dfAvgFFT = value
