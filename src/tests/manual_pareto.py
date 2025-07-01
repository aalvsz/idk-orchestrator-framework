import pandas as pd
import matplotlib.pyplot as plt

def parse_pareto_from_txt(txt_file):
    """
    Extrae las parejas (Peso, elastic_energy) desde el archivo de texto
    """
    pareto_points = []
    with open(txt_file, encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    
    peso = None
    energy = None
    for line in lines:
        line = line.strip()
        if line.startswith("Peso:"):
            try:
                peso = float(line.split(":")[1].strip())
            except:
                peso = None
        elif line.startswith("elastic_energy:"):
            try:
                energy = float(line.split(":")[1].strip())
            except:
                energy = None
        if peso is not None and energy is not None:
            pareto_points.append( (peso, energy) )
            peso = None
            energy = None
    
    return pareto_points


# ==== config ====

def main():
    csv_file = r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\outputs.csv"
    txt_file = r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\results.csv"
    csv_pareto_real = r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\real_pareto.csv"

    # coordenadas del punto nominal
    nominal_point=(9821.927253772777, 1.320873466836539)

    # === leer CSV con todos los puntos ===
    df = pd.read_csv(csv_file)

    # leer CSV con frente de Pareto real
    pareto_real_df = pd.read_csv(csv_pareto_real, sep=";")  # ojo: separador punto y coma

    # verificar columnas
    if "obj_1" not in df.columns or "obj_2" not in df.columns:
        raise ValueError("El CSV inicial debe tener columnas 'obj_1' y 'obj_2'.")

    if not all(c in pareto_real_df.columns for c in ["Peso", "elastic_energy"]):
        raise ValueError("El CSV de Pareto real debe tener columnas 'Peso' y 'elastic_energy'.")

    # extraer puntos de Pareto del archivo de texto
    pareto_points = parse_pareto_from_txt(txt_file)

    # marcar qué filas del CSV son pareto
    is_pareto = df.apply(
        lambda row: any( abs(row["obj_1"] - p[0]) < 1e-6 and abs(row["obj_2"] - p[1]) < 1e-6 for p in pareto_points ),
        axis=1
    )

    # dividir
    pareto_df = df[is_pareto]
    dominated_df = df[~is_pareto]

    # plot
    plt.figure(figsize=(10,7))
    plt.scatter(dominated_df["obj_1"], dominated_df["obj_2"], c="gray", alpha=0.5, label="Dominadas")
    plt.scatter(pareto_df["obj_1"], pareto_df["obj_2"], c="blue", marker="o", label="Pareto encontrado")

    # frente de Pareto real (naranja)
    if not pareto_real_df.empty:
        plt.scatter(
            pareto_real_df["Peso"],
            pareto_real_df["elastic_energy"],
            c="orange", marker="s", s=40, edgecolors="black", label="FRENTE DE PARETO REAL"
        )

    # punto nominal
    plt.scatter(
        nominal_point[0],
        nominal_point[1],
        c="red", s=100, marker="*", edgecolors="black", label="Punto nominal"
    )

    plt.xlabel("Peso (obj_1)")
    plt.ylabel("elastic_energy (obj_2)")
    plt.title("Frente de Pareto resaltado + Pareto real + Punto nominal")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\pareto_plot.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
