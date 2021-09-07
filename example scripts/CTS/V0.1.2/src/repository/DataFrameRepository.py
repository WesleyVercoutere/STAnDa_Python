from pandas import DataFrame


class DataFrameRepository:

    def __init__(self):
        self._rawData = DataFrame()
        self._filteredData = DataFrame()

    def setRawData(self, data: DataFrame):
        self._rawData = data

    def getRawData(self):
        return self._rawData

    def setFilteredData(self, data: DataFrame):
        self._filteredData = data

    def getFilteredData(self):
        return self._filteredData
