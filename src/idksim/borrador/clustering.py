import pandas as pd
import matplotlib
matplotlib.use("Agg")  # para renderizar a archivo (PNG, etc.) sin GUI

import matplotlib.pyplot as plt
import seaborn as sns

# lee tu archivo
df = pd.read_csv(r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\soluciones_pareto_final.csv")
outputs = ["Peso", "elastic_energy"]
inputs = [c for c in df.columns if c not in outputs]

def clustering1():
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


def clustering_kmeans():
    from sklearn.cluster import KMeans

    kmeans = KMeans(n_clusters=3, random_state=42)
    df['cluster_kmeans'] = kmeans.fit_predict(df[inputs])

    import matplotlib.pyplot as plt

    plt.figure(figsize=(8,6))
    for cluster in df['cluster_kmeans'].unique():
        subset = df[df['cluster_kmeans'] == cluster]
        plt.scatter(subset[outputs[0]], subset[outputs[1]], label=f"cluster {cluster}")
    plt.xlabel(outputs[0])
    plt.ylabel(outputs[1])
    plt.title("KMeans clustering sobre Pareto")
    plt.legend()
    plt.show()


def clustering_dbscan():
    from sklearn.cluster import DBSCAN
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[inputs])

    dbscan = DBSCAN(eps=1.5, min_samples=5)
    df['cluster_dbscan'] = dbscan.fit_predict(X_scaled)

    plt.figure(figsize=(8,6))
    for cluster in df['cluster_dbscan'].unique():
        subset = df[df['cluster_dbscan'] == cluster]
        plt.scatter(subset[outputs[0]], subset[outputs[1]], label=f"cluster {cluster}")
    plt.xlabel(outputs[0])
    plt.ylabel(outputs[1])
    plt.title("DBSCAN clustering sobre Pareto")
    plt.legend()
    plt.show()


def parallel_coords():
    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler(feature_range=(-1, 1))
    inputs_scaled = pd.DataFrame(scaler.fit_transform(df[inputs]), columns=inputs)
    inputs_scaled['cluster'] = df['cluster_kmeans']

    from pandas.plotting import parallel_coordinates

    plt.figure(figsize=(14,8))
    parallel_coordinates(inputs_scaled, 'cluster', colormap=plt.cm.tab10)
    plt.title("Parallel Coordinates (inputs escalados -1 a 1)")
    plt.xticks(rotation=90)
    plt.show()


def heatmap_correlacioens():
    corr = df[inputs + outputs].corr()

    plt.figure(figsize=(14,10))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Heatmap de correlaciones")
    plt.show()


def custom_clustering():
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    # Variable sobre la que segmentar
    target_var = "d_t_trans"   # cámbialo por la que quieras

    # Calcular cuantiles
    quantiles = df[target_var].quantile([0.25, 0.5, 0.75]).values

    # Asignar cluster
    def assign_cluster(val):
        if val <= quantiles[0]:
            return "Q1 (0-25%)"
        elif val <= quantiles[1]:
            return "Q2 (25-50%)"
        elif val <= quantiles[2]:
            return "Q3 (50-75%)"
        else:
            return "Q4 (75-100%)"

    df["cluster"] = df[target_var].apply(assign_cluster)

    # Colores bonitos para los 4 clusters
    palette = {
        "Q1 (0-25%)": "blue",
        "Q2 (25-50%)": "green",
        "Q3 (50-75%)": "orange",
        "Q4 (75-100%)": "red"
    }

    # Plot
    plt.figure(figsize=(10, 6))
    for cl, group in df.groupby("cluster"):
        plt.scatter(group["Peso"], group["elastic_energy"],
                    label=cl,
                    color=palette[cl],
                    alpha=0.7,
                    edgecolor="k")

    plt.xlabel("Peso")
    plt.ylabel("Energia Elastica")
    plt.title(f"Distribución del frente de Pareto según rangos de {target_var}")
    plt.legend(title="Cuartil")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def pair_plot():
    df = pd.read_csv(r"C:\Users\aalvarezsanz\OneDrive - DanobatGroup\Documentos\idk_framework\DOE_datos\Carga carro\merged.csv")
    df = df.sample(n=1000, random_state=42)

    # variables
    outputs = ["Peso", "elastic_energy"]
    inputs = [c for c in df.columns if c not in outputs]

    all_vars = inputs + outputs
    sns.set_style("white")

    sns.set(font_scale=0.6)

    # pairplot
    g = sns.pairplot(
        df[all_vars],
        corner=True,
        plot_kws={"alpha":0.6},
        height=2.2
    )

    # quitar ticks de todos los ejes
    for i in range(len(all_vars)):
        for j in range(len(all_vars)):
            ax = g.axes[i,j]
            if ax:
                ax.tick_params(axis='both', which='both', length=0, labelbottom=False, labelleft=False)

    # título opcional
    g.fig.suptitle("Pairplot de todas las variables sin graduaciones", y=1.02, fontsize=14)

    plt.tight_layout()
    plt.show()

pair_plot()