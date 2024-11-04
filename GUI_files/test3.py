import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


# Function to update the plots
def update_plot():
    # Get frequency from the sliders
    freq1 = frequency_slider1.get()
    freq2 = frequency_slider2.get()

    # Update the sine plot
    y1 = np.sin(2 * np.pi * freq1 * x)
    line1.set_ydata(y1)
    canvas1.draw()

    # Update the cosine plot
    y2 = np.cos(2 * np.pi * freq2 * x)
    line2.set_ydata(y2)
    canvas2.draw()

    # Call update_plot again after 100 ms
    window.after(100, update_plot)


# Create main window
window = tk.Tk()
window.title("Multiple Embedded Graphs")
window.geometry("800x600")

# Data setup for x-axis
x = np.linspace(0, 2 * np.pi, 100)

# --- First Graph: Sine Wave ---
fig1, ax1 = plt.subplots()
y1 = np.sin(x)  # Initial sine wave values
line1, = ax1.plot(x, y1, color="blue")
ax1.set_title("Sine Wave")
ax1.set_ylim(-1.5, 1.5)
ax1.set_xlim(0, 2 * np.pi)

# Embed first plot in Tkinter
canvas1 = FigureCanvasTkAgg(fig1, master=window)
canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# --- Second Graph: Cosine Wave ---
fig2, ax2 = plt.subplots()
y2 = np.cos(x)  # Initial cosine wave values
line2, = ax2.plot(x, y2, color="red")
ax2.set_title("Cosine Wave")
ax2.set_ylim(-1.5, 1.5)
ax2.set_xlim(0, 2 * np.pi)

# Embed second plot in Tkinter
canvas2 = FigureCanvasTkAgg(fig2, master=window)
canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# --- Add Sliders to Control Frequencies ---
ttk.Label(window, text="Frequency for Sine Wave").pack()
frequency_slider1 = tk.Scale(window, from_=0.5, to=5.0, resolution=0.1, orient=tk.HORIZONTAL)
frequency_slider1.pack()

ttk.Label(window, text="Frequency for Cosine Wave").pack()
frequency_slider2 = tk.Scale(window, from_=0.5, to=5.0, resolution=0.1, orient=tk.HORIZONTAL)
frequency_slider2.pack()

# Start updating the plots
window.after(100, update_plot)

# Run the Tkinter event loop
window.mainloop()
