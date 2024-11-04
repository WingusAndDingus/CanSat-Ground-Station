import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# from matplotlib.figure import Figure

# from GUI_files.test import generate_data
# from GUI_files.gui import window
# from GUI_files.test2 import update_plot


class Ground_Station:
    def __init__(self):
        self.data = {
            'TEAM_ID': 2031, # FIXME : Add actual team id
            'MISSION_TIME': '00:00:00', # UTC time in hh:mm:ss
            'PACKET_COUNT': 0, # The total count of transmitted packets since turned on reset to zero by command when the CanSat is installed in the rocket on the launch pad at the beginning of the mission and maintained through processor reset.
            'MODE': 'S', # 'F' for flight mode and 'S' for simulation mode.
            'STATE': 'U', # The operation state of the software. (LAUNCH_PAD, ASCENT, APOGEE, DESCENT, PROBE_RELEASE, LANDED).
            'ALTITUDE': 0, # In units of meters and must be relative to ground level at the launch site. (Zeroed before launch?)
            'TEMPERATURE': 0, # In degrees Celsius
            'PRESSURE': 0, # In kPa. Air pressure of the censor used.
            'VOLTAGE': 0, # Voltage of the Cansat power bus
            'GYRO_R': 0, # Gyro reading of roll axis (degrees/sec)
            'GYRO_P': 0,  # Gyro reading of pitch axis (degrees/sec)
            'GYRO_Y': 0,  # Gyro reading of yaw axis (degrees/sec)
            'ACCEL_R': 0,  # Accelerometer reading of roll axis (degrees/sec^2)
            'ACCEL_P': 0,  # Accelerometer reading of pitch axis (degrees/sec^2)
            'ACCEL_Y': 0,  # Accelerometer reading of yaw axis (degrees/sec^2)
            'MAG_R': 0, # Magnetometer reading in roll axis (gauss)
            'MAG_P': 0,  # Magnetometer reading in pitch axis (gauss)
            'MAG_Y': 0,  # Magnetometer reading in yaw axis (gauss)
            'AUTO_GYRO_ROTATION_RATE': 0, # The rotation  rate of the auto-gyro relative to the Cansat structure (degrees/sec)
            'GPS_TIME': '00:00:00', # The time received from the GPS receiver. UTC time, 1 second resolution
            'GPS_ALTITUDE': 0, # The altitude from the GPS in meters above mean sea level. Resolution of 0.1 meters
            'GPS_LATITUDE': 0, # The latitude from the GPS in decimal degrees with resolution of 0.0001 degrees North
            'GPS_LONGITUDE': 0, # The longitude from the GPS in decimal degrees with resolution of 0.0001 degrees West
            'GPS_SATS': 0, # The number of GPS satellites being tracked by the GPS receiver
            'CMD_ECHO': 'CXON' # The text of the last command received and processed by the Cansat
        }
        # self.csv_path = csv_path
        #
        # try:
        #     f = open(self.csv_path)
        #     self.df = pd.read_csv(self.csv_file_path)  # Checks to see if the csv file exists.
        # except:
        #     print("Could not open CSV file: ", self.csv_path)

        self.window = tk.Tk()
        self.window.title('Ground Station')

        self.altitude_data = [0]
        self.temperature_data = [0]
        self.pressure_data = [0]
        self.voltage_data = [0]
        self.gyro_r_data = [0]
        self.gyro_p_data = [0]
        self.gyro_y_data = [0]
        self.accel_r_data = [0]
        self.accel_p_data = [0]
        self.accel_y_data = [0]
        self.mag_r_data = [0]
        self.mag_p_data = [0]
        self.mag_y_data = [0]
        self.auto_gyro_rotate_rate_data = [0]
        self.gps_altitude_data = [0]
        self.gps_latitude_data = [0]
        self.gps_longitude_data = [0]
        self.gps_sats_data = [0]

        self.alt_fig, self.alt_ax = plt.subplots()
        self.alt_ax.title.set_text('Altitude')
        self.alt_line, = self.alt_ax.plot(range(0,len(self.altitude_data)), self.altitude_data)
        # self.alt_line.set_animated(True)
        self.alt_canvas = FigureCanvasTkAgg(self.alt_fig, self.window)
        self.alt_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        self.temp_fig, self.temp_ax = plt.subplots()
        self.temp_line, = self.temp_ax.plot(len(self.temperature_data), self.temperature_data, 'ro')
        self.temp_canvas = FigureCanvasTkAgg(self.temp_fig, self.window)
        self.temp_canvas.get_tk_widget().pack()

        # self.pressure_fig, self.pressure_ax = plt.subplots()
        # self.pressure_line, = self.pressure_ax.plot(len(self.pressure_data), self.pressure_data, 'ro')
        # self.pressure_canvas = FigureCanvasTkAgg(self.pressure_fig, self.window)
        # self.pressure_canvas.get_tk_widget().pack()
        #
        # self.volt_fig, self.volt_ax = plt.subplots()
        # self.volt_line, = self.volt_ax.plot(len(self.voltage_data), self.voltage_data, 'ro')
        # self.volt_canvas = FigureCanvasTkAgg(self.volt_fig, self.window)
        # self.volt_canvas.get_tk_widget().pack()
        #
        # self.gyro_r_fig, self.gyro_r_ax = plt.subplots()
        # self.gyro_r_line, = self.gyro_r_ax.plot(len(self.gyro_r_data), self.gyro_r_data, 'ro')
        # self.gyro_r_canvas = FigureCanvasTkAgg(self.gyro_r_fig, self.window)
        # self.gyro_r_canvas.get_tk_widget().pack()
        #
        # self.gyro_p_fig, self.gyro_p_ax = plt.subplots()
        # self.gyro_p_line, = self.gyro_p_ax.plot(len(self.gyro_p_data), self.gyro_p_data, 'ro')
        # self.gyro_p_canvas = FigureCanvasTkAgg(self.gyro_p_fig, self.window)
        # self.gyro_p_canvas.get_tk_widget().pack()

        # self.gyro_y_fig, self.gyro_y_ax = plt.subplots()
        # self.gyro_y_line, = self.gyro_y_ax.plot(len(self.gyro_self.altitude_data), self.gyro_self.altitude_data, 'ro')
        #
        # self.accel_r_fig, self.accel_r_ax = plt.subplots()
        # self.accel_r_line, = self.accel_r_ax.plot(len(self.accel_r_data), self.accel_r_data, 'ro')
        #
        # self.accel_p_fig, self.accel_p_ax = plt.subplots()
        # self.accel_p_line, = self.accel_p_ax.plot(len(self.accel_p_data), self.accel_p_data, 'ro')
        #
        # self.accel_y_fig, self.accel_y_ax = plt.subplots()
        # self.accel_y_line, = self.accel_y_ax.plot(len(self.accel_self.altitude_data), self.accel_self.altitude_data, 'ro')
        #
        # self.mag_r_fig, self.mag_r_ax = plt.subplots()
        # self.mag_r_line, = self.mag_r_ax.plot(len(self.mag_r_data), self.mag_r_data, 'ro')
        #
        # self.mag_p_fig, self.mag_p_ax = plt.subplots()
        # self.mag_p_line, = self.mag_p_ax.plot(len(self.mag_p_data), self.mag_p_data, 'ro')
        #
        # self.mag_y_fig, self.mag_y_ax = plt.subplots()
        # self.mag_y_line, = self.mag_y_ax.plot(len(self.mag_self.altitude_data), self.mag_self.altitude_data, 'ro')
        #
        # self.auto_gyro_rotate_rate_fig, self.auto_gyro_rotate_rate_ax = plt.subplots()
        # self.auto_gyro_rotate_rate_line, = self.auto_gyro_rotate_rate_ax.plot(len(self.auto_gyro_rotate_rate_data), self.auto_gyro_rotate_rate_data, 'ro')
        #
        # self.gps_alt_fig, self.gps_alt_ax = plt.subplots()
        # self.gps_alt_line, = self.gps_alt_ax.plot(len(self.gps_altitude_data), self.gps_altitude_data, 'ro')
        #
        # self.gps_lat_fig, self.gps_lat_ax = plt.subplots()
        # self.gps_lat_line, = self.gps_lat_ax.plot(len(self.gps_latitude_data), self.gps_latitude_data, 'ro')
        #
        # self.gps_lon_fig, self.gps_lon_ax = plt.subplots()
        # self.gps_lon_line, = self.gps_lon_ax.plot(len(self.gps_longitude_data), self.gps_longitude_data, 'ro')
        #
        # self.gps_sats_fig, self.gps_sats_ax = plt.subplots()
        # self.gps_sats_lin, = self.gps_sats_ax.plot(len(self.gps_sats_data), self.gps_sats_data, 'ro')
        #
        # self.

    def generate_data(self):
        if (len(self.altitude_data) >= 5):
            self.altitude_data.pop(0)
            self.altitude_data.append(np.random.randint(0, 10))
        else:
            self.altitude_data.append(np.random.randint(0, 10))

        if (len(self.temperature_data) >= 5):
            self.temperature_data.pop(0)
            self.temperature_data.append(np.random.randint(0, 10))
        else:
            self.temperature_data.append(np.random.randint(0, 10))

    def update_plots(self):
        self.generate_data()
        self.alt_ax.clear()
        self.alt_line, = self.alt_ax.plot(range(0,len(self.altitude_data)), self.altitude_data)
        self.alt_canvas.draw()

        # self.

        self.window.after(100, self.update_plots)

    def gui(self):
        self.window.after(500, self.update_plots)
        self.window.mainloop()

ground = Ground_Station()
ground.gui()
