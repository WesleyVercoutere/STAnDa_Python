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





class Chart1:

    def __init__(self):
        mgr = Manager()
        self.dfs = mgr.list()


    def addFile(self, file):
        try:
            self.dfs.append(pd.read_csv(file, sep=";"))
            print(len(self.dfs))

        except:
            print(f"error in file: {file}")

    def calculate_average(self, *args, mmin):
        if mmin <= 0:
            return 0

        return (statistics.mean(args) / mmin) 

    def calculate_time(self, dt):
        return(datetime.datetime.strptime(dt, '%Y-%m-%d-%H:%M:%S.%f'))

    def main(self):
        print("Start reading files")
        startTime = time.time()

        path = r"E:\Gilbos Machines\SmarTwist\CTS\Logging CTS Dixie december 2020\csv\W2021_1 per ST\26134.10"
        # path = r"E:\Gilbos Machines\SmarTwist\CTS\Logging CTS Dixie december 2020\csv\W2021_1 per ST\test"
        # path = r"E:\\Gilbos Machines\\SmarTwist\\CTS\\Logging CTS Dixie december 2020\\csv\\W2021_1"

        filenames = glob.glob(path + "/*.csv")



        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self.addFile, filenames)



        # Concatenate all data into one DataFrame
        print(len(self.dfs))
        df = pd.concat(self.dfs, ignore_index=True)

        endTime = time.time()
        totalTime = endTime - startTime

        print("Stop reading files")
        print(f"Time to read = {totalTime}")


        df["avg_tpm"] = df.apply(lambda x: self.calculate_average(x['f1'], x['f2'], x['f3'], x['f4'], x['f5'], x['f6'], x['f7'], x['f8'], x['f9'], x['f10'], mmin = x['mmin']), axis=1)


        # import datetime
        # date_time_str = '2018-06-29 08:15:27.243860'
        # date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
        df["time"] = df.apply(lambda x: self.calculate_time(x['DT']), axis=1)


        df.sort_values(by=['time'], inplace=True)

        groupby = df.groupby(df.SZ)

        s = groupby.get_group("TwistS_")
        z = groupby.get_group("TwistZ_")

        plt.plot(s['time'], s['avg_tpm'], label = "Twist S")
        plt.plot(z['time'], z['avg_tpm'], label = "Twist Z")
        plt.legend(loc="upper left")
        plt.ylim(0, 300)
        plt.grid(True)

        endTime = time.time()
        totalTime = endTime - startTime

        print(f"Total time = {totalTime}")

        plt.show()


if __name__ == "__main__":
    chart = Chart1()
    chart.main()
