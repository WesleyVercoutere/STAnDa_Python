# TODO : Check header is present in file
# TODO : average and median of 50 samples after 15 min.
# TODO : median in chart with 9 and 19 samples

from src.App import App

if __name__ == "__main__":
    folder = r"E:\Gilbos Machines\SmarTwist\Maintenance\20210611 Dixie\W2021_23"
    stPrefix = "26134."
    stId = 2

    nbrOfSections = 10
    sectionMask = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    minFFT = 80

    nbrOfValuesForRefAvg = 50
    nbrOfValuesForMonAvg = 20
    nbrOfValuesForMed1 = 9
    nbrOfValuesForMed2 = 19

    boundary = 10

    app = App(folder=folder,
              st=f"{stPrefix}{stId}",
              nbrOfSections=nbrOfSections,
              sectionMask=sectionMask,
              minFFT=minFFT,
              nbrOfValuesForRefAvg=nbrOfValuesForRefAvg,
              nbrOfValuesForMonAvg=nbrOfValuesForMonAvg,
              nbrOfValuesForMed1=nbrOfValuesForMed1,
              nbrOfValuesForMed2=nbrOfValuesForMed2,
              boundary=boundary)

    app.run()

    # for stId in range(1, 16):
    #
    #     try:
    #         app = App(folder=folder,
    #                   st=f"{stPrefix}{stId}",
    #                   nbrOfSections=nbrOfSections,
    #                   sectionMask=sectionMask,
    #                   minFFT=minFFT,
    #                   nbrOfValuesForRefAvg=nbrOfValuesForRefAvg,
    #                   nbrOfValuesForMonAvg=nbrOfValuesForMonAvg,
    #                   nbrOfValuesForMed1=nbrOfValuesForMed1,
    #                   nbrOfValuesForMed2=nbrOfValuesForMed2,
    #                   boundary=boundary)
    #
    #         app.run()
    #
    #     except Exception as e:
    #         print(f"No data for {stPrefix}{stId}")
    #         print(e)
