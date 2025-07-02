import pandas as pd
import numpy as np

# ruta a tu archivo
csv_file = r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\results.csv"

# parsear el fichero como antes
def parse_solutions(txt_file):
    with open(txt_file, encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    data = []
    current = {}
    for line in lines:
        line = line.strip()
        if line.startswith("---"):
            if current:
                data.append(current)
                current = {}
        elif ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            try:
                value = float(value.strip())
            except:
                value = None
            current[key] = value
    if current:
        data.append(current)

    return pd.DataFrame(data)

# leer
df = parse_solutions(csv_file)

# quitar NaNs
df_clean = df.dropna(subset=["Peso"])

# ordenar por peso
df_sorted = df_clean.sort_values(by="Peso").reset_index(drop=True)

# pesos extremos
peso_min = df_sorted.iloc[0]["Peso"]
peso_max = df_sorted.iloc[-1]["Peso"]

# puntos intermedios equidistantes
targets = np.linspace(peso_min, peso_max, 5)

# buscar la fila más cercana a cada target
selected_indices = []
for t in targets:
    idx = (df_sorted["Peso"] - t).abs().idxmin()
    selected_indices.append(idx)

# sacar las 5 soluciones
five_solutions = df_sorted.loc[selected_indices].reset_index(drop=True)

# guardar CSV
five_solutions.to_csv(r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\five_solutions.csv", index=False)

print("✅ Archivo five_solutions.csv generado con las 5 soluciones seleccionadas.")
