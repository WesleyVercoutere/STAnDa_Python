from src.domain.ChartItem import ChartItem


class ChartItemRepository:

    def __init__(self):
        # 0 = Turtle
        # 1 = Buffer
        # 2 = Full
        self._chartItems = []

    def addItem(self, item: ChartItem):
        self._chartItems.append(item)

    def getAll(self):
        return self._chartItems

    def getIndex(self, index):
        return self._chartItems[index]
