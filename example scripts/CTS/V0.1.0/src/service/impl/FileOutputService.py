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

    def _setHeader(self):
        f = open(self._fileName, "x")

        for i in range(3):
            f.write("STid;Avg start;Avg all;Avg 15;Avg all 15;Med start;Med all;Med 15;Med all 15;")

        f.close()

    def _outputValues(self, file, data, index):
        file.write(
            f"{self._settings.st};{data[index].averageStart};{data[index].averageAll};{data[index].average15};{data[index].average15All};"
            f"{data[index].medianStart};{data[index].medianAll};{data[index].median15};{data[index].median15All};")
