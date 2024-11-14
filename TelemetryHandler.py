import serial
import csv
import os
import time
from threading import Thread
from datetime import datetime
from digi.xbee.devices import XBeeDevice

# TESTING RECEIVING telemetry through XBee instead of Serial
# XBee might be better if used outside of the class file

class TelemetryHandler:
    radioDevice = XBeeDevice("COM1", 9600)
    def __init__(self, team_id, port, baudrate=9600):
        """
        Initialize the telemetry handler.
        
        Args:
            team_id (str): Four digit team identification number
            port (str): Serial port for communication
            baudrate (int): Baud rate for serial communication
        """

        self.team_id = team_id
        self.serial_port = None
        self.is_receiving = False
        self.csv_file = None
        self.csv_writer = None
        self.packet_count = 0
        # Initialize XBee connection
        # radioDevice = XBeeDevice("COM1", 9600)
        # much simpler but IDK if it works?
        # Initialize serial connection
        
        # Original method utilizing Serial
        try:
            self.serial_port = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=1
            )
        except serial.SerialException as e:
            raise Exception(f"Failed to open serial port: {e}")
           
        # Define telemetry fields as per competition requirements
        self.telemetry_fields = [
            'TEAM_ID', 'MISSION_TIME', 'PACKET_COUNT', 'MODE', 'STATE',
            'ALTITUDE', 'TEMPERATURE', 'PRESSURE', 'VOLTAGE',
            'GYRO_R', 'GYRO_P', 'GYRO_Y',
            'ACCEL_R', 'ACCEL_P', 'ACCEL_Y',
            'MAG_R', 'MAG_P', 'MAG_Y',
            'AUTO_GYRO_ROTATION_RATE',
            'GPS_TIME', 'GPS_ALTITUDE', 'GPS_LATITUDE', 'GPS_LONGITUDE', 'GPS_SATS',
            'CMD_ECHO'
        ]
        
    def start_telemetry(self):
        # Start receiving telemetry data. (Using Serial)
        if not self.serial_port.is_open:
            self.serial_port.open()
            
        # Using XbeeDevice
        
        # Create CSV file with specified naming format
        filename = f"Flight_{self.team_id}.csv"
        self.csv_file = open(filename, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        
        # Write header row
        self.csv_writer.writerow(self.telemetry_fields)
        
        # Start receiving data
        self.is_receiving = True
        self.receive_thread = Thread(target=self._receive_telemetry, daemon=True)
        self.receive_thread.start()
        
        # Send initial commands
        self.send_command(f"CMD,{self.team_id},CX,ON")  # Start telemetry
        self.send_command(f"CMD,{self.team_id},CAL")    # Calibrate altitude
        
    def stop_telemetry(self):
        """Stop receiving telemetry data and close files."""
        self.is_receiving = False
        if self.receive_thread:
            self.receive_thread.join()
            
        if self.csv_file:
            self.csv_file.close()
            
        if self.serial_port and self.serial_port.is_open:
            self.send_command(f"CMD,{self.team_id},CX,OFF")
            self.serial_port.close()
            
    def send_command(self, command):
        """
        Send a command to the CanSat.
        
        Args:
            command (str): Command string following competition format
        """
        if self.serial_port and self.serial_port.is_open:
            command = command.strip() + '\n'
            self.serial_port.write(command.encode('utf-8'))
            
    def _receive_telemetry(self):
        """Internal method to receive and process telemetry data."""
        while self.is_receiving:
            try:
                if self.serial_port.in_waiting:
                    # Read line and decode
                    line = self.serial_port.readline().decode('utf-8').strip()
                    
                    # Parse data
                    data = line.split(',')
                    
                    # Validate team ID and basic data format
                    if len(data) >= len(self.telemetry_fields) and data[0] == self.team_id:
                        # Write to CSV file
                        self.csv_writer.writerow(data)
                        self.csv_file.flush()  # Ensure data is written to disk
                        
                        # Update packet count
                        self.packet_count = int(data[2])
                        
            except Exception as e:
                print(f"Error receiving telemetry: {e}")
                self.is_receiving = False
                break
                
    def set_simulation_mode(self, enable=True):
        """
        Enable or disable simulation mode.
        
        Args:
            enable (bool): True to enable simulation mode, False to disable
        """
        if enable:
            self.send_command(f"CMD,{self.team_id},SIM,ENABLE")
            self.send_command(f"CMD,{self.team_id},SIM,ACTIVATE")
        else:
            self.send_command(f"CMD,{self.team_id},SIM,DISABLE")
            
    def set_pressure(self, pressure):
        """
        Send simulated pressure data (simulation mode only).
        
        Args:
            pressure (int): Pressure in pascals
        """
        self.send_command(f"CMD,{self.team_id},SIMP,{pressure}")
        
    def set_time(self, time_str=None):
        """
        Set the mission time.
        
        Args:
            time_str (str): Time in format hh:mm:ss, or None to use GPS time
        """
        if time_str:
            self.send_command(f"CMD,{self.team_id},ST,{time_str}")
        else:
            self.send_command(f"CMD,{self.team_id},ST,GPS")