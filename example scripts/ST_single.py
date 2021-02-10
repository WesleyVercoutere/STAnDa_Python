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

    def __init__(self, path, id):
        # only for debugging
        # pd.set_option('display.max_rows', None)

        mgr = Manager()
        self.dfs = mgr.list()

        self.percentageFFtUsed = 0
        self.totalFFt = 0
        self.usedFFT = 0

        # User settings
        self.machineId = id
        self.nbrOfSections = 10
        self.filterFFT = 80
        self.nbrOfTwistLengthsForMovingAvg = 50

        self.path = path

    def openFiles(self):
        filenames = glob.glob(self.path + "/*.csv")

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self.addFile, filenames)

    def addFile(self, file):
        try:
            if "Unknown" not in file: 
                self.dfs.append(pd.read_csv(file, sep=";"))

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

    def splitData(self):
        self.df = self.df[pd.notnull(self.df['avg_tpm'])]
        groupby = self.df.groupby(self.df.SZ)

        self.s = groupby.get_group("TwistS_")
        self.z = groupby.get_group("TwistZ_")

    def addMovingAvg(self):
        self.s["MovingAvg"] =  self.s["avg_tpm"].rolling(window = self.nbrOfTwistLengthsForMovingAvg).mean()
        self.z["MovingAvg"] =  self.z["avg_tpm"].rolling(window = self.nbrOfTwistLengthsForMovingAvg).mean()

    def showChart(self):
        plt.plot(self.s['time'], self.s['avg_tpm'], label = "Twist S")
        plt.plot(self.z['time'], self.z['avg_tpm'], label = "Twist Z")
        plt.legend(loc="upper left")
        plt.ylim(0, 300)
        plt.grid(True)

        plt.title(f"Percentage used FFT : {self.percentageFFtUsed}%")

        plt.show()

    def showSubPlot(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex = True, sharey = True)

        fig.suptitle(f"CTS - ST {self.machineId} - All speeds\nPercentage used FFT : {self.percentageFFtUsed:.1f}%")

        ax1.plot(self.s['time'], self.s['avg_tpm'], label = "Twist S")
        ax1.plot(self.s['time'], self.s['MovingAvg'], label = "Avg Twist S")
        ax1.grid(True)
        ax1.legend(loc="upper left")
        ax1.set_ylim([0, 400])


        ax2.plot(self.z['time'], self.z['avg_tpm'], label = "Twist Z")
        ax2.plot(self.z['time'], self.z['MovingAvg'], label = "Avg Twist Z")
        ax2.grid(True)
        ax2.legend(loc="upper left")
        ax2.set_ylim([0, 400])
        
        plt.show()


    def main(self):
        self.openFiles()

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

    # Create chart for each ST.
    # ids = [1,2,4,6,7,8,9,10,11,12,14]

    # for i in ids:
    #     id = f"26134.{i}"

    #     chart = Chart(id)
    #     chart.main()

    # self.path = f"E:\\Gilbos Machines\\SmarTwist\\CTS\\Logging CTS Dixie december 2020\\csv\\W2021_1 per ST\\{self.machineId}"
    # self.path = r"E:\Gilbos Machines\SmarTwist\CTS\Logging CTS Dixie december 2020\csv\W2021_1 per ST\test"
    # self.path = r"E:\\Gilbos Machines\\SmarTwist\\CTS\\Logging CTS Dixie december 2020\\csv\\W2021_1"

    path = f"E:\\Gilbos Machines\\SmarTwist\\CTS\\Logging CTS Dixie december 2020\\csv\\W2021_1 per ST"
    id = "26134.10"

    path = f"{path}\\{id}"

    chart = Chart(path, id)
    chart.main()
