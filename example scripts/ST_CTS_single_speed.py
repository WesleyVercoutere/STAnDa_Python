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
        self.path = path
        self.machineId = id

        # only for debugging
        pd.set_option('display.max_rows', None)

        mgr = Manager()
        self.dfs = mgr.list()

        self.percentageFFtUsed = 0
        self.totalFFt = 0
        self.usedFFT = 0

        # User settings
        self.nbrOfSections = 10
        self.filterFFT = 80
        self.nbrOfTwistLengthsForMovingAvg = 50    

# region Open files

    def openFiles(self):
        filenames = glob.glob(self.path + "/*.csv")

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self.addFile, filenames)

    def addFile(self, file):
        try:
            filename = file.split("\\")
            filename = filename[len(filename) - 1]
            filename = filename.split("_")

            localDf = pd.read_csv(file, sep = ";")

            gmsId = filename[1]
            stId = filename[2]

            if stId == self.machineId:
                # Only for Dixie - wrong id for st 11
                if gmsId == "GMS11" and stId == "26134.10":
                    stId = "26134.11"

                localDf["gmsId"] = gmsId
                localDf["stId"] = stId

                self.dfs.append(localDf)

        except:
            print(f"error in file: {file}")

# endregion

# region Add columns to raw data

    def addAvgTpm(self):
        self.rawData["avg_tpm"] = self.rawData.apply(lambda x: self.calculate_average(x), axis=1)

    def calculate_average(self, row):
        values = []
        prefixFreq = "f"
        prefixFFT = "FT"

        for i in range(1, (self.nbrOfSections + 1)):

            if row["Speed"] != "Unknown":
                self.totalFFt += 1

            if row[f"{prefixFFT}{i}"] > self.filterFFT:
                if row["Speed"] != "Unknown":
                    self.usedFFT += 1
                
                values.append(row[f"{prefixFreq}{i}"])

        if len(values) > 0 and row["mmin"] > 0:
            return statistics.mean(values) / row["mmin"]

        return np.nan

    def addDateTime(self):
        self.rawData["time"] = self.rawData.apply(lambda x: self.calculateDateTime(x['DT']), axis=1)

    def calculateDateTime(self, dt):
        try:
            return(datetime.datetime.strptime(dt, '%Y-%m-%d-%H:%M:%S.%f'))

        except:
            print(f"Wrong date time format, {dt}")

    def sortData(self):
        self.rawData.sort_values(by=['time'], inplace=True)

    def removNullValues(self):
        self.rawData = self.rawData[pd.notnull(self.rawData['avg_tpm'])]

# endregion

