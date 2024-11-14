import tkinter as tk
from tkinter import ttk
from tkinter import font

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14}) # Default font size, minimum set by mission guide
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from time import strftime

class Ground_Station:
    def __init__(self):
        self.data = { # I just used this as a way to get the format of the packets out, we don't need to use it for anything and can be deleted eventually if not used
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

        ###### Any other variables can go here ######
        self.sim_on: bool = False
        self.sim_active: bool = False
        self.can_on: bool = False
        self.set_time_gps: bool = False
        self.set_time: bool = False
        self.sim_pressure: bool = False
        self.calibrate: bool = False
        self.mechanism_actuate: bool = False

        ##### This just makes the window, sets title, and allows it to be resizable #####
        self.window = tk.Tk()
        self.window.title('Ground Station')
        self.window.resizable(True, True)

        ##### This is where the graphs will take their data from ######

        # For final implementation another array for time stamps will be used (hopefully)
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
        self.telemetry_time = [0] # Used for timestamps

        ##### This is basically a template for all of the plots of data #####

        self.alt_fig, self.alt_ax = plt.subplots() # Initializes the figure and axes that will be used
        self.alt_line, = self.alt_ax.plot(range(0,len(self.altitude_data)), self.altitude_data) # Creates the line that will be displayed
        self.alt_canvas = FigureCanvasTkAgg(self.alt_fig, self.window) # This is what stores the plot and allows it to be displayed in a TKinter window
        self.alt_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew") # Place the canvas so that all the graphs can be aligned
        # The 'sticky' variable basically just lets the canvas take up its entire "section" of the window
        # I don't actually know what the documentation says it is, that's just my understanding

        self.temp_fig, self.temp_ax = plt.subplots()
        self.temp_line, = self.temp_ax.plot(range(0,len(self.temperature_data)), self.temperature_data)
        self.temp_canvas = FigureCanvasTkAgg(self.temp_fig, self.window)
        self.temp_canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew")

        self.pressure_fig, self.pressure_ax = plt.subplots()
        self.pressure_line, = self.pressure_ax.plot(range(len(self.pressure_data)), self.pressure_data)
        self.pressure_canvas = FigureCanvasTkAgg(self.pressure_fig, self.window)
        self.pressure_canvas.get_tk_widget().grid(row=0, column=2, sticky="nsew")

        self.volt_fig, self.volt_ax = plt.subplots()
        self.volt_line, = self.volt_ax.plot(range(len(self.voltage_data)), self.voltage_data)
        self.volt_canvas = FigureCanvasTkAgg(self.volt_fig, self.window)
        self.volt_canvas.get_tk_widget().grid(row=0, column=3, sticky="nsew")

        self.gyro_r_fig, self.gyro_r_ax = plt.subplots()
        self.gyro_r_line, = self.gyro_r_ax.plot(range(len(self.gyro_r_data)), self.gyro_r_data)
        self.gyro_r_canvas = FigureCanvasTkAgg(self.gyro_r_fig, self.window)
        self.gyro_r_canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        self.gyro_p_fig, self.gyro_p_ax = plt.subplots()
        self.gyro_p_line, = self.gyro_p_ax.plot(range(len(self.gyro_p_data)), self.gyro_p_data)
        self.gyro_p_canvas = FigureCanvasTkAgg(self.gyro_p_fig, self.window)
        self.gyro_p_canvas.get_tk_widget().grid(row=1, column=1, sticky="nsew")

        self.gyro_y_fig, self.gyro_y_ax = plt.subplots()
        self.gyro_y_line, = self.gyro_y_ax.plot(range(len(self.gyro_y_data)), self.gyro_y_data)
        self.gyro_y_canvas = FigureCanvasTkAgg(self.gyro_y_fig, self.window)
        self.gyro_y_canvas.get_tk_widget().grid(row=1, column=2, sticky="nsew")

        self.accel_r_fig, self.accel_r_ax = plt.subplots()
        self.accel_r_line, = self.accel_r_ax.plot(range(len(self.accel_r_data)), self.accel_r_data)
        self.accel_r_canvas = FigureCanvasTkAgg(self.accel_r_fig, self.window)
        self.accel_r_canvas.get_tk_widget().grid(row=1, column=3, sticky="nsew")

        self.accel_p_fig, self.accel_p_ax = plt.subplots()
        self.accel_p_line, = self.accel_p_ax.plot(range(len(self.accel_p_data)), self.accel_p_data)
        self.accel_p_canvas = FigureCanvasTkAgg(self.accel_p_fig, self.window)
        self.accel_p_canvas.get_tk_widget().grid(row=2, column=0, sticky="nsew")

        self.accel_y_fig, self.accel_y_ax = plt.subplots()
        self.accel_y_line, = self.accel_y_ax.plot(len(self.accel_y_data), self.accel_y_data)
        self.accel_y_canvas = FigureCanvasTkAgg(self.accel_y_fig, self.window)
        self.accel_y_canvas.get_tk_widget().grid(row=2, column=1, sticky="nsew")

        self.mag_r_fig, self.mag_r_ax = plt.subplots()
        self.mag_r_line, = self.mag_r_ax.plot(len(self.mag_r_data), self.mag_r_data)
        self.mag_r_canvas = FigureCanvasTkAgg(self.mag_r_fig, self.window)
        self.mag_r_canvas.get_tk_widget().grid(row=2, column=2, sticky="nsew")

        self.mag_p_fig, self.mag_p_ax = plt.subplots()
        self.mag_p_line, = self.mag_p_ax.plot(len(self.mag_p_data), self.mag_p_data)
        self.mag_p_canvas = FigureCanvasTkAgg(self.mag_p_fig, self.window)
        self.mag_p_canvas.get_tk_widget().grid(row=2, column=3, sticky="nsew")

        self.mag_y_fig, self.mag_y_ax = plt.subplots()
        self.mag_y_line, = self.mag_y_ax.plot(len(self.mag_y_data), self.mag_y_data)
        self.mag_y_canvas = FigureCanvasTkAgg(self.mag_y_fig, self.window)
        self.mag_y_canvas.get_tk_widget().grid(row=3, column=0, sticky="nsew")

        self.auto_gyro_rotate_rate_fig, self.auto_gyro_rotate_rate_ax = plt.subplots()
        self.auto_gyro_rotate_rate_line, = self.auto_gyro_rotate_rate_ax.plot(len(self.auto_gyro_rotate_rate_data), self.auto_gyro_rotate_rate_data)
        self.auto_gyro_rotate_rate_canvas = FigureCanvasTkAgg(self.auto_gyro_rotate_rate_fig, self.window)
        self.auto_gyro_rotate_rate_canvas.get_tk_widget().grid(row=3, column=1, sticky="nsew")

        self.gps_alt_fig, self.gps_alt_ax = plt.subplots()
        self.gps_alt_line, = self.gps_alt_ax.plot(len(self.gps_altitude_data), self.gps_altitude_data)
        self.gps_alt_canvas = FigureCanvasTkAgg(self.gps_alt_fig, self.window)
        self.gps_alt_canvas.get_tk_widget().grid(row=3, column=2, sticky="nsew")

        self.gps_lat_fig, self.gps_lat_ax = plt.subplots()
        self.gps_lat_line, = self.gps_lat_ax.plot(len(self.gps_latitude_data), self.gps_latitude_data)
        self.gps_lat_canvas = FigureCanvasTkAgg(self.gps_lat_fig, self.window)
        self.gps_lat_canvas.get_tk_widget().grid(row=3, column=3, sticky="nsew")

        self.gps_lon_fig, self.gps_lon_ax = plt.subplots()
        self.gps_lon_line, = self.gps_lon_ax.plot(len(self.gps_longitude_data), self.gps_longitude_data)
        self.gps_lon_canvas = FigureCanvasTkAgg(self.gps_lon_fig, self.window)
        self.gps_lon_canvas.get_tk_widget().grid(row=4, column=0, sticky="nsew")

        self.gps_sats_fig, self.gps_sats_ax = plt.subplots()
        self.gps_sats_line, = self.gps_sats_ax.plot(len(self.gps_sats_data), self.gps_sats_data)
        self.gps_sats_canvas = FigureCanvasTkAgg(self.gps_sats_fig, self.window)
        self.gps_sats_canvas.get_tk_widget().grid(row=4, column=1, sticky="nsew")


        ###### Other random widgets that are needed ######
        self.mission_data = ttk.Frame(self.window)
        self.mission_data.grid(row=4, column=2, sticky="nsew")


        ## UI to send commands, only type the actual command i.e. CXON or ENABLE/ACTIVATE for Simulation ##
        self.command_string = tk.StringVar()
        self.command_entry_label = ttk.Label(self.mission_data, text="Command:")
        self.command_entry_label.pack()
        self.command_entry = ttk.Entry(self.mission_data, textvariable=self.command_string)
        self.command_entry.pack()
        self.command_button = ttk.Button(self.mission_data, text='Send Command', command=self.send_command)
        self.command_button.pack()

        # Command Echo #
        self.command_echo = tk.StringVar(value="None", name="command_echo")
        self.command_echo_label = ttk.Label(self.mission_data, text="Last Command: ", textvariable=self.command_echo)
        self.command_echo_label.pack()

        # Mission Time #
        self.spacer = ttk.Label(self.mission_data)
        self.spacer.pack()
        self.mission_time = ttk.Label(self.mission_data, text="Mission Time")
        self.mission_time.pack()
        self.mission_clock_string = strftime('%H:%M:%S')
        self.mission_clock_lbl = ttk.Label(self.mission_data, text=self.mission_clock_string)
        self.mission_clock_lbl.pack()

        # GPS Time #
        self.spacer2 = ttk.Label(self.mission_data)
        self.spacer2.pack()
        self.gps_time = ttk.Label(self.mission_data, text="GPS Time")
        self.gps_time.pack()
        self.gps_clock_string = self.data['GPS_TIME']
        self.gps_clock_lbl = ttk.Label(self.mission_data, text=self.gps_clock_string)
        self.gps_clock_lbl.pack()

        ## Any notifications that need to be shown ##
        self.info_frame = ttk.Frame(self.window)
        self.info_frame.grid(row=4, column=3, sticky="nsew")

        # Simulation
        self.simulation_enable_label = ttk.Label(self.info_frame, text="Simulation Enable", background="red", font=("Helvetica", 18))
        self.simulation_enable_label.pack()

        self.underlined_font = font.Font(family="Helvetica", size=18, underline=True)
        self.simulation_active_label = ttk.Label(self.info_frame, text="Simulation Active", background="red", font=self.underlined_font)
        self.simulation_active_label.pack()

    # For any commands other than SIM ENABLE/ACTIVATE the booleans should be set true and then the data handler will
    # set them back to false
    def send_command(self):
        command = self.command_entry.get()
        if command != '':
            self.command_echo.set(command) # FIXME : This needs to come from the most recent packet, currently just for debugging

        if (command == "ENABLE"):
            self.sim_on = not self.sim_on
        elif (command == "ACTIVATE" and self.sim_on):
            self.sim_active = not self.sim_active

        elif (command == "CXON"):
            self.can_on = True
        elif (command == "CXOFF"):
            self.can_on = False

        elif (command == "ST GPS"):
            self.set_time_gps = True
        # elif (command == "") FIXME : Find a way to set a custom time to the CanSat

        elif (command == "SIMP" and self.sim_active):
            self.sim_pressure = not self.sim_pressure

        elif (command == "CAL"):
            self.calibrate = True

        elif (command == "MEC"):
            self.mechanism_actuate = True



    # Replace this bullshit with actual data collection from CSV, somehow
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

        if (len(self.pressure_data) >= 5):
            self.pressure_data.pop(0)
            self.pressure_data.append(np.random.randint(0, 20))
        else:
            self.pressure_data.append(np.random.randint(0, 20))

        if (len(self.voltage_data) >= 5):
            self.voltage_data.pop(0)
            self.voltage_data.append(np.random.randint(0, 10))
        else:
            self.voltage_data.append(np.random.randint(0, 10))

        if (len(self.gyro_r_data) >= 5):
            self.gyro_r_data.pop(0)
            self.gyro_r_data.append(np.random.randint(0, 10))
        else:
            self.gyro_r_data.append(np.random.randint(0, 10))

        if (len(self.gyro_p_data) >= 5):
            self.gyro_p_data.pop(0)
            self.gyro_p_data.append(np.random.randint(0, 10))
        else:
            self.gyro_p_data.append(np.random.randint(0, 10))

        if (len(self.gyro_y_data) >= 5):
            self.gyro_y_data.pop(0)
            self.gyro_y_data.append(np.random.randint(0, 10))
        else:
            self.gyro_y_data.append(np.random.randint(0, 10))

        if (len(self.accel_r_data) >= 5):
            self.accel_r_data.pop(0)
            self.accel_r_data.append(np.random.randint(0, 10))
        else:
            self.accel_r_data.append(np.random.randint(0, 10))

        if (len(self.accel_p_data) >= 5):
            self.accel_p_data.pop(0)
            self.accel_p_data.append(np.random.randint(0, 20))
        else:
            self.accel_p_data.append(np.random.randint(0,20))

        if (len(self.accel_y_data) >= 5):
            self.accel_y_data.pop(0)
            self.accel_y_data.append(np.random.randint(0,10))
        else:
            self.accel_y_data.append(np.random.randint(0,10))

        if (len(self.mag_r_data) >= 5):
            self.mag_r_data.pop(0)
            self.mag_r_data.append(np.random.randint(0,10))
        else:
            self.mag_r_data.append(np.random.randint(0,10))

        if (len(self.mag_y_data) >= 5):
            self.mag_y_data.pop(0)
            self.mag_y_data.append(np.random.randint(0,10))
        else:
            self.mag_y_data.append(np.random.randint(0,10))

        if (len(self.mag_p_data) >= 5):
            self.mag_p_data.pop(0)
            self.mag_p_data.append(np.random.randint(0,20))
        else:
            self.mag_p_data.append(np.random.randint(0,10))

        if (len(self.auto_gyro_rotate_rate_data) >= 5):
            self.auto_gyro_rotate_rate_data.pop(0)
            self.auto_gyro_rotate_rate_data.append(np.random.randint(0, 10))
        else:
            self.auto_gyro_rotate_rate_data.append(np.random.randint(0, 10))

        if (len(self.gps_altitude_data) >= 5):
            self.gps_altitude_data.pop(0)
            self.gps_altitude_data.append(np.random.randint(0, 10))
        else:
            self.gps_altitude_data.append(np.random.randint(0, 10))

        if (len(self.gps_latitude_data) >= 5):
            self.gps_latitude_data.pop(0)
            self.gps_latitude_data.append(np.random.randint(0, 10))
        else:
            self.gps_latitude_data.append(np.random.randint(0, 10))

        if (len(self.gps_longitude_data) >= 5):
            self.gps_longitude_data.pop(0)
            self.gps_longitude_data.append(np.random.randint(0, 10))
        else:
            self.gps_longitude_data.append(np.random.randint(0,10))

        if (len(self.gps_sats_data) >= 5):
            self.gps_sats_data.pop(0)
            self.gps_sats_data.append(np.random.randint(0,20))
        else:
            self.gps_sats_data.append(np.random.randint(0,10))

    def draw_plots(self):
        self.alt_canvas.draw()
        self.temp_canvas.draw()
        self.pressure_canvas.draw()
        self.volt_canvas.draw()
        self.gyro_r_canvas.draw()
        self.gyro_p_canvas.draw()
        self.gyro_y_canvas.draw()
        self.accel_r_canvas.draw()
        self.accel_p_canvas.draw()
        self.accel_y_canvas.draw()
        self.mag_r_canvas.draw()
        self.mag_p_canvas.draw()
        self.mag_y_canvas.draw()
        self.auto_gyro_rotate_rate_canvas.draw()
        self.gps_alt_canvas.draw()
        self.gps_lat_canvas.draw()
        self.gps_lon_canvas.draw()
        self.gps_sats_canvas.draw()

    def update_plots(self):
        if (not self.sim_active):
            self.generate_data()

            self.alt_line.set_data(range(len(self.altitude_data)), self.altitude_data)
            self.alt_fig.gca().relim()
            self.alt_fig.gca().autoscale_view()
            self.alt_ax.set_title('Altitude (m)')

            self.temp_line.set_data(range(len(self.temperature_data)), self.temperature_data)
            self.temp_fig.gca().relim()
            self.temp_fig.gca().autoscale_view()
            self.temp_ax.set_title('Temperature (C)')

            self.pressure_line.set_data(range(len(self.pressure_data)), self.pressure_data)
            self.pressure_fig.gca().relim()
            self.pressure_fig.gca().autoscale_view()
            self.pressure_ax.set_title('Pressure (kPa)')

            self.volt_line.set_data(range(len(self.voltage_data)), self.voltage_data)
            self.volt_fig.gca().relim()
            self.volt_fig.gca().autoscale_view()
            self.volt_ax.set_title("Voltage (V)")

            self.gyro_r_line.set_data(range(len(self.gyro_r_data)), self.gyro_r_data)
            self.gyro_r_fig.gca().relim()
            self.gyro_r_fig.gca().autoscale_view()
            self.gyro_r_ax.set_title("Gyro R (m/s)")

            self.gyro_p_line.set_data(range(len(self.gyro_p_data)), self.gyro_p_data)
            self.gyro_p_fig.gca().relim()
            self.gyro_p_fig.gca().autoscale_view()
            self.gyro_p_ax.set_title("Gyro P (m/s)")

            self.gyro_y_line.set_data(range(len(self.gyro_y_data)), self.gyro_y_data)
            self.gyro_y_fig.gca().relim()
            self.gyro_y_fig.gca().autoscale_view()
            self.gyro_y_ax.set_title("Gyro Y (m/s)")

            self.accel_r_line.set_data(range(len(self.accel_r_data)), self.accel_r_data)
            self.accel_r_fig.gca().relim()
            self.accel_r_fig.gca().autoscale_view()
            self.accel_r_ax.set_title("Accel R (m/s)")

            self.accel_p_line.set_data(range(len(self.accel_p_data)), self.accel_p_data)
            self.accel_p_fig.gca().relim()
            self.accel_p_fig.gca().autoscale_view()
            self.accel_p_ax.set_title("Accel P (m/s)")

            self.accel_y_line.set_data(range(len(self.accel_y_data)), self.accel_y_data)
            self.accel_y_fig.gca().relim()
            self.accel_y_fig.gca().autoscale_view()
            self.accel_y_ax.set_title("Accel Y (m/s)")

            self.mag_r_line.set_data(range(len(self.mag_r_data)), self.mag_r_data)
            self.mag_r_fig.gca().relim()
            self.mag_r_fig.gca().autoscale_view()
            self.mag_r_ax.set_title("Roll Magnetometer (Gauss)")

            self.mag_p_line.set_data(range(len(self.mag_p_data)), self.mag_p_data)
            self.mag_p_fig.gca().relim()
            self.mag_p_fig.gca().autoscale_view()
            self.mag_p_ax.set_title("Pitch Magnetometer (Gauss)")

            self.mag_y_line.set_data(range(len(self.mag_y_data)), self.mag_y_data)
            self.mag_y_fig.gca().relim()
            self.mag_y_fig.gca().autoscale_view()
            self.mag_y_ax.set_title("Yaw Magnetometer (Gauss)")

            self.auto_gyro_rotate_rate_line.set_data(range(len(self.auto_gyro_rotate_rate_data)), self.auto_gyro_rotate_rate_data)
            self.auto_gyro_rotate_rate_fig.gca().relim()
            self.auto_gyro_rotate_rate_fig.gca().autoscale_view()
            self.auto_gyro_rotate_rate_ax.set_title('Auto-Gyro Rotate Rate (m/s)')

            self.gps_alt_line.set_data(range(len(self.gps_altitude_data)), self.gps_altitude_data)
            self.gps_alt_fig.gca().relim()
            self.gps_alt_fig.gca().autoscale_view()
            self.gps_alt_ax.set_title('GPS Altitude (m)')

            self.gps_lat_line.set_data(range(len(self.gps_latitude_data)), self.gps_latitude_data)
            self.gps_lat_fig.gca().relim()
            self.gps_lat_fig.gca().autoscale_view()
            self.gps_lat_ax.set_title('GPS Latitude (deg)')

            self.gps_lon_line.set_data(range(len(self.gps_longitude_data)), self.gps_longitude_data)
            self.gps_lon_fig.gca().relim()
            self.gps_lon_fig.gca().autoscale_view()
            self.gps_lon_ax.set_title('GPS Longitude (deg)')

            self.gps_sats_line.set_data(range(len(self.gps_sats_data)), self.gps_sats_data)
            self.gps_sats_fig.gca().relim()
            self.gps_sats_fig.gca().autoscale_view()
            self.gps_sats_ax.set_title('GPS Satellites')

        if (self.sim_on):
            self.simulation_enable_label.pack()
        else:
            self.simulation_enable_label.pack_forget()

        if (self.sim_on and self.sim_active):
            self.simulation_active_label.pack()
        else:
            self.simulation_active_label.pack_forget()

        # Mission Clock
        self.mission_clock_string = strftime('%H :%M:%S')
        hour = int(self.mission_clock_string[0:2])
        rest_of_clock = self.mission_clock_string[2:]
        if (hour < 12):
            hour += 12
        hour += 5
        hour = hour % 24
        if (hour == 0):
            self.mission_clock_string = '00' + rest_of_clock
        else:
            self.mission_clock_string = str(hour) + rest_of_clock

        self.mission_clock_lbl.config(text=self.mission_clock_string)

        # GPS Clock
        # self.gps_clock_string = self.data['GPS_TIME']   FIXME : Re-enable this code once GPS Time is real
        # hour = int(self.gps_clock_string[0:2])
        # rest_of_clock = self.gps_clock_string[2:]
        # hour += 5
        # hour = hour % 24
        # self.gps_clock_string = str(hour) + rest_of_clock
        #
        # self.gps_clock_lbl.config(text=self.gps_clock_string)

        self.draw_plots()
        self.window.after(1, self.update_plots)

    def create_grid(self):
        grid = 5
        for i in range(0,grid):
            self.window.grid_rowconfigure(i, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_columnconfigure(3, weight=1)
        

    def gui(self):
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (width, height))
        self.create_grid()

        self.window.after(500, self.update_plots)
        self.window.mainloop()

ground = Ground_Station()
ground.gui()
