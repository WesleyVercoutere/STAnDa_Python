import numpy as np

from src.domain.ChartItem import ChartItem
from src.domain.Settings import Settings
from src.repository.ChartItemRepository import ChartItemRepository
from src.service.DataService import DataService


class ChartItemService:

    def __init__(self, settings: Settings, dataService: DataService, chartItemRepo: ChartItemRepository):
        self._settings = settings
        self._dataService = dataService
        self._chartItemRepo = chartItemRepo

    def processData(self):
        [self._splitData(speed) for speed in self._settings.speeds]
        [self._addReferenceAvg(chartItem) for chartItem in self._chartItemRepo.getAll()]
        [self._addMonitorAvg(chartItem) for chartItem in self._chartItemRepo.getAll()]
        [self._addMonitorMed1(chartItem) for chartItem in self._chartItemRepo.getAll()]
        [self._addMonitorMed2(chartItem) for chartItem in self._chartItemRepo.getAll()]

    def getData(self):
        return self._chartItemRepo.getAll()

    def _splitData(self, speed):
        data = self._dataService.getFilteredData()
        chartItem = ChartItem()
        chartItem.dfSignalData = self._groupByArg(data, "V", speed)
        self._chartItemRepo.addItem(chartItem)

    def _groupByArg(self, df, groupByType, name):
        groupBy = df.groupby(df[groupByType])
        return groupBy.get_group(name).reset_index(drop=True)

    def _addReferenceAvg(self, chartItem: ChartItem):
        df = chartItem.dfSignalData.head(self._settings.nbrOfValuesForRefAvg)
        avg = df["tpm"].mean()

        chartItem.dfReferenceAvg = chartItem.dfSignalData.head(1)
        chartItem.dfReferenceAvg = chartItem.dfReferenceAvg.append(chartItem.dfSignalData.tail(1))
        chartItem.dfReferenceAvg = chartItem.dfReferenceAvg.filter(["time"]).reset_index(drop=True)

        chartItem.dfReferenceAvg["avg_tpm"] = avg
        chartItem.dfReferenceAvg["lower_boundary"] = chartItem.dfReferenceAvg["avg_tpm"] * (1 - (self._settings.boundary / 100))
        chartItem.dfReferenceAvg["upper_boundary"] = chartItem.dfReferenceAvg["avg_tpm"] * (1 + (self._settings.boundary / 100))

    def _addMonitorAvg(self, chartItem: ChartItem):
        chartItem.dfMonitorAvg = chartItem.dfSignalData.tail(len(chartItem.dfSignalData.index) - self._settings.nbrOfValuesForRefAvg)
        chartItem.dfMonitorAvg["avg_tpm"] = chartItem.dfMonitorAvg["tpm"].rolling(window=self._settings.nbrOfValuesForMonAvg).mean()
        chartItem.dfMonitorAvg = chartItem.dfMonitorAvg[::self._settings.nbrOfValuesForMonAvg]

    def _addMonitorMed1(self, chartItem: ChartItem):
        chartItem.dfMonitorMed1 = chartItem.dfSignalData.tail(len(chartItem.dfSignalData.index) - self._settings.nbrOfValuesForRefAvg)
        chartItem.dfMonitorMed1["median"] = chartItem.dfMonitorMed1["tpm"].rolling(window=self._settings.nbrOfValuesForMed1).median()
        chartItem.dfMonitorMed1 = chartItem.dfMonitorMed1[::self._settings.nbrOfValuesForMed1]

    def _addMonitorMed2(self, chartItem: ChartItem):
        chartItem.dfMonitorMed2 = chartItem.dfSignalData.tail(len(chartItem.dfSignalData.index) - self._settings.nbrOfValuesForRefAvg)
        chartItem.dfMonitorMed2["median"] = chartItem.dfMonitorMed2["tpm"].rolling(window=self._settings.nbrOfValuesForMed2).median()
        chartItem.dfMonitorMed2 = chartItem.dfMonitorMed2[::self._settings.nbrOfValuesForMed2]