# region Data frames

    def dataFrameForEachSpeed(self):
        dfForSingleSpeed = self.rawData.filter(["time", "avg_tpm", "SZ", "Speed"])
        dfForSingleSpeed = self.addNanRow(dfForSingleSpeed).reset_index(drop=True)

        dfUnknown = self.groupByArg(dfForSingleSpeed, "Speed", "Unknown")
        dfTurtle = self.groupByArg(dfForSingleSpeed, "Speed", "Turtle")
        dfBuffer = self.groupByArg(dfForSingleSpeed, "Speed", "Buffer")
        dfFull = self.groupByArg(dfForSingleSpeed, "Speed", "Full")
        
        self.dfUnknownTwistS = self.groupByArg(dfUnknown, "SZ", "TwistS_").reset_index(drop=True)
        self.dfUnknownTwistZ = self.groupByArg(dfUnknown, "SZ", "TwistZ_").reset_index(drop=True)
        self.dfTurtleTwistS = self.groupByArg(dfTurtle, "SZ", "TwistS_").reset_index(drop=True)
        self.dfTurtleTwistZ = self.groupByArg(dfTurtle, "SZ", "TwistZ_").reset_index(drop=True)
        self.dfBufferTwistS = self.groupByArg(dfBuffer, "SZ", "TwistS_").reset_index(drop=True)
        self.dfBufferTwistZ = self.groupByArg(dfBuffer, "SZ", "TwistZ_").reset_index(drop=True)
        self.dfFullTwistS = self.groupByArg(dfFull, "SZ", "TwistS_").reset_index(drop=True)
        self.dfFullTwistZ = self.groupByArg(dfFull, "SZ", "TwistZ_").reset_index(drop=True)

    def dataFrameForMovingAverage(self):
        dfForSingleSpeed = self.rawData.filter(["time", "avg_tpm", "SZ", "Speed"])
        dfTurtle = self.groupByArg(dfForSingleSpeed, "Speed", "Turtle")
        dfBuffer = self.groupByArg(dfForSingleSpeed, "Speed", "Buffer")
        dfFull = self.groupByArg(dfForSingleSpeed, "Speed", "Full")

        df = pd.concat([dfTurtle, dfBuffer, dfFull], ignore_index=True)
        # df = pd.concat([dfTurtle, dfFull], ignore_index=True)
        # df = pd.concat([dfTurtle], ignore_index=True)
        df.sort_values(by=['time'], inplace=True)

        dfS = self.groupByArg(df, "SZ", "TwistS_").reset_index(drop=True)
        dfZ = self.groupByArg(df, "SZ", "TwistZ_").reset_index(drop=True)

        self.dfMovingAvgAllS = self.calculateMovingAverage(dfS)
        self.dfMovingAvgAllZ = self.calculateMovingAverage(dfZ)

    def dataFrameForMovingAveragePerSpeed(self):
        dfForSingleSpeed = self.rawData.filter(["time", "avg_tpm", "SZ", "Speed"])
        dfTurtle = self.groupByArg(dfForSingleSpeed, "Speed", "Turtle")
        dfBuffer = self.groupByArg(dfForSingleSpeed, "Speed", "Buffer")

        dfTurtleS = self.groupByArg(dfTurtle, "SZ", "TwistS_").reset_index(drop=True)
        dfTurtleZ = self.groupByArg(dfTurtle, "SZ", "TwistZ_").reset_index(drop=True)
        dfBufferS = self.groupByArg(dfBuffer, "SZ", "TwistS_").reset_index(drop=True)
        dfBufferZ = self.groupByArg(dfBuffer, "SZ", "TwistZ_").reset_index(drop=True)

        self.dfMovingAvgTurtleS = self.calculateMovingAverage(dfTurtleS)
        self.dfMovingAvgTurtleZ = self.calculateMovingAverage(dfTurtleZ)
        self.dfMovingAvgBufferS = self.calculateMovingAverage(dfBufferS)
        self.dfMovingAvgBufferZ = self.calculateMovingAverage(dfBufferZ)

# endregion

# region Helper methods for data frames

    def addNanRow(self, df):
        df["next_speed"] = df["Speed"].shift(-1)

        for row in df.itertuples():
            if row.Speed != row.next_speed:
                newRowS = pd.DataFrame([[row.time + datetime.timedelta(0,1), np.nan, "TwistS_", row.Speed, row.next_speed]], columns = df.columns)
                newRowZ = pd.DataFrame([[row.time + datetime.timedelta(0,1), np.nan, "TwistZ_", row.Speed, row.next_speed]], columns = df.columns)

                df = df.append(newRowS)
                df = df.append(newRowZ)

        df.sort_values(by=['time'], inplace=True)
        return df

    def groupByArg(self, df, groupByType, name):
        groupby = df.groupby(df[groupByType])
        return groupby.get_group(name)
    
    def calculateMovingAverage(self, df):
        df["MovingAvg"] =  df["avg_tpm"].rolling(window = self.nbrOfTwistLengthsForMovingAvg).mean()
        return df
    
#endregion

