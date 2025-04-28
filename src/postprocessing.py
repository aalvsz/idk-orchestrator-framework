import os
import numpy as np
import matplotlib.pyplot as plt

from pymoo.core.result import Result

# Asumimos que 'parameters' es una lista de instancias de Parameter
def write_results_file(data, res: Result, parameters: list, outputs: list):
    """
    Guarda en un archivo CSV los resultados de la optimización, usando las clases Parameter y Output
    para obtener nombres y transformaciones de los objetivos.
    """
    # Obtener el directorio de salida desde la configuración
    output_dir = data['analysis']['params']['tracking']['path']

    # Crear el directorio si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Construir el nombre del archivo de resultados
    savefile = os.path.join(
        output_dir,
        os.path.basename(data['model']['pathModel']).replace('.pkl', '_NSGA2_Results.csv')
    )
    # Si existe, eliminar para escribir de nuevo
    if os.path.isfile(savefile):
        os.remove(savefile)

    with open(savefile, 'w') as f:
        # Iterar soluciones
        for i, x in enumerate(res.X):
            f.write(f"--- Solución {i + 1} ---\n")

            # Variables de decisión
            if isinstance(x, dict):
                # Caso dict con nombres
                for name, val in x.items():
                    f.write(f"{name}: {val}\n")
            else:
                # Asumimos array/list, usar parameters para nombres
                for idx, param in enumerate(parameters):
                    f.write(f"{param.name}: {x[idx]}\n")

            f.write("Objetivos:\n")
            # Objetivos y transformación
            for j, raw_val in enumerate(res.F[i]):
                out = outputs[j]
                val = out.transform(raw_val)
                f.write(f"{out.name}: {val}\n")

            f.write("\n")

    return 0


# Asumimos que 'parameters' y 'outputs' son listas de Parameter y Output respectivamente

def print_optimization_summary(results: Result, parameters: list, outputs: list):
    """
    Imprime un resumen de la optimización, listando generaciones, número de individuos y soluciones de Pareto,
    con nombres y transformaciones de parámetros y objetivos.
    """
    print("\n🔎 RESUMEN DE LA OPTIMIZACIÓN")
    print("-" * 50)

    # Generaciones
    n_gen = len(results.history)
    print(f"🧬 Generaciones totales: {n_gen}")

    # Total individuos evaluados
    total_inds = sum(len(algo.pop) for algo in results.history)
    print(f"👥 Individuos evaluados (en total): {total_inds}")

    # Frontera de Pareto
    F_pareto = results.F
    X_pareto = results.X

    # Asegurar forma consistente
    if isinstance(X_pareto, np.ndarray) and X_pareto.dtype == object:
        X_pareto = X_pareto.tolist()

    if np.ndim(F_pareto) == 1:
        F_pareto = F_pareto.reshape(1, -1)
        X_pareto = [X_pareto]

    n_pareto = len(F_pareto)
    print(f"🏁 Soluciones en el frente de Pareto: {n_pareto}")

    # Mostrar soluciones
    for i in range(n_pareto):
        print(f"\n--- Solución {i + 1} ---")
        # Decisiones
        print("Variables de decisión (X):")
        x = X_pareto[i]
        if isinstance(x, dict):
            for name, val in x.items():
                print(f"  {name}: {val}")
        else:
            for idx, param in enumerate(parameters):
                print(f"  {param.name}: {x[idx]}")

        # Objetivos
        print("Objetivos (F):")
        for j, raw_val in enumerate(F_pareto[i]):
            out = outputs[j]
            val = out.transform(raw_val)
            print(f"  {out.name}: {val}")

    return 0


def is_dominated_by_pareto(f, pareto_set):
    """
    Verifica si el punto f está dominado por algún punto en el pareto_set.
    Dominancia estricta: f' domina a f si f' <= f y f' != f
    """
    return any(np.all(f_ <= f) and np.any(f_ < f) for f_ in pareto_set)

def plot_pareto_and_dominated(results: Result, save_path: str = "pareto_dominance.png"):
    """
    Dibuja en el mismo gráfico:
    - El frente de Pareto (res.F)
    - Todas las soluciones dominadas evaluadas durante la optimización
    """
    F_pareto = results.F
    F_all = []

    # Recolectar todos los F evaluados generación a generación
    for algo in results.history:
        F_gen = algo.pop.get("F")
        F_all.append(F_gen)

    F_all = np.vstack(F_all)

    # Filtrar dominadas (todo lo que no está en el Pareto)
    is_dominated = np.array([is_dominated_by_pareto(f, F_pareto) for f in F_all])
    F_dominated = F_all[is_dominated]

    # Visualizar
    # Si es 1D, asume que hay un único objetivo.
    if F_pareto.ndim == 1:
        num_obj = 1
    else:
        num_obj = F_pareto.shape[1]

    if num_obj == 1:
        # Visualización para 1 objetivo
        plt.figure(figsize=(8,6))
        plt.scatter(range(len(F_pareto)), F_pareto, c='red', label='Frontera de Pareto')
        plt.xlabel("Individuo")
        plt.ylabel("Objetivo (MSE)")
        plt.title("Frente de Pareto (1 objetivo)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300)
        plt.show()

    if num_obj == 2:
        plt.figure(figsize=(8,6))
        if len(F_dominated) > 0:
            plt.scatter(F_dominated[:, 0], F_dominated[:, 1], c='gray', s=20, label='Dominadas')
        plt.scatter(F_pareto[:, 0], F_pareto[:, 1], c='red', s=40, marker='o', label='Frontera de Pareto')
        plt.xlabel("Objetivo 1")
        plt.ylabel("Objetivo 2")
        plt.title("Frontera de Pareto y soluciones dominadas")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300)
        plt.show()

    elif num_obj == 3:
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111, projection='3d')
        if len(F_dominated) > 0:
            ax.scatter(F_dominated[:, 0], F_dominated[:, 1], F_dominated[:, 2], c='gray', s=20, label='Dominadas')
        ax.scatter(F_pareto[:, 0], F_pareto[:, 1], F_pareto[:, 2], c='red', s=40, label='Frontera de Pareto')
        ax.set_xlabel("Objetivo 1")
        ax.set_ylabel("Objetivo 2")
        ax.set_zlabel("Objetivo 3")
        ax.set_title("Frontera de Pareto y soluciones dominadas")
        ax.legend()
        plt.tight_layout()
        plt.savefig(save_path, dpi=300)
        plt.show()

    else:
        print(f"No se soporta la visualización para {F_pareto.ndim} objetivos.")

    return 0

