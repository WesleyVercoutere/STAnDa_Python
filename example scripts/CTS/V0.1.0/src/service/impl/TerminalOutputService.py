from src.domain.Settings import Settings
from src.service.OutputService import OutputService


class TerminalOutputService(OutputService):

    def __init__(self, settings: Settings):
        super().__init__(settings=settings)

    def output(self, data):
        print()
        print(f"Reference values for {self._settings.st}")
        [self._outputValues(data, index) for index in range(len(data))]

    def _outputValues(self, data, index):
        print(self._settings.speeds[index])
        print(f"Avg all samples = {data[index].averageAll}")
        print(f"Avg 50 samples @start = {data[index].averageStart}")
        print(f"Avg 50 samples @15 min = {data[index].average15}")
        print(f"Avg all samples @15 min = {data[index].average15All}")
        print(f"Med all samples = {data[index].medianAll}")
        print(f"Med 50 samples @start = {data[index].medianStart}")
        print(f"Med 50 samples @15 min = {data[index].median15}")
        print(f"Med all samples @15 min = {data[index].median15All}")
        print()
