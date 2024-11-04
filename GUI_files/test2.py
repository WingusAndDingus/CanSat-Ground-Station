import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


# Function to update the plots
def update_plot():
    global x, line1, line2

    # Get the frequency values from the sliders
    freq1 = frequency_slider1.get()
    freq2 = frequency_slider2.get()

    # Update the data for each plot
    y1 = np.sin(2 * np.pi * freq1 * x)
    y2 = np.cos(2 * np.pi * freq2 * x)

    line1.set_ydata(y1)
    line2.set_ydata(y2)

    # Redraw the canvas
    canvas.draw()

    # Call this function again after 50 milliseconds (for real-time effect)
    window.after(50, update_plot)


# Create the main window
window = tk.Tk()
window.title("Real-time Multiple Plots")
window.geometry("600x600")

# Create a Matplotlib figure
fig, ax = plt.subplots()
x = np.linspace(0, 2 * np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create two plot lines
line1, = ax.plot(x, y1, label="Sine Wave")
line2, = ax.plot(x, y2, label="Cosine Wave")

ax.set_ylim(-1.5, 1.5)
ax.set_xlim(0, 2 * np.pi)
ax.legend()

# Add Matplotlib figure to Tkinter window
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Add sliders for controlling the frequencies of both plots
ttk.Label(window, text="Frequency for Sine Wave").pack()
frequency_slider1 = tk.Scale(window, from_=0.5, to=5.0, resolution=0.1, orient=tk.HORIZONTAL)
frequency_slider1.pack()

ttk.Label(window, text="Frequency for Cosine Wave").pack()
frequency_slider2 = tk.Scale(window, from_=0.5, to=5.0, resolution=0.1, orient=tk.HORIZONTAL)
frequency_slider2.pack()

# Start the update loop for real-time plotting using 'after'
window.after(100, update_plot)

# Start the Tkinter event loop
window.mainloop()
