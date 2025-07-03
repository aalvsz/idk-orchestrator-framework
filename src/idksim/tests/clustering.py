import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# lee tu archivo
df = pd.read_csv(r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\soluciones_pareto_final.csv")

# identifica las columnas de output
output_x = "Peso"
output_y = "elastic_energy"

# identificamos la columna para cluster
cluster_col = "N_trans"

# creamos el plot
plt.figure(figsize=(10,8))

# usar seaborn para colorear automáticamente
sns.scatterplot(
    data=df,
    x=output_x,
    y=output_y,
    hue=cluster_col,
    palette="tab10",
    s=100,
    edgecolor="k"
)

plt.title(f"Clusters según N_trans en el espacio de [{output_x}] vs [{output_y}]")
plt.xlabel(output_x)
plt.ylabel(output_y)
plt.grid(True)
plt.legend(title="N_trans")
plt.show()
