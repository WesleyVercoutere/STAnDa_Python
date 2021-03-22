import pandas as pd
import glob
import functools
import os
import time
import statistics 
import datetime
import matplotlib.pyplot as plt
import concurrent.futures
import multiprocessing as mp
from multiprocessing import Manager
import numpy as np


# TODO : add goal

class Chart:

    def __init__(self, path, speed):
        # only for debugging
        # pd.set_option('display.max_rows', None)

        self.selectedSpeed = speed
        self.path = path

        mgr = Manager()
        self.dfs = mgr.list()
        self.machineIds = mgr.list()

        self.idSet = set()
        self.dfChartS = {}
        self.dfChartZ = {}

        self.percentageFFtUsed = 0
        self.totalFFt = 0
        self.usedFFT = 0

        # User settings
        self.machineId = id
        self.nbrOfSections = 10
        self.filterFFT = 0
        self.nbrOfTwistLengthsForMovingAvg = 50

    def openFiles(self):
        filenames = glob.glob(self.path + "/*.csv")

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self.addFile, filenames)

    def addFile(self, file):
        try:
            if ("Unknown") not in file and (self.selectedSpeed in file): 
                filename = file.split("\\")
                filename = filename[len(filename) - 1]
                filename = filename.split("_")

                localDf = pd.read_csv(file, sep = ";")

                gmsId = filename[1]
                stId = filename[2]
                speed = filename[4]

                if gmsId == "GMS11" and stId == "26134.10":
                    stId = "26134.11"

                localDf["gmsId"] = gmsId
                localDf["stId"] = stId
                localDf["speed"] = speed

                self.machineIds.append(stId)
                self.dfs.append(localDf)

        except:
            print(f"error in file: {file}")

    def addAvgTpm(self):
        self.df["avg_tpm"] = self.df.apply(lambda x: self.calculate_average(x), axis=1)

    def calculate_average(self, row):
        values = []
        prefixFreq = "f"
        prefixFFT = "FT"

        for i in range(1, (self.nbrOfSections + 1)):
            self.totalFFt += 1

            if row[f"{prefixFFT}{i}"] > self.filterFFT:
                self.usedFFT += 1
                values.append(row[f"{prefixFreq}{i}"])

        if len(values) > 0 and row["mmin"] > 0:
            return statistics.mean(values) / row["mmin"]

        return np.nan

    def addDateTime(self):
        self.df["time"] = self.df.apply(lambda x: self.calculateDateTime(x['DT']), axis=1)

    def calculateDateTime(self, dt):
        return(datetime.datetime.strptime(dt, '%Y-%m-%d-%H:%M:%S.%f'))

    def sortData(self):
        self.df.sort_values(by=['time'], inplace=True)
        self.df = self.df[pd.notnull(self.df['avg_tpm'])]

    def splitData(self):
        groupbyMachineId = self.df.groupby(self.df.stId)
        ids = sorted(self.idSet)

        for id in self.idSet:
            dfMachine = groupbyMachineId.get_group(id)
            
            groupbyTwist = dfMachine.groupby(dfMachine.SZ)
            
            self.dfChartS[id] = groupbyTwist.get_group("TwistS_").reset_index(drop = True)
            self.dfChartZ[id] = groupbyTwist.get_group("TwistZ_").reset_index(drop = True)

    def addMovingAvg(self):
        for item in self.dfChartS:
            self.dfChartS[item]["MovingAvg"] =  self.dfChartS[item]["avg_tpm"].rolling(window = self.nbrOfTwistLengthsForMovingAvg).mean()
        
        for item in self.dfChartZ:
            self.dfChartZ[item]["MovingAvg"] =  self.dfChartZ[item]["avg_tpm"].rolling(window = self.nbrOfTwistLengthsForMovingAvg).mean()

    def showChart(self):

        for i in self.dfChartS:
            plt.plot(i['time'], i['avg_tpm'], label = i['stId'])

        plt.legend(loc="upper left")
        plt.ylim(0, 300)
        plt.grid(True)

        plt.title(f"Percentage used FFT : {self.percentageFFtUsed}%")

        plt.show()

    def showSubPlot(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex = True, sharey = True)

        fig.suptitle(f"CTS - ST {self.machineId} - All speeds\nPercentage used FFT : {self.percentageFFtUsed:.1f}%\nFFT > {self.filterFFT}")

        for item in self.dfChartS:
            ax1.plot(self.dfChartS[item]['MovingAvg'], label = item) # self.dfChartS[item]['MovingAvg'], label = item)

        ax1.grid(True)
        ax1.legend(loc="upper left")
        ax1.set_ylim([0, 400])
        ax1.set_ylabel("Twist S")

        for item in self.dfChartZ:
            ax2.plot(self.dfChartZ[item]['MovingAvg'], label = item) # self.dfChartZ[item]['MovingAvg'], label = item)

        ax2.grid(True)
        ax2.legend(loc="upper left")
        ax2.set_ylim([0, 400])
        ax2.set_ylabel("Twist Z")

        plt.show()


    def main(self):
        self.openFiles()

        # Create set of all SmarTwist id's
        for id in self.machineIds:
            self.idSet.add(id)

        # Concatenate all data into one DataFrame
        self.df = pd.concat(self.dfs, ignore_index=True)

        self.addAvgTpm()
        self.addDateTime()
        self.sortData()
        self.splitData()
        self.addMovingAvg()

        print(f"used FFT: {self.usedFFT} / total FFT: {self.totalFFt}")
        self.percentageFFtUsed = (self.usedFFT / self.totalFFt) * 100
        
        # self.showChart()
        self.showSubPlot()


if __name__ == "__main__":
    path = r"E:\Gilbos Machines\SmarTwist\CTS\20210212_Dixie\W2021_6"
    speed = "Buffer"

    chart = Chart(path, speed)
    chart.main()
