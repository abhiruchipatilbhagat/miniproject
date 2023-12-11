import tkinter as tk
from tkinter import ttk
import psutil
import GPUtil

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")

        # CPU usage
        self.cpu_label = ttk.Label(root, text="CPU Usage:")
        self.cpu_label.grid(row=0, column=0, padx=10, pady=5, sticky="W")

        # GPU usage
        self.gpu_label = ttk.Label(root, text="GPU Usage:")
        self.gpu_label.grid(row=1, column=0, padx=10, pady=5, sticky="W")

        # memory usage
        self.memory_label = ttk.Label(root, text="Memory Usage:")
        self.memory_label.grid(row=2, column=0, padx=10, pady=5, sticky="W")

        # dropdown to select interval
        self.dropdown = ttk.Combobox(
            state="readonly",
            values=[0.1, 0.5, 1, 5, 10],
        )
        self.dropdown.grid(row=3, column=0, padx=10, pady=5, sticky="W")
        self.dropdown.set(1)

        # set up the automatic refresh
        self.update_data()

    def update_data(self):
        interval = float(self.dropdown.get())

        # get CPU usage
        cpu_percent = psutil.cpu_percent(interval=interval)
        self.cpu_label.config(text=f"CPU Usage: {cpu_percent}%")

        # get GPU usage
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_percent = gpus[0].load * 100
                self.gpu_label.config(text=f"GPU Usage: {gpu_percent:.2f}%")
            else:
                self.gpu_label.config(text="GPU Usage: N/A (No GPU detected)")
        except Exception as e:
            print(f"Error getting GPU usage: {e}")
            self.gpu_label.config(text="GPU Usage: N/A")

        # get RAM usage
        memory_info = psutil.virtual_memory()
        self.memory_label.config(text=f"Memory Usage: {memory_info.percent}%")

        # set up the next automatic refresh
        self.root.after(int(interval * 1000), self.update_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()