# region Plot

    def showSubPlot(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex = True, sharey = True)

        self.setTitle(fig)
        self.addDataToPlot(ax1, ax2)
        self.initSubPlot(ax1, "Twist S")
        self.initSubPlot(ax2, "Twist Z")

        plt.show()

    def setTitle(self, fig):
        percentageFFtUsed = (self.usedFFT / self.totalFFt) * 100
        fig.suptitle(f"CTS - ST {self.machineId} - All speeds\nPercentage used FFT : {percentageFFtUsed:.1f}%\nFFT > {self.filterFFT}")

    def initSubPlot(self, ax, title):
        ax.grid(True)
        ax.legend(loc="upper left")
        ax.set_ylim([0, 400])
        ax.set_ylabel(title)

    def addDataToPlot(self, ax1, ax2):
        ax1.plot(self.dfUnknownTwistS['time'], self.dfUnknownTwistS['avg_tpm'], label = "Unknown")
        ax1.plot(self.dfTurtleTwistS['time'], self.dfTurtleTwistS['avg_tpm'], label = "Turtle")
        ax1.plot(self.dfBufferTwistS['time'], self.dfBufferTwistS['avg_tpm'], label = "Buffer")
        ax1.plot(self.dfFullTwistS['time'], self.dfFullTwistS['avg_tpm'], label = "Full")
        ax1.plot(self.dfMovingAvgAllS['time'], self.dfMovingAvgAllS['MovingAvg'], label = "AVG all")
        # ax1.plot(self.dfMovingAvgTurtleS['time'], self.dfMovingAvgTurtleS['MovingAvg'], label = "AVG Turtle")
        # ax1.plot(self.dfMovingAvgBufferS['time'], self.dfMovingAvgBufferS['MovingAvg'], label = "AVG Buffer")

        ax2.plot(self.dfUnknownTwistZ['time'], self.dfUnknownTwistZ['avg_tpm'], label = "Unknown")
        ax2.plot(self.dfTurtleTwistZ['time'], self.dfTurtleTwistZ['avg_tpm'], label = "Turtle")
        ax2.plot(self.dfBufferTwistZ['time'], self.dfBufferTwistZ['avg_tpm'], label = "Buffer")
        ax2.plot(self.dfFullTwistZ['time'], self.dfFullTwistZ['avg_tpm'], label = "Full")
        ax2.plot(self.dfMovingAvgAllZ['time'], self.dfMovingAvgAllZ['MovingAvg'], label = "AVG all")
        # ax2.plot(self.dfMovingAvgTurtleZ['time'], self.dfMovingAvgTurtleZ['MovingAvg'], label = "AVG Turtle")
        # ax2.plot(self.dfMovingAvgBufferZ['time'], self.dfMovingAvgBufferZ['MovingAvg'], label = "AVG Buffer")

# endregion

    def main(self):
        print("Open files ...")
        self.openFiles()

        # Concatenate all data into one DataFrame
        self.rawData = pd.concat(self.dfs, ignore_index=True)

        # Update raw data table
        print("Update original data frame ...")
        self.addAvgTpm()
        self.addDateTime()
        self.sortData()
        self.removNullValues()

        # Split data in data frames for chart
        print("Split data in separate data frames ...")
        self.dataFrameForEachSpeed()
        self.dataFrameForMovingAverage()
        self.dataFrameForMovingAveragePerSpeed()
        
        # Show chart
        print("Plot chart ...")
        self.showSubPlot()


if __name__ == "__main__":

    # Create chart for each ST.
    # ids = [1,2,4,6,7,8,9,10,11,12,14]

    # for i in ids:
    #     id = f"26134.{i}"

    #     chart = Chart(id)
    #     chart.main()

    # path = f"E:\\Gilbos Machines\\SmarTwist\\CTS\\20210107_Dixie\\csv\\W2021_1 per ST"    
    # id = "26134.1"
    # path = f"{path}\\{id}"

    # path = r"E:\Gilbos Machines\SmarTwist\CTS\20210212_Dixie\W2021_6 - kopie"
    # id = "26134.1"

    path = r"E:\Gilbos Machines\SmarTwist\Maintenance\20210305 Dixie\CTS\W2021_9"
    # id = "26040.99"

    # chart = Chart(path, id)
    # chart.main()

    for i in range(1, 16):
        id = f"26134.{i}"

        try:
            chart = Chart(path, id)
            chart.main()

        except:
            print(f"No data for {id}")
