import pandas as pd
import glob


class Merge:

    def __init__(self, path):
        self.path = path

        self.dfs = []

    def openFiles(self):
        filenames = glob.glob(self.path + "/*.csv")

        for file in filenames:
            self.addFile(file)

        self.df = pd.concat(self.dfs, ignore_index=True)

        print(self.df)

    def addFile(self, file):
        try:
            filename = file.split("\\")
            filename = filename[len(filename) - 1]
            filename = filename.split("_")

            localDf = pd.read_csv(file, sep = ";")
            localDf["stId"] = filename[2]
            
            self.dfs.append(localDf)

        except:
            print(f"error in file: {file}")

    def exportCsv(self):
        self.df.to_excel(f"{path}\\MAINT_BurstTack_merged.xlsx")


    def main(self):
        self.openFiles()
        self.exportCsv()

    
if __name__ == "__main__":

    path = f"E:\\Gilbos Machines\\SmarTwist\\Maintenance\\20210211 Dixie\\Flow\\All"

    merge = Merge(path)
    merge.main()