import matplotlib.pyplot as plt
import numpy as np
from pymoo.core.result import Result
from mpl_toolkits.mplot3d import Axes3D

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
    if F_pareto.shape[1] == 2:
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

    elif F_pareto.shape[1] == 3:
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
        print(f"No se soporta la visualización para {F_pareto.shape[1]} objetivos.")

    return 0


def print_optimization_summary(results: Result):
    """
    Imprime un resumen de la optimización:
    - Generaciones
    - Número total de individuos evaluados
    - Soluciones de Pareto con variables de decisión X y objetivos F
    """
    print("\n🔎 RESUMEN DE LA OPTIMIZACIÓN")
    print("-" * 50)
    
    n_generations = len(results.history)
    print(f"🧬 Generaciones totales: {n_generations}")

    pop_per_gen = [len(algo.pop) for algo in results.history]
    total_individuals = sum(pop_per_gen)
    print(f"👥 Individuos evaluados (en total): {total_individuals}")

    pareto_front = results.F
    print(f"🏁 Soluciones en el frente de Pareto: {len(pareto_front)}")

    print("\n📌 Soluciones de Pareto:")
    for i, (x, f) in enumerate(zip(results.X, results.F)):
        x_dict = x if isinstance(x, dict) else {f"x{i}": val for i, val in enumerate(x)}
        print(f"\n--- Solución {i+1} ---")
        print("Variables de decisión (X):")
        for k, v in x_dict.items():
            print(f"  {k}: {v}")
        print("Objetivos (F):")
        for j, val in enumerate(f):
            print(f"  f{j+1}: {val}")

    return 0