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

    def __init__(self, file, id):
        self.file = file
        self.machineId = id

        # only for debugging
        # pd.set_option('display.max_rows', None) 

        self.df = None
        self.errorDf = None
        self.errorDfs = []
        self.messageIds = ["[2049]", "[204A]", "[204B]", "[204C]", "[204D]", "[204E]"]

# region Open files

    def openFile(self):
        self.df = pd.read_excel(self.file)

# endregion

# region Add columns to raw data

    def addDateTime(self):
        self.df["time"] = self.df.apply(lambda x: self.calculateDateTime(x["Timestamp"]), axis=1)

    def calculateDateTime(self, dt):
        try:
            return(datetime.datetime.strptime(dt, '%m/%d/%Y %I:%M:%S %p'))

        except:
            print(f"Wrong date time format, {dt}")

    def sortData(self):
        self.df.sort_values(by=['time'], inplace=True)

# endregion

# region Data frames

    def selectST(self):
        self.df = self.groupByArg(self.df, "submachine name", self.machineId)

    def setTests(self):
        self.tackTest = self.groupByArg(self.df, "Message ID", "[2049]")

    def setErrorDf(self):
        self.errorDf = self.groupByArg(self.df, "Event Level", "Error")

    def setErrors(self):
        for id in self.messageIds:
            try:
                df = self.groupByArg(self.errorDf, "Message ID", id)
                self.errorDfs.append(df)
            except:
                print(f"No entries for {id}")

            
# endregion

# region Helper methods for data frames

    def groupByArg(self, df, groupByType, name):
        groupby = df.groupby(df[groupByType])
        return groupby.get_group(name)
    
#endregion

# region Plot

    def showPlot(self):
        fig, (ax) = plt.subplots(1, 1)

        ax.plot(self.tackTest["time"], self.tackTest["Message ID"], 'o', markersize=10, markerfacecolor='gray', markeredgecolor='black', markeredgewidth=2)

        for i in self.errorDfs:
            ax.plot(i["time"], i["Message ID"], 'o', markersize=10, markerfacecolor='gray', markeredgecolor='red', markeredgewidth=2)


        self.setTitle(fig)
        # self.addDataToPlot(ax1, ax2)
        # self.initSubPlot(ax1, "Twist S")
        # self.initSubPlot(ax2, "Twist Z")

        plt.show()

    def setTitle(self, fig):
        fig.suptitle(f"Tack burst errors for {self.machineId}")

# endregion

    def main(self):
        print("Open file ...")
        self.openFile()

        # Update raw data table
        print("Update original data frame ...")
        self.addDateTime()
        self.sortData()
        
        self.selectST()
        self.setTests()
        self.setErrorDf()
        self.setErrors()
        
        # Show chart
        print("Plot chart ...")
        self.showPlot()


if __name__ == "__main__":

    file = r"E:\Gilbos Machines\SmarTwist\Maintenance\20210309 Dixie\MachineEvents2.xlsx"
    id = "ST8"

    chart = Chart(file, id)
    chart.main()

    # for i in range(1, 16):
    #     id = f"ST{i}"

    #     try:
    #         chart = Chart(file, id)
    #         chart.main()

    #     except:
    #         print(f"No data for {id}")
