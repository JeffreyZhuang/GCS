import serial
import time
import struct
import threading
from lib.cobs import cobs
from input import Input
from generate_packet import *

class InputBluetooth(Input):
    def __init__(self):
        super().__init__()

        self.bluetooth = serial.Serial('COM9', 115200, timeout=1000)
        self.prev_send_time = time.time()
        self.prev_recv_time = time.time()

        thread = threading.Thread(target=self.serial_thread)
        thread.setDaemon(True)
        thread.start()
    
    def serial_thread(self):
        while True:
            # Find start byte
            start_byte = self.bluetooth.read(1)
            if start_byte == b'\x00':
                # Get length byte
                payload_length = struct.unpack("B", self.bluetooth.read(1))[0]
                
                # Get payload
                payload = cobs.decode(self.bluetooth.read(payload_length + 1))
                
                # Figure out what type of payload from message ID byte
                payload_type = payload[0] # Incorrect, need to unpack?
                # print(f"Payload type: {payload_type}")
                if payload_type == 0: # Telemetry payload
                    data = struct.unpack("<BhhHhHffBBB?", payload) # Use endian to remove padding
                    self.flight_data.roll = float(data[1]) / 100
                    self.flight_data.pitch = float(data[2]) / 100
                    self.flight_data.heading = float(data[3]) / 10
                    self.flight_data.altitude = float(data[4]) / 10
                    self.flight_data.speed = float(data[5]) / 10
                    self.flight_data.lat = data[6]
                    self.flight_data.lon = data[7]
                    self.flight_data.mode_id = data[8]
                    self.flight_data.wp_idx = data[0]
                    self.flight_data.sats = data[10]
                    self.flight_data.gps_fix = data[11]

                    self.flight_data.packet_rate = 1 / (time.time() - self.prev_recv_time)
                elif payload_type == 1 or payload_type == 2 or payload_type == 3 or payload_type == 4: # Command/waypoint/landing target acknowledgement payload
                    if payload in self.command_queue:
                        self.command_queue.remove(payload)
    
    def send(self):
        if len(self.command_queue) > 0 and time.time() - self.prev_send_time > 0.1:
            self.bluetooth.write(get_pkt(self.command_queue[0]))
            self.prev_send_time = time.time()
    
    def append_queue(self, payload):
        if not payload in self.command_queue:
            self.command_queue.append(payload)