import psutil
import time
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd

def monitor_memory(interval=1.0, output_file="memory_usage.csv"):
    """
    Monitorea el uso de memoria RAM del proceso actual y guarda los datos en un archivo CSV.

    Args:
        interval (float): Intervalo de muestreo en segundos entre cada medición de memoria.
        output_file (str): Nombre del archivo CSV donde se guardarán los datos de uso de memoria.

    El archivo CSV generado contendrá dos columnas:
        - "Time (s)": Tiempo transcurrido en segundos desde el inicio del monitoreo.
        - "RAM Used (MB)": Memoria RAM utilizada por el proceso (en megabytes).

    El monitoreo se detiene si ocurre una excepción (por ejemplo, interrupción manual).
    """
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
    """
    Genera y guarda un gráfico del uso de memoria RAM a lo largo del tiempo a partir de un archivo CSV.

    Args:
        csv_to_plot (str): Ruta al archivo CSV generado por monitor_memory().

    El gráfico muestra la memoria RAM utilizada (en MB) en función del tiempo (en segundos).
    El resultado se guarda como 'ram_vs_time.png' y también se muestra en pantalla.
    """
    df = pd.read_csv(csv_to_plot)

    plt.plot(df["Time (s)"], df["RAM Used (MB)"], label="RAM usada")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Memoria RAM (MB)")
    plt.title("Uso de RAM durante el DOE")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("ram_vs_time.png")