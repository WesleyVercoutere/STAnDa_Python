import concurrent.futures
import glob
from multiprocessing import Manager

import pandas as pd

from src.domain.Settings import Settings
from src.service.DataService import DataService


class FolderService:

    def __init__(self, settings: Settings, dataService: DataService):
        self._settings = settings
        self._dataService = dataService

        mgr = Manager()
        self._dfs = mgr.list()

    def openFiles(self):
        filenames = glob.glob(self._settings.folder + "/*.csv")

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self._addFile, filenames)

        data = pd.concat(self._dfs, ignore_index=True)
        self._dataService.addRawData(data)

    def _addFile(self, file):
        try:
            filename = file.split("\\")
            filename = filename[len(filename) - 1]
            filename = filename.split("_")

            # localDf = pd.read_csv(file, sep=";")

            gmsId = filename[1]
            stId = filename[2]

            if stId == self._settings.st:
                localDf = pd.read_csv(file, sep=";")
                localDf["gmsId"] = gmsId
                localDf["stId"] = stId

                self._dfs.append(localDf)

        except Exception as e:
            print(f"error in file: {file}")
            print(e)
            print()
