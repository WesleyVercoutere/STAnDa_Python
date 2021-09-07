from src.domain.Settings import Settings
from src.service.OutputService import OutputService


class FileOutputService(OutputService):

    def __init__(self, settings: Settings):
        super().__init__(settings=settings)

        self._fileName = r"d:\temp\CTS_output.txt"

        try:
            self._setHeader()

        except Exception as e:
            print("File already exists")
            print(e)

    def output(self, data):
        f = open(self._fileName, "a")
        f.write("\n")

        [self._outputValues(f, data, index) for index in range(len(data))]

        f.close()

    '''
        volgorde items in array
            0 : average/mediaan eerste 50 samples
            1 : average/mediaan alle samples
            2 : average/mediaan eerste 50 samples na 15 minuten
            3 : average/mediaan alle samples na 15 minuten
            4 : average/mediaan eerste 50 samples dag 2
            5 : average/mediaan alle samples dag2
            6 : average/mediaan eerste 50 samples na 15 minuten dag 2
            7 : average/mediaan alle samples na 15 minuten dag 2
        '''

    def _setHeader(self):
        f = open(self._fileName, "x")

        for i in range(3):
            f.write("STid;Avg start;Avg all;Avg 15;Avg all 15;"
                    "Avg start day 2;Avg all day 2;Avg 15 day 2;Avg all 15 day 2;"
                    "Med start;Med all;Med 15;Med all 15;"
                    "Med start day 2;Med all day 2;Med 15 day 2;Med all 15 day 2;")

        f.close()

    def _outputValues(self, file, data, index):
        file.write(
            f"{self._settings.st};")

        for i in range(len(data[index].getAverages())):
            file.write(f"{data[index].getAverages()[i]};")

        for i in range(len(data[index].getMedians())):
            file.write(f"{data[index].getMedians()[i]};")
