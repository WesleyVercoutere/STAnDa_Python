import statistics
from datetime import datetime

import numpy as np

from src.domain.Settings import Settings
from src.domain.TitleProperties import TitleProperties
from src.repository.DataFrameRepository import DataFrameRepository


class DataService:

    def __init__(self, settings: Settings, titleProps: TitleProperties, dataFrameRepo: DataFrameRepository):
        self._settings = settings
        self._titleProps = titleProps
        self._dataRepo = dataFrameRepo

    def addRawData(self, data):
        # only for debugging
        # pd.set_option('display.max_columns', None)
        # print(data)

        self._dataRepo.setRawData(data)

    def processData(self):
        data = self._dataRepo.getRawData()

        self._addDateTime(data)
        self._addAvgTpm(data)
        self._addAvgFFT(data)

        data.sort_values(by=['time'], inplace=True)
        data.reset_index(drop=True)

        filteredData = data.filter(["time", "tpm", "V", "fft"])

        print(filteredData)

        self._dataRepo.setFilteredData(filteredData)

    def getRawData(self):
        return self._dataRepo.getRawData()

    def getFilteredData(self):
        return self._dataRepo.getFilteredData()

    def _addDateTime(self, data):
        data["time"] = data.apply(lambda x: self._calculateDateTime(x['DT']), axis=1)

    def _calculateDateTime(self, dt):
        try:
            return datetime.strptime(dt, '%Y-%m-%d-%H:%M:%S.%f')

        except Exception as e:
            print(f"Wrong date time format, {dt}")
            print(e)
            print()

    def _addAvgTpm(self, data):
        data["tpm"] = data.apply(lambda x: self._calculateAverageTpm(x), axis=1).reset_index(drop=True)

    def _addAvgFFT(self, data):
        data["fft"] = data.apply(lambda x: self._calculateAverageFFT(x), axis=1).reset_index(drop=True)

    def _calculateAverageTpm(self, row):
        values = []
        prefixFreq = "f"
        prefixFFT = "FT"

        for i in range(self._settings.nbrOfSections):

            if self._settings.sectionMask[i]:
                if row["V"] != "Unknown":
                    self._titleProps.totalFFT += 1

                if row[f"{prefixFFT}{i + 1}"] > self._settings.minFFT:
                    if row["V"] != "Unknown":
                        self._titleProps.usedFFT += 1

                    values.append(row[f"{prefixFreq}{i + 1}"])

        if len(values) > 0 and row["mmin"] > 0:
            return statistics.mean(values) / row["mmin"]

        return np.nan

    def _calculateAverageFFT(self, row):
        values = []
        prefixFFT = "FT"

        for i in range(self._settings.nbrOfSections):

            if self._settings.sectionMask[i]:

                if row[f"{prefixFFT}{i + 1}"] > self._settings.minFFT:
                    values.append(row[f"{prefixFFT}{i + 1}"])

        if len(values) > 0:
            return statistics.mean(values)

        return 0

