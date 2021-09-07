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
        # pd.set_option('display.max_rows', None)

        mgr = Manager()
        self.dfs = mgr.list()

        self.percentageFFtUsed = 0
        self.totalFFt = 0
        self.usedFFT = 0

        # User settings
        self.nbrOfSections = 10
        self.filterFFT = 80
        self.nbrOfTwistLengthsForMovingAvg = 20

        self.dfUnknownTwist = None
        self.dfTurtleTwist = None
        self.dfBufferTwist = None
        self.dfFullTwist = None
        self.dfMovingAvg = None

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

            localDf["gmsId"] = gmsId
            localDf["stId"] = stId

            self.dfs.append(localDf)

        except Exception as e:
            print(f"error in file: {file}")
            print(e)

# endregion

# region Add columns to raw data

    def addAvgTpm(self):
        self.rawData["avg_tpm"] = self.rawData.apply(lambda x: self.calculate_average(x), axis=1)

    def calculate_average(self, row):
        values = []
        prefixFreq = "f"
        prefixFFT = "FT"

        for i in range(4, (self.nbrOfSections + 1)):
            
            try:
                if row["V"] != "Unknown":
                    self.totalFFt += 1

                if row[f"{prefixFFT}{i}"] > self.filterFFT:
                    if row["V"] != "Unknown":
                        self.usedFFT += 1
                    
                    values.append(row[f"{prefixFreq}{i}"])
            
            except Exception as e:
                print(e)

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
        dfForSingleSpeed = self.rawData.filter(["time", "avg_tpm", "SZ", "V"])
        dfForSingleSpeed = self.addNanRow(dfForSingleSpeed).reset_index(drop=True)

        # result = x if a > b else y

        try:
            self.dfUnknownTwist = self.groupByArg(dfForSingleSpeed, "V", "Unknown").reset_index(drop=True)

        except Exception as e:
            print(e)
            
        try:
            self.dfTurtleTwist = self.groupByArg(dfForSingleSpeed, "V", "Turtle").reset_index(drop=True)

        except Exception as e:
            print(e)
        
        try:
            self.dfBufferTwist = self.groupByArg(dfForSingleSpeed, "V", "Buffer").reset_index(drop=True)

        except Exception as e:
            print(e)
            
        try:
            self.dfFullTwist = self.groupByArg(dfForSingleSpeed, "V", "Full").reset_index(drop=True)

        except Exception as e:
            print(e)
        

    def dataFrameForMovingAverage(self):
        frames = []
        dfForSingleSpeed = self.rawData.filter(["time", "avg_tpm", "SZ", "V"])
        
        try:
            dfTurtle = self.groupByArg(dfForSingleSpeed, "V", "Turtle")
            frames.append(dfTurtle)

        except:
            pass


        try:
            dfBuffer = self.groupByArg(dfForSingleSpeed, "V", "Buffer")
            frames.append(dfBuffer)

        except:
            pass

        try:
            dfFull = self.groupByArg(dfForSingleSpeed, "V", "Full")
            frames.append(dfFull)

        except:
            pass

        df = pd.concat(frames, ignore_index=True)
        df.sort_values(by=['time'], inplace=True)

        self.dfMovingAvg = self.calculateMovingAverage(df)

# endregion

# region Helper methods for data frames

    def addNanRow(self, df):
        df["next_speed"] = df["V"].shift(-1)

        for row in df.itertuples():
            if row.V != row.next_speed:
                newRow = pd.DataFrame([[row.time + datetime.timedelta(0,1), np.nan, "TwistS_", row.V, row.next_speed]], columns = df.columns)

                df = df.append(newRow)

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
        fig, (ax1) = plt.subplots(1, 1, sharex = True, sharey = True)

        self.setTitle(fig)
        self.addDataToPlot(ax1)
        self.initSubPlot(ax1, "Twist")

        plt.show()

    def setTitle(self, fig):
        percentageFFtUsed = (self.usedFFT / self.totalFFt) * 100
        fig.suptitle(f"CTS - ST {self.machineId} - All speeds\nPercentage used FFT : {percentageFFtUsed:.1f}%\nFFT > {self.filterFFT}")

    def initSubPlot(self, ax, title):
        ax.grid(True)
        ax.legend(loc="upper left")
        ax.set_ylim([0, 400])
        ax.set_ylabel(title)

    def addDataToPlot(self, ax1):

        if self.dfUnknownTwist is not None:
            ax1.plot(self.dfUnknownTwist['time'], self.dfUnknownTwist['avg_tpm'], label = "Unknown")

        if self.dfTurtleTwist is not None:
            ax1.plot(self.dfTurtleTwist['time'], self.dfTurtleTwist['avg_tpm'], label = "Turtle")

        if self.dfBufferTwist is not None:
            ax1.plot(self.dfBufferTwist['time'], self.dfBufferTwist['avg_tpm'], label = "Buffer")

        if self.dfFullTwist is not None:
            ax1.plot(self.dfFullTwist['time'], self.dfFullTwist['avg_tpm'], label = "Full")

        if self.dfMovingAvg is not None:
            ax1.plot(self.dfMovingAvg['time'], self.dfMovingAvg['MovingAvg'], label = "AVG all")


# endregion

    def main(self):
        print("Open files ...")
        self.openFiles()

        # Concatenate all data into one DataFrame
        self.rawData = pd.concat(self.dfs, ignore_index=True)

        # Update raw data table
        print("Update original data frame ...")
        self.addDateTime()
        
        self.addAvgTpm()
        self.removNullValues()
        self.sortData()
        
        # Split data in data frames for chart
        print("Split data in separate data frames ...")
        self.dataFrameForEachSpeed()
        self.dataFrameForMovingAverage()
        # self.dataFrameForMovingAveragePerSpeed()
        
        # Show chart
        print("Plot chart ...")
        self.showSubPlot()


if __name__ == "__main__":
    path = r"E:\Gilbos Machines\SmarTwist\CableTwistSensor\CTS data\20210622_Demo\Test6b"
    chart = Chart(path, "26040.99")
    chart.main()

