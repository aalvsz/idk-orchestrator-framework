import pandas as pd
import numpy as np

def pick_5():
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


def rangos():
    import pandas as pd

    # ruta a tu csv
    csv_file = r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\neural_network_01-07-2025-14-41\data\outputs.csv"

    # cargar el csv
    df = pd.read_csv(csv_file)

    # calcular min y max por columna
    min_values = df.min()
    max_values = df.max()

    # unir resultados en un solo DataFrame
    summary_df = pd.DataFrame({
        "min": min_values,
        "max": max_values
    })

    # guardar a csv
    summary_df.to_csv(r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\neural_network_01-07-2025-14-41\data\min_max_summary.csv")

    print("Resumen de valores min/max generado correctamente.")

def calculo_error():
    import pandas as pd

    # rutas
    pred_file = r"D:\idk_framework\idkROM\src\results\neural_network_04-07-2025-12-16\predicciones_test.csv"
    true_file = r"D:\idk_framework\idkROM\src\results\neural_network_04-07-2025-12-16\valores_esperados_test.csv"
    ranges_file = r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\neural_network_01-07-2025-14-41\data\min_max_summary.csv"

    # leer csvs
    df_pred = pd.read_csv(pred_file)
    df_true = pd.read_csv(true_file)
    df_ranges = pd.read_csv(ranges_file, index_col=0)

    # comprobar que columnas coinciden
    assert all(df_pred.columns == df_true.columns), "Predicciones y esperados deben tener las mismas columnas"

    # dataframe donde guardaremos errores normalizados
    df_error = pd.DataFrame()

    for col in df_pred.columns:
        min_val = df_ranges.loc[col, "min"]
        max_val = df_ranges.loc[col, "max"]
        range_val = max_val - min_val
        
        # evita división por cero
        if range_val == 0:
            range_val = 1e-12

        df_error[col] = (df_pred[col] - df_true[col]) / range_val

    # guardar a CSV
    output_file = r"D:\idk_framework\idkROM\src\results\neural_network_04-07-2025-12-16\errores_normalizados.csv"
    df_error.to_csv(output_file, index=False)

    print(f"Errores normalizados guardados en {output_file}")

def plot_error_frecuencia():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    # === rutas ===
    error_csv = r"D:\idk_framework\idkROM\src\results\neural_network_04-07-2025-12-16\errores_normalizados.csv"

    # leer errores
    df_error = pd.read_csv(error_csv)

    # calcular medias
    mean_errors = df_error.mean()

    # ===  histograma general de todos los errores mezclados ===
    plt.figure(figsize=(10,6))
    sns.histplot(df_error.values.flatten(), bins=50, kde=True, color="steelblue")
    plt.xlabel("Error normalizado")
    plt.ylabel("Frecuencia")
    plt.title("Distribución de todos los errores normalizados")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

plot_error_frecuencia()