import pandas as pd
import matplotlib.pyplot as plt

# Carga tu CSV de Pareto
df = pd.read_csv(r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\soluciones_pareto_final.csv")

# lista de tus 16 variables de entrada
inputs = [
    "t_front", "t_rear", "t_top", "t_bottom", "t_lateral",
    "t1_long", "t2_long", "h_long", "t1_trans", "t2_trans",
    "inc_t_trans", "d_t_trans", "K_trans", "ang_Z", "D", "N_trans"
]

# define tamaño de la cuadrícula de gráficos
ncols = 4
nrows = (len(inputs) + ncols - 1) // ncols

# figura más compacta
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(12, 3 * nrows))

for i, var in enumerate(inputs):
    ax = axes[i // ncols, i % ncols]
    ax.hist(df[var], bins=20, color="steelblue", edgecolor="black")
    ax.set_title(f"Histograma de {var}", fontsize=9)
    ax.set_ylabel("Frecuencia", fontsize=8)
    ax.tick_params(axis='both', which='major', labelsize=8)

# quita ejes vacíos si sobran
for j in range(len(inputs), ncols * nrows):
    fig.delaxes(axes[j // ncols, j % ncols])

plt.tight_layout()
plt.show()
