import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cdist
import logging
import os

def setup_logger(log_path):
    """
    Configura un logger que escribe a un archivo y también a consola
    """
    logger = logging.getLogger("postproc_logger")
    logger.setLevel(logging.INFO)

    # Limpia handlers previos
    if logger.hasHandlers():
        logger.handlers.clear()

    # Handler a archivo
    fh = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    fh.setLevel(logging.INFO)

    # Handler a consola
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


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
            val_str = value.strip()
            try:
                val = float(val_str)
            except:
                val = None
            current[key] = val
    if current:
        data.append(current)

    return pd.DataFrame(data)


def cluster_inputs(df, n_clusters, logger):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df_clean = df.fillna(0)
    labels = kmeans.fit_predict(df_clean)

    df_cluster = df_clean.copy()
    df_cluster['cluster'] = labels

    centers = pd.DataFrame(kmeans.cluster_centers_, columns=df.columns)
    silhouette = silhouette_score(df_clean, labels)
    inertia = kmeans.inertia_
    counts = pd.Series(labels).value_counts()

    dists = cdist(df_clean, centers)

    logger.info(f"✅ Silhouette score: {silhouette:.4f}")
    logger.info(f"✅ Inercia (SSE): {inertia:.4f}")
    logger.info(f"✅ Tamaños de clusters:\n{counts}")
    logger.info(f"✅ Distancias mínimas a centroides: {dists.min(axis=0)}")
    logger.info(f"✅ Distancias máximas a centroides: {dists.max(axis=0)}")

    return df_cluster, centers


def analyze_correlations(df_inputs, df_targets, logger):
    corr_results = {}
    for output in df_targets.columns:
        corr_with_output = df_inputs.corrwith(df_targets[output])
        corr_results[output] = corr_with_output
        logger.info(f"\n✅ Correlaciones con {output}:")
        logger.info(corr_with_output.sort_values(key=lambda x: abs(x), ascending=False))
    return corr_results


def main():
    txt_file = r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\results.csv"
    output_folder = r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica"
    os.makedirs(output_folder, exist_ok=True)

    # logger
    log_path = os.path.join(output_folder, "logs_postproc.txt")
    logger = setup_logger(log_path)

    df = parse_solutions(txt_file)

    input_cols = [c for c in df.columns if c not in ["Peso", "elastic_energy"]]
    inputs_df = df[input_cols]
    outputs_df = df[["Peso", "elastic_energy"]]

    """clustered_df, centers = cluster_inputs(inputs_df, n_clusters=3, logger=logger)
    clustered_df.to_csv(os.path.join(output_folder, "inputs_clustered.csv"), index=False)
    logger.info("✅ Archivo clustered guardado como inputs_clustered.csv")"""

    analyze_correlations(inputs_df.fillna(0), outputs_df, logger)

    logger.info("✅ Proceso terminado correctamente.")

def main2():
    import csv
    import re

    # Cambia esto por la ruta real de tu archivo
    input_file = r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\results.csv"
    output_file = r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\soluciones_pareto_final.csv"

    # lista de campos de entrada
    input_fields = [
        "t_front", "t_rear", "t_top", "t_bottom", "t_lateral",
        "t1_long", "t2_long", "h_long", "t1_trans", "t2_trans",
        "inc_t_trans", "d_t_trans", "K_trans", "ang_Z", "D", "N_trans"
    ]

    # lista de campos de salida (objetivos)
    output_fields = ["Peso", "elastic_energy"]

    # combinamos todos para el header
    all_fields = input_fields + output_fields

    # lista donde se guardarán las filas
    rows = []

    with open(input_file, "r") as f:
        content = f.read()

    # divide cada solución
    solutions = re.split(r"--- Solución \d+ ---", content)

    for sol in solutions:
        if sol.strip() == "":
            continue  # descarta textos vacíos
        row = []
        for field in input_fields:
            match = re.search(rf"{field}:\s*([-+eE0-9\.]+)", sol)
            if match:
                row.append(float(match.group(1)))
            else:
                row.append(None)  # si falta, poner None
        # objetivos
        for field in output_fields:
            match = re.search(rf"{field}:\s*([-+eE0-9\.]+)", sol)
            if match:
                row.append(float(match.group(1)))
            else:
                row.append(None)
        rows.append(row)

    # guardar en CSV
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(all_fields)
        writer.writerows(rows)

    print(f"Archivo CSV generado correctamente con {len(rows)} filas en {output_file}")


if __name__ == "__main__":
    main()
