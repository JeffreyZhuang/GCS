from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qdarktheme
from pfd import PrimaryFlightDisplay
from map import Map
from altitude_graph import AltitudeGraph
from datatable import DataTable
from command_buttons import CommandButtons
from input_random import InputRandom
from input_bluetooth import InputBluetooth
import numpy as np

# Bug: Doesn't work when USB used. You have to load waypoints first.
# The slow loading of waypoints is due to the delay
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # North, east, down
        self.waypoints = np.array([[-400, 200, -40],
                                   [-200, -200, -40],
                                   [200, 0, -40],
                                   [0, 400, -40]])
        
        self.pfd = PrimaryFlightDisplay()
        # self.input = InputRandom()
        self.input = InputBluetooth()

        for i in range(len(self.waypoints)):
            self.input.append_queue(self.input.generate_waypoint_packet(self.waypoints[i], i))

        self.setup_window()
        self.create_main_layout()
        self.create_left_layout()
        self.create_map_layout()
        self.add_hud()
        self.add_datatable()
        self.add_plot()
        self.start_thread()
    
    def start_thread(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1)
    
    def setup_window(self):
        self.setWindowTitle("UAV Ground Control")
        qdarktheme.setup_theme()
    
    def create_main_layout(self):
        self.main_layout = QHBoxLayout()

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def create_map_layout(self):
        self.map_layout = QVBoxLayout()
        self.main_layout.addLayout(self.map_layout, 2)

    def add_datatable(self):
        self.tabs = QTabWidget()
        self.datatable = DataTable()
        self.command_buttons = CommandButtons()
        self.tabs.addTab(self.datatable, "Data")
        self.tabs.addTab(self.command_buttons, "Commands")
        self.tabs.addTab(QWidget(), "Terminal") # Raw telemetry packets
        self.left_layout.addWidget(self.tabs)

    def create_left_layout(self):
        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)

    def add_hud(self):
        self.hud_label = QLabel()
        self.hud_label.setPixmap(self.pfd.update(0, 0, 0, 0, 0, 0, 0))
        self.left_layout.addWidget(self.hud_label)

    def add_plot(self):
        self.map = Map(self.waypoints)
        self.map_layout.addWidget(self.map, 2)

        self.altitude_graph = AltitudeGraph(self.waypoints)
        self.map_layout.addWidget(self.altitude_graph)
    
    def update(self):
        if self.input.getData():
            roll = self.input.roll
            pitch = self.input.pitch
            heading = self.input.heading
            altitude = self.input.altitude
            speed = self.input.speed 
            lat = self.input.lat 
            lon = self.input.lon

            # Transmit data
            self.input.send()
            
            # Update GUI
            self.hud_label.setPixmap(self.pfd.update(pitch, roll, heading, altitude, speed, 80, 50))
            self.map.update(heading, lat, lon)
            self.datatable.update(self.input.mode_id)
            self.command_buttons.update(len(self.input.command_queue))

if __name__ == "__main__":
    app = QApplication([])
    main = MainWindow()
    main.showMaximized()
    app.exec()