import matplotlib.pyplot as plt

from src.domain.Settings import Settings
from src.service.ChartItemService import ChartItemService


class Chart:

    def __init__(self, settings: Settings, chartItemService: ChartItemService):
        self._settings = settings
        self._chartItemService = chartItemService

    def showPlot(self):
        fig, axs = plt.subplots(3, 1, sharex=True, sharey=True)
        [self._setAx(axs[i], i) for i in range(len(self._settings.speeds))]

        plt.subplots_adjust(left=0.03, bottom=0.03, right=0.98, top=0.98, wspace=None, hspace=None)
        plt.show()

    def _setAx(self, ax, index):
        data = self._chartItemService.getData()

        ax.plot(data[index].dfSignalData["time"], data[index].dfSignalData["tpm"], label="Signal data")
        ax.plot(data[index].dfReferenceAvg["time"], data[index].dfReferenceAvg["avg_tpm"], label="Average tpm")
        ax.plot(data[index].dfReferenceAvg["time"], data[index].dfReferenceAvg["upper_boundary"], label="Upper limit")
        ax.plot(data[index].dfReferenceAvg["time"], data[index].dfReferenceAvg["lower_boundary"], label="Lower limit")
        ax.plot(data[index].dfMonitorAvg["time"], data[index].dfMonitorAvg["avg_tpm"], label="ST samples")
        ax.plot(data[index].dfMonitorMed["time"], data[index].dfMonitorMed["median"], label="Median")

        self._initSubPlot(ax, self._settings.speeds[index])

    def _initSubPlot(self, ax, title):
        ax.grid(True)
        ax.legend(loc="upper left")
        ax.set_ylim([0, 400])
        ax.set_ylabel(title)

    def _setTitle(self, fig):
        percentageFFtUsed = (self.usedFFT / self.totalFFt) * 100
        fig.suptitle(
            f"CTS - ST {self.machineId} - All speeds\nPercentage used FFT : {percentageFFtUsed:.1f}%\nFFT > {self.filterFFT}")
