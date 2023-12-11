import tkinter as tk
from tkinter import ttk
import psutil
import GPUtil

class SystemMonitorApp:
    def __init__(self, root):
        # Initialize the application with the main Tkinter window
        self.root = root
        self.root.title("System Monitor")  # Set the title of the window

        # Create labels to display CPU, GPU, and memory usage
        self.cpu_label = ttk.Label(root, text="CPU Usage:")
        self.cpu_label.grid(row=0, column=0, padx=10, pady=5, sticky="W")

        self.gpu_label = ttk.Label(root, text="GPU Usage:")
        self.gpu_label.grid(row=1, column=0, padx=10, pady=5, sticky="W")

        self.memory_label = ttk.Label(root, text="Memory Usage:")
        self.memory_label.grid(row=2, column=0, padx=10, pady=5, sticky="W")

        # Create a dropdown menu to select the refresh interval
        self.dropdown = ttk.Combobox(
            state="readonly",
            values=[0.1, 0.5, 1, 5, 10],
        )
        self.dropdown.grid(row=3, column=0, padx=10, pady=5, sticky="W")
        self.dropdown.set(1)  # Set the default interval to 1 second

        # Set up the automatic refresh of system data
        self.update_data()

    def update_data(self):
        # Function to update system data based on the selected interval

        # Get the interval value from the dropdown and convert it to a float
        interval = float(self.dropdown.get())

        # Get and display CPU usage
        cpu_percent = psutil.cpu_percent(interval=interval)
        self.cpu_label.config(text=f"CPU Usage: {cpu_percent}%")

        try:
            # Get and display GPU usage if available
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_percent = gpus[0].load * 100
                self.gpu_label.config(text=f"GPU Usage: {gpu_percent:.2f}%")
            else:
                self.gpu_label.config(text="GPU Usage: N/A (No GPU detected)")
        except Exception as e:
            print(f"Error getting GPU usage: {e}")
            self.gpu_label.config(text="GPU Usage: N/A")

        # Get and display RAM usage
        memory_info = psutil.virtual_memory()
        self.memory_label.config(text=f"Memory Usage: {memory_info.percent}%")

        # Set up the next automatic refresh based on the selected interval
        self.root.after(int(interval * 1000), self.update_data)

if __name__ == "__main__":
    # Create the Tkinter window and start the event loop
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()
