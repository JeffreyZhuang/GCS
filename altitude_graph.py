import pyqtgraph as pg
from PyQt5.QtGui import *

class AltitudeGraph(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        self.x = [0, 1, 2, 5, 6, 10]
        self.y = [0, 50, 70, 70, 40, 0]

        self.plot(self.x, self.y, pen=pg.mkPen('magenta', width=5), fillLevel=0, brush=QColor(255, 0, 255, 100))
        self.getAxis('left').setTextPen(pg.mkPen('white', width=3))
        self.getAxis('bottom').setTextPen(pg.mkPen('white', width=3))
        self.getAxis('left').setPen(pg.mkPen('white', width=3))
        self.getAxis('bottom').setPen(pg.mkPen('white', width=3))
        self.setMenuEnabled(False)
        self.hideButtons()
        self.setLabel('left', 'Altitude', units="m")
        self.setLabel('bottom', 'Distance Travelled', units="m")

        # Add numbers
        font = QFont()
        font.setPixelSize(40)
        for i in range(len(self.x)):
            text = pg.TextItem(text=str(i), color=QColor("white"), fill=QColor("black"), anchor=(0.5, 0.5))
            text.setPos(self.x[i], self.y[i])
            text.setFont(font)
            self.addItem(text)