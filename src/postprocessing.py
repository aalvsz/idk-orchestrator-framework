import os
import matplotlib.pyplot as plt
import numpy as np
from pymoo.core.result import Result

def write_results_file(data, res):
    import os

    savefileName = os.path.join(
        data['analysis']['params']['tracking']['path'],
        os.path.basename(data['model']['pathModel']).replace('.pkl', '_NSGA2_Results.csv')
    )

    if os.path.isfile(savefileName):
        os.remove(savefileName)

    with open(savefileName, 'w') as file:
        for i, x_dict in enumerate(res.X):
            file.write(f"--- Solución {i+1} ---\n")
            for k, v in x_dict.items():
                file.write(f"{k}: {v}\n")
            file.write("Objetivos:\n")
            for j, fval in enumerate(res.F[i]):
                file.write(f"f{j}: {fval}\n")
            file.write("\n")

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

def print_optimization_summary(problem, results):
    """
    Imprime un resumen de la optimización.
    """
    import numpy as np

    print("\n🔎 RESUMEN DE LA OPTIMIZACIÓN")
    print("-" * 50)

    n_generations = len(results.history)
    print(f"🧬 Generaciones totales: {n_generations}")

    pop_per_gen = [len(algo.pop) for algo in results.history]
    total_individuals = sum(pop_per_gen)
    print(f"👥 Individuos evaluados (en total): {total_individuals}")

    F_pareto = results.F
    X_pareto = results.X

    # Asegurar forma consistente
    if isinstance(X_pareto, np.ndarray) and X_pareto.dtype == "O":
        X_pareto = X_pareto.tolist()

    if np.ndim(F_pareto) == 1:
        F_pareto = F_pareto.reshape(1, -1)
        X_pareto = [X_pareto]  # convertir en lista de un único dict

    print(f"🏁 Soluciones en el frente de Pareto: {len(F_pareto)}")

    print("\n📌 Soluciones de Pareto:")
    for i in range(len(F_pareto)):
        print(f"\n--- Solución {i + 1} ---")

        print("Variables de decisión (X):")
        for name, value in X_pareto[i].items():
            print(f"  {name}: {value}")

        print("Objetivos (F):")
        for j, obj_value in enumerate(F_pareto[i]):
            obj_name = getattr(problem, "obj_names", [f"f{j}" for j in range(len(F_pareto[i]))])[j]
            print(f"  {obj_name}: {obj_value}")

    return 0
