import tkinter as tk
from tkinter import ttk
import psutil
import GPUtil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")

        # Labels for CPU, GPU, and memory usage
        self.cpu_label = ttk.Label(root, text="CPU Usage:")
        self.cpu_label.grid(row=0, column=0, padx=10, pady=5, sticky="W")

        self.gpu_label = ttk.Label(root, text="GPU Usage:")
        self.gpu_label.grid(row=1, column=0, padx=10, pady=5, sticky="W")

        self.memory_label = ttk.Label(root, text="Memory Usage:")
        self.memory_label.grid(row=2, column=0, padx=10, pady=5, sticky="W")

        # Dropdown to select the refresh interval
        self.dropdown = ttk.Combobox(
            state="readonly",
            values=[0.1, 0.5, 1, 5, 10],
        )
        self.dropdown.grid(row=3, column=0, padx=10, pady=5, sticky="W")
        self.dropdown.set(1)

        # Set up the automatic refresh and initial plot
        self.update_data()
        self.plot_cpu_memory()

    def update_data(self):
        # Function to update system data based on the selected interval

        # Get the interval value from the dropdown and convert it to a float
        interval = float(self.dropdown.get())

        # Get CPU usage
        cpu_percent = psutil.cpu_percent(interval=interval)
        self.cpu_label.config(text=f"CPU Usage: {cpu_percent}%")

        try:
            # Get GPU usage if available
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_percent = gpus[0].load * 100
                self.gpu_label.config(text=f"GPU Usage: {gpu_percent:.2f}%")
            else:
                self.gpu_label.config(text="GPU Usage: N/A (No GPU detected)")
        except Exception as e:
            print(f"Error getting GPU usage: {e}")
            self.gpu_label.config(text="GPU Usage: N/A")

        # Get memory usage
        memory_info = psutil.virtual_memory()
        self.memory_label.config(text=f"Memory Usage: {memory_info.percent}%")

        # Set up the next automatic refresh
        self.root.after(int(interval * 1000), self.update_data)

    def plot_cpu_memory(self):
        # Function to plot CPU and memory usage over time

        # Get historical CPU and memory usage
        cpu_history = []
        memory_history = []

        for _ in range(60):  # Collect data for the last 60 seconds
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent

            cpu_history.append(cpu_percent)
            memory_history.append(memory_percent)

        # Plot CPU usage
        fig, ax1 = plt.subplots(figsize=(8, 3))
        ax1.plot(cpu_history, label='CPU Usage', color='blue')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('CPU Usage (%)', color='blue')
        ax1.tick_params('y', colors='blue')

        # Create a second y-axis for memory usage
        ax2 = ax1.twinx()
        ax2.plot(memory_history, label='Memory Usage', color='red')
        ax2.set_ylabel('Memory Usage (%)', color='red')
        ax2.tick_params('y', colors='red')

        # Combine legends from both axes
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper left')

        # Display the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="W")

        # Set up the next automatic refresh for the plot
        self.root.after(5000, self.plot_cpu_memory)


if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()
