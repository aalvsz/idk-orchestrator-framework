import os
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.result import Result

# Asumimos que 'parameters' es una lista de instancias de Parameter
def write_results_file(data, res, parameters: list, outputs: list, filename=None):
    """
    Guarda resultados de optimización en CSV o JSON:
    - Si `res` es un Result de pymoo, exporta todas las soluciones del frente de Pareto.
    - Si `res` es un objeto con atributos `x_orig`, `fun`, `eval_history`, exporta la mejor solución y el historial.
    """
    output_dir = data['analysis']['params']['tracking']['path']
    os.makedirs(output_dir, exist_ok=True)

    # Determinar tipo de resultado
    if isinstance(res, Result):
        # PYMOO NSGA2/3
        savefile = filename or os.path.join(
            output_dir,
            os.path.basename(data['model']['pathModel']).replace('.pkl', 'results.csv')
        )
        if os.path.isfile(savefile): os.remove(savefile)
        with open(savefile, 'w') as f:
            for i, x in enumerate(res.X):
                f.write(f"--- Solución {i + 1} ---\n")
                # Decisiones
                if isinstance(x, dict):
                    for name, val in x.items(): f.write(f"{name}: {val}\n")
                else:
                    for idx, param in enumerate(parameters): f.write(f"{param.name}: {x[idx]}\n")
                # Objetivos
                f.write("Objetivos:\n")
                for j, raw in enumerate(res.F[i]):
                    val = outputs[j].transform(raw)
                    f.write(f"{outputs[j].name}: {val}\n")
                f.write("\n")
    else:
        # SCALAR minimize
        savefile = filename or os.path.join(output_dir, 'minimize_results.json')
        out = {
            'x_opt': res.x_orig.tolist(),
            'f_opt': float(res.fun)
        }
        if hasattr(res, 'eval_history'):
            out['eval_history'] = res.eval_history
        with open(savefile, 'w') as f:
            import json
            json.dump(out, f, indent=2)
        print(f"Resultados guardados en: {savefile}")

    return 0


def print_optimization_summary(res, parameters: list, outputs: list):
    from pymoo.core.result import Result
    print("\n🔎 RESUMEN DE LA OPTIMIZACIÓN (GA Multiobjetivo)")
    print("-" * 50)

    if isinstance(res, Result):
        n_gen = len(res.history)
        print(f"🧬 Generaciones totales: {n_gen}")
        total_inds = sum(len(algo.pop) for algo in res.history)
        print(f"👥 Individuos evaluados (en total): {total_inds}")

        X = res.X

        # --- Corrección: si X es dict de dicts (mal interpretado como varias soluciones)
        if isinstance(X, dict) and all(isinstance(v, dict) for v in X.values()):
            # Tomar la primera solución válida
            first_key = next(iter(X))
            x = X[first_key]
            X_list = [x]
        elif isinstance(X, dict):
            X_list = [X]
        else:
            X = np.atleast_2d(X)
            X_list = X

        print(f"🏁 Soluciones en el frente de Pareto: {len(X_list)}")

        for i, x in enumerate(X_list):
            print(f"\n--- Solución {i + 1} ---")
            if isinstance(x, dict):
                for k, v in x.items():
                    print(f"  {k}: {v}")
            else:
                for idx, param in enumerate(parameters):
                    try:
                        print(f"  {param.name}: {x[idx]}")
                    except IndexError:
                        print(f"  ⚠️ Error: x tiene longitud {len(x)}, se esperaba al menos {idx+1}")
                        break

            f_vals = res.F[i] if res.F.ndim > 1 else res.F
            print("Objetivos:")
            for j, raw in enumerate(np.atleast_1d(f_vals)):
                val = outputs[j].transform(raw)
                print(f"  {outputs[j].name}: {val}")
    else:
        print("⚠️ Tipo de resultado no reconocido.")

    return 0




def plot_pareto_and_dominated(res, save_path: str = None, show=True):
    """
    Dibuja Pareto vs dominadas:
    - Para Result (pymoo): usa history.
    - Para scalar minimize: traza eval_history puntos f vs iter.
    """
    
    if isinstance(res, Result):
        # Extraer F pareto y F all
        F_p = res.F
        F_all = np.vstack([algo.pop.get('F') for algo in res.history])
        # Dominancia
        def dominated(f): return any(np.all(fp <= f) and np.any(fp < f) for fp in F_p)
        mask_dom = np.array([dominated(f) for f in F_all])
        F_dom = F_all[mask_dom]
        # Plot 2D solamente
        plt.figure(figsize=(8,6))
        if F_dom.size: plt.scatter(F_dom[:,0],F_dom[:,1],label='Dominadas',marker='x')
        plt.scatter(F_p[:,0],F_p[:,1],label='Pareto',marker='o')
        plt.xlabel('Objetivo 1'); plt.ylabel('Objetivo 2')
        plt.title('Pareto y dominadas')
        plt.legend(); plt.grid(True); plt.tight_layout()
        if save_path: plt.savefig(save_path, dpi=300)
        if show: plt.show()
    else:
        # Scalar minimize: plotea eval_history f vs iter
        fvals = [e['f'][0] if isinstance(e['f'], list) else e['f'] for e in res.eval_history]

        #fvals = [e['f'][0] if isinstance(e['f'], list) else e['f'] for e in res.eval_history]
        plt.figure(figsize=(8,6))
        plt.plot(range(len(fvals)), fvals, marker='o')
        plt.xlabel('Iteración'); plt.ylabel('Función objetivo')
        plt.title('Evolución de la función objetivo')
        plt.grid(True); plt.tight_layout()
        if save_path: plt.savefig(save_path, dpi=300)
        if show: plt.show()

    return 0
