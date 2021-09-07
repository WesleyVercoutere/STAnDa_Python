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

        self._calculateRefStart(df, val)
        self._calculateAll(df, val)
        self._calculateRef15(df, val)
        self._calculateAll15(df, val)

        self._calculateRefStartDay2(df, val)
        self._calculateAllDay2(df, val)
        self._calculateRef15Day2(df, val)
        self._calculateAll15Day2(df, val)

    '''
    volgorde items in array
        0 : average/mediaan eerste 50 samples
        1 : average/mediaan alle samples
        2 : average/mediaan eerste 50 samples na 15 minuten
        3 : average/mediaan alle samples na 15 minuten
        4 : average/mediaan eerste 50 samples dag 2
        5 : average/mediaan alle samples dag2
        6 : average/mediaan eerste 50 samples na 15 minuten dag 2
        7 : average/mediaan alle samples na 15 minuten dag 2
    '''

    def _calculateRefStart(self, df: DataFrame, val: OutputValues):
        localDf = df.head(self._settings.nbrOfValuesForRefAvg)
        val.appendAverage(localDf["tpm"].mean())
        val.appendMedian(localDf["tpm"].median())

    def _calculateAll(self, df: DataFrame, val: OutputValues):
        val.appendAverage(df["tpm"].mean())
        val.appendMedian(df["tpm"].median())

    def _calculateRef15(self, df: DataFrame, val: OutputValues):
        localDf = df
        time = localDf._get_value(0, 'time')
        startTime = time + timedelta(minutes=15)
        localDf = localDf.loc[(localDf['time'] >= startTime).idxmax():]
        localDf = localDf.head(self._settings.nbrOfValuesForRefAvg)

        val.appendAverage(localDf["tpm"].mean())
        val.appendMedian(localDf["tpm"].median())

    def _calculateAll15(self, df: DataFrame, val: OutputValues):
        localDf = df
        time = localDf._get_value(0, 'time')
        startTime = time + timedelta(minutes=15)
        localDf = localDf.loc[(localDf['time'] >= startTime).idxmax():]

        val.appendAverage(localDf["tpm"].mean())
        val.appendMedian(localDf["tpm"].median())

    def _getSecondDayDf(self, df):
        time = df._get_value(0, 'time')
        nextDay = time + timedelta(days=1)
        nextDay = nextDay.replace(hour=0, minute=0, second=0, microsecond=0)

        localDf = df.loc[(df['time'] >= nextDay).idxmax():]

        return localDf.reset_index(drop=True)

    def _calculateRefStartDay2(self, df: DataFrame, val: OutputValues):
        localDf = self._getSecondDayDf(df)
        self._calculateRefStart(localDf, val)

    def _calculateAllDay2(self, df: DataFrame, val: OutputValues):
        localDf = self._getSecondDayDf(df)
        self._calculateAll(localDf, val)

    def _calculateRef15Day2(self, df: DataFrame, val: OutputValues):
        localDf = self._getSecondDayDf(df)
        self._calculateRef15(localDf, val)

    def _calculateAll15Day2(self, df: DataFrame, val: OutputValues):
        localDf = self._getSecondDayDf(df)
        self._calculateAll15(localDf, val)
