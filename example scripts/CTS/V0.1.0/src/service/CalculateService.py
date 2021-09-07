from datetime import datetime, timedelta

from pandas import DataFrame

from src.domain.ChartItem import ChartItem
from src.domain.OutputValues import OutputValues
from src.domain.Settings import Settings
from src.repository.ChartItemRepository import ChartItemRepository
from src.service.DataService import DataService
from src.service.OutputService import OutputService


class CalculateService:

    def __init__(self, settings: Settings, dataService: DataService, chartItemRepo: ChartItemRepository, outputService: OutputService):
        self._settings = settings
        self._dataService = dataService
        self._chartItemRepo = chartItemRepo
        self._outputService = outputService

        self._values = []

    def processData(self):
        [self._process(item) for item in self._chartItemRepo.getAll()]
        self._outputService.output(self._values)

    def _process(self, chartItem: ChartItem):
        df = chartItem.dfSignalData

        val = OutputValues()
        self._values.append(val)

        self._calculateAll(df, val)
        self._calculateStart(df, val)
        self._calculate15(df, val)
        self._calculate15All(df, val)

    def _calculateAll(self, df: DataFrame, val: OutputValues):
        val.averageAll = df["tpm"].mean()
        val.medianAll = df["tpm"].median()

    def _calculateStart(self, df: DataFrame, val: OutputValues):
        localDf = df.head(self._settings.nbrOfValuesForRefAvg)
        val.averageStart = localDf["tpm"].mean()
        val.medianStart = localDf["tpm"].median()

    def _calculate15(self, df: DataFrame, val: OutputValues):
        localDf = df
        time = localDf._get_value(0, 'time')
        startTime = time + timedelta(minutes=15)
        localDf = localDf.loc[(localDf['time'] >= startTime).idxmax():]
        localDf = localDf.head(self._settings.nbrOfValuesForRefAvg)

        val.average15 = localDf["tpm"].mean()
        val.median15 = localDf["tpm"].median()

    def _calculate15All(self, df: DataFrame, val: OutputValues):
        localDf = df
        time = localDf._get_value(0, 'time')
        startTime = time + timedelta(minutes=15)
        localDf = localDf.loc[(localDf['time'] >= startTime).idxmax():]

        val.average15All = localDf["tpm"].mean()
        val.median15All = localDf["tpm"].median()
