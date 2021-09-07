import concurrent.futures
import glob
from multiprocessing import Manager

import pandas as pd
from pandas import DataFrame

class SmarTwistData:

    def __init__(self) -> None:
        self.__id = str()
        self.data = dict()

        self.speeds = ("Turtle", "Buffer", "Full")

    @property
    def Id(self):
        return self.__id

    @Id.setter
    def Id(self, value):
        self.__id = value

    # Equals and Hashcode
    def __eq__(self, o: object) -> bool:
        if o == None : return False
        if type(o) != type(self): return False

        return o.Id == self.Id

    def __hash__(self) -> int:
        return hash(self.Id)

    # To string
    def __str__(self) -> str:
        # return f"{self.Id}: {self.data}"

        try :
            text = "id;speed;total;0;10;20;30;40;50;60;70;80;90;100\n"
            for speed in self.speeds:
                text += self.Id + ";"
                text += speed + ";"
                
                for number in self.data[speed]:
                    text += str(self.data[speed][number]) + ";"

                text += "\n"

            return text
        
        except:
            return "No Data"


class DataInspection:

    def __init__(self, folder) -> None:
        self.folder = folder
        self.smarTwists = list()
        mgr = Manager()
        self._dfs = mgr.list()
        self.data = DataFrame()
        self.speeds = ("Turtle", "Buffer", "Full")
        self.header = "DT;SZ;mmin;SnID;NrSgm;f1;f2;f3;f4;f5;f6;f7;f8;f9;f10;f11;f12;f13;f14;f15;f16;S1;S2;S3;S4;S5;S6;S7;S8;S9;S10;S11;S12;S13;S14;S15;S16;FT1;FT2;FT3;FT4;FT5;FT6;FT7;FT8;FT9;FT10;FT11;FT12;FT13;FT14;FT15;SnNOK;FTNOK;Shrt;Inv;TSlw;ADCOv;ADCFlt;UndFlt;V;#Tens"
        self.minFFT = [0,10,20,30,40,50,60,70,80,90,100]

    def run(self):
        filenames = glob.glob(self.folder + "/*.csv") 

        print("Get SmarTwist id's ...")
        self._getMachineNames(filenames)
        
        print("Read data from csv files ...")
        self._readFiles(filenames)
        
        print("Calculate for each ST and speed number of twistlengths ...")
        self._calculate()

        print("Output data")
        self._output()


    def _getMachineNames(self, filenames) -> None:
        machineNames = set()

        [machineNames.add(self._getName(i)) for i in filenames]
        self.smarTwists = list(machineNames)
        self.smarTwists.sort(key=lambda x: int(x.Id.split(".")[-1]))

    def _getName(self, file) -> SmarTwistData:
        smarTwist = SmarTwistData()

        filename = file.split("\\")[-1]
        filename = filename.split("_")

        smarTwist.Id = filename[2]

        return smarTwist

    def _readFiles(self, filenames) -> None:

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self._addFile, filenames)

        self.data = pd.concat(self._dfs, ignore_index=True)

    def _addFile(self, file):
        try:
            filename = file.split("\\")
            filename = filename[len(filename) - 1]
            filename = filename.split("_")

            gmsId = filename[1]
            stId = filename[2]

            localDf = pd.read_csv(file, sep=";")
            localDf["gmsId"] = gmsId
            localDf["stId"] = stId

            firstLine = open(file, 'r').readline().rstrip()

            if self.header == firstLine:
                self._dfs.append(localDf)

            else:
                print(f"No header in file: {file}")

        except Exception as e:
            print(f"error in file: {file}")
            print(e)
            print()

    def _calculate(self):
        for st in self.smarTwists:
            df = self.data
            group = df.groupby(df.stId)

            df = group.get_group(st.Id)
            group = df.groupby(df["V"])

            for speed in self.speeds:
                try:
                    dfspeed = group.get_group(speed)
                    count_row = dfspeed.shape[0]

                    st.data[speed] = dict()
                    st.data[speed]["total"] = count_row

                    for i in self.minFFT:
                        count_row = 0
                        dfspeed["totalFFT"] = dfspeed.apply(lambda x: self._calculateTotal(x, i), axis=1)
                        groupTotal = dfspeed.groupby("totalFFT")
                        dfTotal = groupTotal.get_group(1)

                        count_row = dfTotal.shape[0]

                        st.data[speed][i] = count_row

                except Exception as e:
                    print(e)

    def _calculateTotal(self, row, minFFT):
        total = 0

        for i in range(3, 10):

            if row[f"FT{i}"] >= minFFT:
                total = 1
                break

        return total

    def _output(self):
        [print(i) for i in self.smarTwists]


if __name__ == "__main__":

    # folder = r"E:\Gilbos Machines\SmarTwist\Maintenance\20210824 Dixie\CTS data\W2021_32_33 na update"
    folder = r"E:\Gilbos Machines\SmarTwist\Maintenance\20210824 Dixie\CTS data\W2021_34"
    # folder = r"E:\Gilbos Machines\SmarTwist\Maintenance\20210824 Dixie\CTS data\Test"

    app = DataInspection(folder)
    app.run()
