import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import numpy as np

# Create a Tkinter window
window = tk.Tk()
window.title("Real-time Graph")

# Create a Matplotlib figure
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)

# Initialize empty lists for x and y data
x_data = []
y_data = []

# Function to generate random data
def generate_data():
    if (x_data.__len__() >= 5): # General array length limitations
        x_data[0] = x_data[1]
        x_data[1] = x_data[2]
        x_data[2] = x_data[3]
        x_data[3] = x_data[4]
        x_data[4] = x_data[4] + 1

        y_data[0] = y_data[1]
        y_data[1] = y_data[2]
        y_data[2] = y_data[3]
        y_data[3] = y_data[4]
        y_data[4] = np.random.randint(0, 10)
    else:
        x_data.append(len(x_data))
        y_data.append(np.random.randint(0, 10))

# Function to update the graph
def animate(i):
    generate_data()
    ax.clear()
    ax.plot(x_data, y_data)

# Create a canvas to embed the Matplotlib figure in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Start the animation
ani = animation.FuncAnimation(fig, animate, interval=1000)

# Start the Tkinter event loop
window.mainloop()