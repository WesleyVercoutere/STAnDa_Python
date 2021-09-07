import matplotlib.pyplot as plt

from src.domain.Settings import Settings
from src.service.ChartItemService import ChartItemService


class Chart:

    def __init__(self, settings: Settings, chartItemService: ChartItemService):
        self._settings = settings
        self._chartItemService = chartItemService

        self._fig = plt.figure()
        self._axs = self._fig.subplots(3, 1, sharex=True, sharey=True)

        self._legs = []
        self._lines = []
        self._lined = dict()
        self._NUMBER_OF_LINES = 6

    def showPlot(self):
        [self._setAx(self._axs[i], i) for i in range(len(self._settings.speeds))]

        self._mapLines()

        self._setTitle()
        self._fig.canvas.mpl_connect('pick_event', self._onpick)
        plt.subplots_adjust(left=0.03, bottom=0.03, right=0.98, top=0.95, wspace=None, hspace=None)
        plt.show()

    def _setAx(self, ax, index):
        data = self._chartItemService.getData()

        self._lines.append(ax.plot(data[index].dfSignalData["time"], data[index].dfSignalData["tpm"], label="Signal data")[0])
        self._lines.append(ax.plot(data[index].dfReferenceMed["time"], data[index].dfReferenceMed["med_tpm"], label="Reference median")[0])
        self._lines.append(ax.plot(data[index].dfReferenceMed["time"], data[index].dfReferenceMed["upper_boundary"], label="Upper limit")[0])
        self._lines.append(ax.plot(data[index].dfReferenceMed["time"], data[index].dfReferenceMed["lower_boundary"], label="Lower limit")[0])
        self._lines.append(ax.plot(data[index].dfMonitorMed2["time"], data[index].dfMonitorMed2["median"], label=f"Median {self._settings.nbrOfValuesForMed2} samples")[0])
        self._lines.append(ax.plot(data[index].dfSignalData["time"], data[index].dfSignalData["fft"], marker='o', label="fft")[0])

        self._initSubPlot(ax, self._settings.speeds[index])

    def _initSubPlot(self, ax, title):
        ax.grid(True)
        self._legs.append(ax.legend(loc="upper left"))
        ax.set_ylim([0, 400])
        ax.set_ylabel(title)

    def _setTitle(self):
        # percentageFFtUsed = (self.usedFFT / self.totalFFt) * 100
        # fig.suptitle(
        #     f"CTS - ST {self.machineId} - All speeds\nPercentage used FFT : {percentageFFtUsed:.1f}%\nFFT > {self.filterFFT}")

        self._fig.suptitle(f"ST {self._settings.st}")

    def _mapLines(self):
        for i in range(len(self._legs)):
            startIndex = i * self._NUMBER_OF_LINES
            stopIndex = (i * self._NUMBER_OF_LINES) + self._NUMBER_OF_LINES

            for legLine, origLine in zip(self._legs[i].get_lines(), self._lines[startIndex: stopIndex]):
                legLine.set_picker(5)  # 5 pts tolerance
                self._lined[legLine] = origLine

    def _onpick(self, event):
        # on the pick event, find the orig line corresponding to the legend proxy line, and toggle the visibility
        legLine = event.artist
        origLine = self._lined[legLine]
        vis = not origLine.get_visible()
        origLine.set_visible(vis)
        # Change the alpha on the line in the legend so we can see what lines have been toggled
        if vis:
            legLine.set_alpha(1.0)
        else:
            legLine.set_alpha(0.2)
        self._fig.canvas.draw()
