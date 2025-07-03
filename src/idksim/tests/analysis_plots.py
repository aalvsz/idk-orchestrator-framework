import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# cargar tus datos
df = pd.read_csv(r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\soluciones_pareto_final.csv")

# por ejemplo, definimos terciles del output "Peso"
df['Peso_bin'] = pd.qcut(df['Peso'], q=3, labels=["bajo", "medio", "alto"])

# plot histogramas/KDE de todas las features agrupadas por Peso_bin
for col in df.columns:
    if col not in ["Peso", "elastic_energy", "Peso_bin"]:
        plt.figure(figsize=(8,4))
        sns.histplot(data=df, x=col, hue="Peso_bin", kde=True, stat="density", common_norm=False)
        plt.title(f"Distribución de {col} según terciles de Peso")
        plt.show()


