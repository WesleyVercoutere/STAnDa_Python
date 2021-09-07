from src.domain.Settings import Settings
from src.domain.TitleProperties import TitleProperties
from src.frontend.Chart import Chart
from src.repository.ChartItemRepository import ChartItemRepository
from src.repository.DataFrameRepository import DataFrameRepository
from src.service.CalculateService import CalculateService
from src.service.ChartItemService import ChartItemService
from src.service.DataService import DataService
from src.service.FolderService import FolderService
from src.service.impl.FileOutputService import FileOutputService
from src.service.impl.TerminalOutputService import TerminalOutputService


class App:

    def __init__(self, folder, st, nbrOfSections, sectionMask, minFFT,
                 nbrOfValuesForRefAvg, nbrOfValuesForMonAvg,
                 nbrOfValuesForMed1, nbrOfValuesForMed2,  boundary):
        settings = Settings(folder, st, nbrOfSections, sectionMask, minFFT, nbrOfValuesForRefAvg, nbrOfValuesForMonAvg, nbrOfValuesForMed1, nbrOfValuesForMed2, boundary)
        titleProps = TitleProperties()
        dataFrameRepo = DataFrameRepository()
        chartItemRepo = ChartItemRepository()

        self.dataService = DataService(settings=settings, titleProps=titleProps, dataFrameRepo=dataFrameRepo)
        self.folderService = FolderService(settings=settings, dataService=self.dataService)
        self.chartItemService = ChartItemService(settings=settings, dataService=self.dataService, chartItemRepo=chartItemRepo)

        outputService = TerminalOutputService(settings=settings)
        # outputService = FileOutputService(settings=settings)
        self.calculateService = CalculateService(settings=settings, dataService=self.dataService, chartItemRepo=chartItemRepo, outputService=outputService)
        self.chart = Chart(settings=settings, chartItemService=self.chartItemService)

    def run(self):
        print("Open files ...")
        self.folderService.openFiles()

        print("Process raw data ...")
        self.dataService.processData()

        print("Process data for each speed ...")
        self.chartItemService.processData()

        print("Process average and median values ...")
        # self.calculateService.processData()

        print("Plot chart ...")
        self.chart.showPlot()
