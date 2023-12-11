import tkinter as tk
from tkinter import ttk
import psutil


class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")

        # CPU usage
        self.cpu_label = ttk.Label(root, text="CPU Usage:")
        self.cpu_label.grid(row=0, column=0, padx=10, pady=5, sticky="W")

        # memory usage
        self.memory_label = ttk.Label(root, text="Memory Usage:")
        self.memory_label.grid(row=1, column=0, padx=10, pady=5, sticky="W")

        # network shit
        self.network_label = ttk.Label(root, text="Network statistics")
        self.network_label.grid(row=2, column=0)

        self.bytes_sent = ttk.Label(root, text="Bytes sent: ")
        self.bytes_sent.grid(row=3, column=1, padx=20)

        self.bytes_recieved = ttk.Label(root, text="Bytes Recieved: ")
        self.bytes_recieved.grid(row=3, column=2)

        # dropdown to select interval
        self.dropdown = ttk.Combobox(
            state="readonly",
            # values=["100ms", "500ms", "1s", "5s", "10s"],
            values=[0.1, 0.5, 1, 5, 10],
            )
        self.dropdown.grid(row=4, column=1)
        self.dropdown.set(5)
        # button to refresh data
        self.refresh_button = ttk.Button(root, text="Refresh", command=self.update_data)  # noqa: E501
        self.refresh_button.grid(row=4, column=3, padx=10, pady=10, sticky="W")

        # call the initial update
        self.update_data()

    def update_data(self):
        interval = float(self.dropdown.get())

        # get CPU usage
        cpu_percent = psutil.cpu_percent(interval=interval)
        self.cpu_label.config(text=f"CPU Usage: {cpu_percent}%")

        # get RAM usage
        memory_info = psutil.virtual_memory()
        self.memory_label.config(text=f"Memory Usage: {memory_info.percent}%")

        # get network information for a specific network interface
        interface_name = "eth0"  # Replace with your desired network interface
        bytes_info = psutil.net_io_counters(pernic=True).get(interface_name, None)

        if bytes_info:
            self.bytes_sent.config(text=f"Bytes Sent: {bytes_info.bytes_sent} bytes")
            self.bytes_received.config(text=f"Bytes Received: {bytes_info.bytes_recv} bytes")

        # Note: You need to handle the case when 'bytes_info' is None or when the interface is not available.



if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()
