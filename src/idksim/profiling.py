import psutil
import time
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd

def monitor_memory(interval=1.0, output_file="memory_usage.csv"):
    start_time = time.time()
    pid = os.getpid()  # PID del proceso principal
    process = psutil.Process(pid)

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Time (s)", "RAM Used (MB)"])

        while True:
            try:
                elapsed = time.time() - start_time
                mem = process.memory_info().rss / (1024 ** 2)  # Convertir a MB
                writer.writerow([elapsed, mem])
                time.sleep(interval)
            except Exception:
                break


def memory_usage_plot(csv_to_plot):
    df = pd.read_csv(csv_to_plot)

    plt.plot(df["Time (s)"], df["RAM Used (MB)"], label="RAM usada")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Memoria RAM (MB)")
    plt.title("Uso de RAM durante el DOE")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("ram_vs_time.png")
    plt.show()
