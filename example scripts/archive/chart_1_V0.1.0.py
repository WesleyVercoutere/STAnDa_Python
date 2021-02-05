import pandas as pd
import glob
import functools
import os
import time
import statistics 
import datetime
import matplotlib.pyplot as plt
import concurrent.futures


# print(df)

print("Start reading files")

startTime = time.time()


# singleFile = "E:/Gilbos Machines/SmarTwist/CTS/Logging CTS Dixie december 2020/csv/W2021_1 per ST/26134.10/CTS_GMS10_26134.10_0042f33e3b71e5b31d4403189bcea8fb90fef1c4_Buffer_2021-01-04-90329.csv"

# df = pd.read_csv(singleFile, sep=";")

path = r"E:\Gilbos Machines\SmarTwist\CTS\Logging CTS Dixie december 2020\csv\W2021_1 per ST\26134.10"
# path = r"E:\\Gilbos Machines\\SmarTwist\\CTS\\Logging CTS Dixie december 2020\\csv\\W2021_1"

# all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent
# df_from_each_file = (pd.read_csv(f) for f in all_files)
# concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)


filenames = glob.glob(path + "/*.csv")

dfs = []

# for filename in filenames:
#     try:
#         dfs.append(pd.read_csv(filename, sep=";"))

#     except:
#         print(f"error in file: {filename}")


# def do_something(filename):
#     try:
#         dfs.append(pd.read_csv(filename, sep=";"))

#     except:
#         print(f"error in file: {filename}")

# with concurrent.futures.ProcessPoolExecutor() as executor:
#     executor.map(do_something, filenames)



def do_something(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    return f'Done Sleeping...{seconds}'


with concurrent.futures.ProcessPoolExecutor() as executor:
    secs = [5, 4, 3, 2, 1]
    results = executor.map(do_something, secs)

    # for result in results:
    #     print(result)





# Concatenate all data into one DataFrame
df = pd.concat(dfs, ignore_index=True)

endTime = time.time()
totalTime = endTime - startTime

print("Stop reading files")

print(f"Time to read = {totalTime}")



def calculate_average(*args, mmin):

    if mmin <= 0:
        return 0

    return (statistics.mean(args) / mmin) 


def calculate_time(dt):

    return(datetime.datetime.strptime(dt, '%Y-%m-%d-%H:%M:%S.%f'))


df["avg_tpm"] = df.apply(lambda x: calculate_average(x['f1'], x['f2'], x['f3'], x['f4'], x['f5'], x['f6'], x['f7'], x['f8'], x['f9'], x['f10'], mmin = x['mmin']), axis=1)


# import datetime
# date_time_str = '2018-06-29 08:15:27.243860'
# date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
df["time"] = df.apply(lambda x: calculate_time(x['DT']), axis=1)


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

