from src.domain.Settings import Settings
from src.service.OutputService import OutputService


class TerminalOutputService(OutputService):

    def __init__(self, settings: Settings):
        super().__init__(settings=settings)

    def output(self, data):
        print()
        print(f"Reference values for {self._settings.st}")
        [self._outputValues(data, index) for index in range(len(data))]

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

    def _outputValues(self, data, index):
        print(self._settings.speeds[index])
        print(f"Avg 50 samples @start = {data[index].getAverages()[0]}")
        print(f"Avg all samples = {data[index].getAverages()[1]}")
        print(f"Avg 50 samples @15 min = {data[index].getAverages()[2]}")
        print(f"Avg all samples @15 min = {data[index].getAverages()[3]}")

        print(f"Avg 50 samples @start day 2 = {data[index].getAverages()[4]}")
        print(f"Avg all samples day 2 = {data[index].getAverages()[5]}")
        print(f"Avg 50 samples @15 min day 2 = {data[index].getAverages()[6]}")
        print(f"Avg all samples @15 min day 2 = {data[index].getAverages()[7]}")

        print(f"Med 50 samples @start = {data[index].getMedians()[0]}")
        print(f"Med all samples = {data[index].getMedians()[1]}")
        print(f"Med 50 samples @15 min = {data[index].getMedians()[2]}")
        print(f"Med all samples @15 min = {data[index].getMedians()[3]}")

        print(f"Med 50 samples @start day 2 = {data[index].getMedians()[4]}")
        print(f"Med all samples day 2 = {data[index].getMedians()[5]}")
        print(f"Med 50 samples @15 min day 2 = {data[index].getMedians()[6]}")
        print(f"Med all samples @15 min day 2 = {data[index].getMedians()[7]}")
        print()
