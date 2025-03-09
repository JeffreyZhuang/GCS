import pyqtgraph as pg
from PyQt5.QtGui import QColor, QFont
from app.utils.utils import calculate_displacement_meters
import math
from app.utils.data_structures import *
import time

class RealtimeAltPlot(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        self.setFixedHeight(250)
        self.setFixedWidth(500)
        
        self.setBackground(None)

        self.x_data = []
        self.alt_data = []
        self.setpoint_data = []

        self.alt_line = self.plot([], 
                              [], 
                              pen=pg.mkPen('magenta', width=2), 
                              fillLevel=0, 
                              brush=QColor(255, 0, 255, 50))
    
        self.setpoint_line = self.plot([], 
                              [], 
                              pen=pg.mkPen('yellow', width=2))
        
        self.start_time = time.time()
    
    def update(self, alt, setpoint):
        if len(self.x_data) == 200:
            self.x_data.pop(0)
            self.alt_data.pop(0)
            self.setpoint_data.pop(0)
        self.x_data.append(time.time() - self.start_time)
        self.alt_data.append(alt)
        self.setpoint_data.append(setpoint)
        self.alt_line.setData(self.x_data, self.alt_data)
        self.setpoint_line.setData(self.x_data, self.setpoint_data)
        # self.setYRange(min=0, max=max((max(self.alt_data), max(self.setpoint_data))))