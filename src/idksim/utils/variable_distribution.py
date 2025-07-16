import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# carga los datos
df = pd.read_csv(r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\soluciones_pareto_final.csv")

plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x="Peso", y="d_t_trans", color="steelblue", s=80, edgecolor="k")
plt.title("Relación entre Peso y d_t_trans")
plt.xlabel("Peso")
plt.ylabel("d_t_trans")
plt.grid(True)
plt.show()


plt.figure(figsize=(10,6))
sns.kdeplot(
    x=df["Peso"],
    y=df["d_t_trans"],
    cmap="Blues",
    fill=True,
    thresh=0.05
)
plt.title("Densidad conjunta de Peso y d_t_trans")
plt.xlabel("Peso")
plt.ylabel("d_t_trans")
plt.grid(True)
plt.show()
