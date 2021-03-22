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

	# cEv_FlowMonitoring_OutOfLimit_Turtle_TwistS									: UDINT := 16#0000202A; //Dec. 8234
	# cEv_FlowMonitoring_OutOfLimit_Turtle_TwistZ									: UDINT := 16#0000202B; //Dec. 8235
	# cEv_FlowMonitoring_OutOfLimit_Turtle_TackStage1								: UDINT := 16#0000202C; //Dec. 8236
	# cEv_FlowMonitoring_OutOfLimit_Turtle_TackStage2								: UDINT := 16#0000202D; //Dec. 8237	
	# cEv_FlowMonitoring_OutOfLimit_Buffer_TwistS									: UDINT := 16#0000202E; //Dec. 8238
	# cEv_FlowMonitoring_OutOfLimit_Buffer_TwistZ									: UDINT := 16#0000202F; //Dec. 8239
	# cEv_FlowMonitoring_OutOfLimit_Buffer_TackStage1								: UDINT := 16#00002030; //Dec. 8240
	# cEv_FlowMonitoring_OutOfLimit_Buffer_TackStage2								: UDINT := 16#00002031; //Dec. 8241	
	# cEv_FlowMonitoring_OutOfLimit_Full_TwistS									: UDINT := 16#00002032; //Dec. 8242
	# cEv_FlowMonitoring_OutOfLimit_Full_TwistZ									: UDINT := 16#00002033; //Dec. 8243
	# cEv_FlowMonitoring_OutOfLimit_Full_TackStage1								: UDINT := 16#00002034; //Dec. 8244
	# cEv_FlowMonitoring_OutOfLimit_Full_TackStage2								: UDINT := 16#00002035; //Dec. 8245	


        self.df = None
        self.errorDfs = []
        self.messageIds = ["[202A]", "[202B]", "[202C]", "[202D]", "[202E]", "[202F]", "[2030]", "[2031]", "[2032]", "[2033]", "[2034]", "[2035]"]

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

    def setErrorDf(self):
        self.df = self.groupByArg(self.df, "Event Level", "Error")

    def setErrors(self):
        for id in self.messageIds:
            try:
                errorDf = self.groupByArg(self.df, "Message ID", id)
                self.errorDfs.append(errorDf)
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

        for i in self.errorDfs:
            ax.plot(i["time"], i["Message ID"], 'o', markersize=10, markerfacecolor='gray', markeredgecolor='red', markeredgewidth=2)


        self.setTitle(fig)
        # self.addDataToPlot(ax1, ax2)
        # self.initSubPlot(ax1, "Twist S")
        # self.initSubPlot(ax2, "Twist Z")

        plt.show()

    def setTitle(self, fig):
        fig.suptitle(f"Flow errors for {self.machineId}")

# endregion

    def main(self):
        print("Open file ...")
        self.openFile()

        # Update raw data table
        print("Update original data frame ...")
        self.addDateTime()
        self.sortData()
        
        self.selectST()
        self.setErrorDf()
        self.setErrors()
        
        # Show chart
        print("Plot chart ...")
        self.showPlot()


if __name__ == "__main__":

    file = r"E:\Gilbos Machines\SmarTwist\Maintenance\20210309 Dixie\MachineEvents2.xlsx"
    # id = "ST8"

    # chart = Chart(file, id)
    # chart.main()

    for i in range(1, 16):
        id = f"ST{i}"

        try:
            chart = Chart(file, id)
            chart.main()

        except:
            print(f"No data for {id}")
