import os
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.result import Result

def optimization_summary(data, res, parameters, outputs, problem):
    print_optimization_summary(data, res, parameters, outputs)
    write_results_file(data, res, parameters, outputs, 'results.txt')
    if data['analysis']['params']['algorithm'] == 'NSGA2' or data['analysis']['params']['algorithm'] == 'NSGA3':
        plot_pareto_and_dominated(data, res, outputs, nominal_point=(9821.927253772777, 1.320873466836539), plotly=True)


def write_results_file(data, res, parameters: list, outputs: list, filename=None):
    """
    Guarda resultados de optimización:
    - Si `res` es un Result de pymoo:
        - Si es monoobjetivo: guarda solo la mejor solución en un .txt
        - Si es multiobjetivo: guarda el frente de Pareto completo en un .csv
    - Si es scalar minimize: guarda la mejor solución en un .txt
    """

    if isinstance(res, Result) and len(outputs) == 0:
        raise ValueError("⚠️ La lista 'outputs' está vacía. No se pueden escribir los objetivos.")

    output_dir = data['analysis']['params']['tracking']['path']
    os.makedirs(output_dir, exist_ok=True)

    savefile = os.path.join(output_dir, filename)

    if isinstance(res, Result):
        F = res.F
        X = res.X

        # Caso NSGA2 con 1 objetivo
        if F.ndim == 1 or (F.ndim == 2 and F.shape[1] == 1):
            F = F.flatten()

            # Caso especial: X es un único dict (una sola solución)
            if isinstance(X, dict) and all(k in X for k in [p.name for p in parameters]):
                x_opt = X
                f_opt = float(F[0])  # solo hay un valor de función objetivo
            else:
                best_idx = int(np.argmin(F))
                x_opt = X[best_idx]
                f_opt = float(F[best_idx])


            with open(savefile, 'w') as f:
                f.write("=== MEJOR SOLUCIÓN ENCONTRADA ===\n\n")
                f.write("Parámetros:\n")
                if isinstance(x_opt, dict):
                    for k, v in x_opt.items():
                        f.write(f"  {k}: {v}\n")
                else:
                    for i, param in enumerate(parameters):
                        f.write(f"  {param.name}: {float(x_opt[i])}\n")
                f.write("\nObjetivo:\n")
                if len(outputs) > 0:
                    val = outputs[0].transform(f_opt)
                    f.write(f"  {outputs[0].name}: {val}\n")
                else:
                    f.write(f"  f: {f_opt}\n")

                # Historial si existe
                if hasattr(res, 'history'):
                    f.write("\nHistorial de evaluaciones (fitness):\n")
                    for gen, algo in enumerate(res.history):
                        Fs = algo.pop.get("F")
                        for fval in Fs:
                            val = fval[0] if isinstance(fval, (np.ndarray, list, tuple)) else fval
                            f.write(f"  Gen {gen}: {float(val)}\n")

            print(f"Resultados guardados en: {savefile}")

        else:
            # MULTIOBJETIVO - guardar frente de Pareto en CSV
            savefile_csv = savefile.replace('.txt', '.csv')
            if os.path.isfile(savefile_csv): os.remove(savefile_csv)
            F = np.atleast_2d(F)

            with open(savefile_csv, 'w') as f:
                for i, x in enumerate(X):
                    f.write(f"--- Solución {i + 1} ---\n")
                    if isinstance(x, dict):
                        for name, val in x.items():
                            f.write(f"{name}: {val}\n")
                    else:
                        for idx, param in enumerate(parameters):
                            f.write(f"{param.name}: {float(x[idx])}\n")
                    f.write("Objetivos:\n")
                    for j, raw in enumerate(F[i]):
                        if j < len(outputs):
                            try:
                                val = outputs[j].transform(raw)
                                f.write(f"{outputs[j].name}: {val}\n")
                            except Exception as e:
                                f.write(f"{outputs[j].name}: ERROR ({e})\n")
                        else:
                            f.write(f"Objetivo {j}: {raw}\n")
                    f.write("\n")
            print(f"Frente de Pareto guardado en: {savefile_csv}")

    else:
        # Scalar minimize (scipy)
        savefile = savefile.replace('.txt', '_minimize.txt')
        with open(savefile, 'w') as f:
            f.write("=== MEJOR SOLUCIÓN ENCONTRADA ===\n\n")
            f.write("Parámetros:\n")
            for i, param in enumerate(parameters):
                f.write(f"  {param.name}: {float(res.x_orig[i])}\n")
            f.write("\nObjetivo:\n")
            print("Raw objective value (res.fun):", float(res.fun))
            print("Transformed value:", outputs[0].transform(float(res.fun)))
            
            if len(outputs) > 0:
                f_opt_raw = float(res.fun)
                f_opt_transf = outputs[0].transform(f_opt_raw)
                f.write(f"  {outputs[0].name} (raw): {f_opt_raw}\n")
                f.write(f"  {outputs[0].name} (transformed): {f_opt_transf}\n")
            else:
                f.write(f"  f: {float(res.fun)}\n")


            if hasattr(res, 'eval_history'):
                f.write("\nHistorial de evaluaciones:\n")
                for i, e in enumerate(res.eval_history):
                    val = e['f_raw'][0] if isinstance(e['f_raw'], list) else e['f_raw']
                    f.write(f"  {i}: {float(val)}\n")

        print(f"Resultados guardados en: {savefile}")

    return 0


def print_optimization_summary(data, res, parameters: list, outputs: list):
    print("\n🔎 RESUMEN DE LA OPTIMIZACIÓN")
    print("-" * 50)


    if isinstance(res, Result):
        n_gen = len(res.history)
        print(f"🧬 Generaciones totales: {n_gen}")
        total_inds = sum(len(algo.pop) for algo in res.history)
        print(f"👥 Individuos evaluados (en total): {total_inds}") 

        """# --- Normalización segura ---
        if isinstance(res.X, dict) and all(isinstance(v, dict) for v in res.X.values()):
            values = list(res.X.values())
            if all(val == values[0] for val in values[1:]):
                X_list = [values[0]]  # Solo una solución única
            else:
                raise ValueError("Estructura incorrecta: múltiples valores distintos bajo X.keys()")
        elif isinstance(res.X, dict):
            X_list = [res.X]
        elif isinstance(res.X, list) and all(isinstance(xi, dict) for xi in res.X):
            X_list = res.X
        else:
            X = np.atleast_2d(res.X)
            X_list = [dict(zip([p.name for p in parameters], xi)) for xi in X]"""


        X_list = list(res.X)

        print(f"🏁 Soluciones en el frente de Pareto: {len(X_list)}")

        for i, x in enumerate(X_list):
            print(f"\n--- Solución {i + 1} ---")
            for k, v in x.items():
                print(f"  {k}: {v:.3f}")


            f_vals = res.F[i] if res.F.ndim > 1 else res.F
            print("Objetivos:")
            for j, raw in enumerate(np.atleast_1d(f_vals)):
                val = outputs[j].transform(raw)
                print(f"{outputs[j].goal} {outputs[j].name}: {float(val):.3f}")
    else:
        print("⚠️ Tipo de resultado no reconocido.")

    return 0



def plot_pareto_and_dominated(data, res, outputs: list, nominal_point=None, plotly=False):
    """
    Dibuja el frente de Pareto y puntos dominados, en 2D con Matplotlib
    o 3D con Plotly si plotly=True.
    """

    from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
    from pymoo.core.result import Result

    import os
    import matplotlib.pyplot as plt
    from matplotlib import cm

    output_dir = data['analysis']['params']['tracking']['path']
    os.makedirs(os.path.join(output_dir, 'figures'), exist_ok=True)

    if not isinstance(res, Result):
        print("⚠️ Resultado no reconocido. No se puede graficar Pareto.")
        return

    # --- extracción segura de resultados ---
    F_p = np.atleast_2d(res.F)
    n_obj = F_p.shape[1] if F_p.ndim > 1 else 1

    if n_obj < 2:
        print("⚠️ Problema monoobjetivo, solo evolución temporal.")
        return

    # recopilar todos los individuos evaluados
    F_list = []
    for algo in res.history:
        F = algo.pop.get("F")
        if F is not None and F.size > 0:
            F_list.append(F)
    if not F_list:
        print("⚠️ No hay datos para graficar.")
        return

    F_all = np.vstack(F_list)
    nds = NonDominatedSorting().do(F_all, only_non_dominated_front=True)
    mask_dom = np.ones(F_all.shape[0], dtype=bool)
    mask_dom[nds] = False

    F_dom = F_all[mask_dom]
    F_pareto = F_all[nds]

    if plotly and n_obj >= 3:
        # === 3D Plotly ===
        import plotly.graph_objects as go

        fig = go.Figure()

        if F_dom.size > 0:
            fig.add_trace(go.Scatter3d(
                x=F_dom[:, 0],
                y=F_dom[:, 1],
                z=F_dom[:, 2],
                mode="markers",
                marker=dict(size=3, color="gray"),
                name="Dominadas"
            ))

        fig.add_trace(go.Scatter3d(
            x=F_pareto[:, 0],
            y=F_pareto[:, 1],
            z=F_pareto[:, 2],
            mode="markers",
            marker=dict(size=4, color="blue"),
            name="Pareto"
        ))

        if nominal_point is not None and len(nominal_point) == 3:
            fig.add_trace(go.Scatter3d(
                x=[nominal_point[0]],
                y=[nominal_point[1]],
                z=[nominal_point[2]],
                mode="markers",
                marker=dict(size=6, color="red", symbol="diamond"),
                name="Nominal"
            ))


        fig.update_layout(
            title="Frente de Pareto 3D",
            scene=dict(
                xaxis_title=outputs[0].name,
                yaxis_title=outputs[1].name,
                zaxis_title=outputs[2].name
            ),
            legend=dict(x=0.01, y=0.99)
        )
        plotly_path = os.path.join(output_dir, "figures", "pareto_plot_3D.html")
        fig.write_html(plotly_path)
        print(f"✅ Gráfico 3D interactivo guardado en {plotly_path}")

    else:
        # === 2D Matplotlib ===
        plt.figure(figsize=(8, 6))
        if F_dom.size > 0:
            plt.scatter(F_dom[:, 0], F_dom[:, 1], label="Dominadas", c="gray", alpha=0.5, marker="x")
        plt.scatter(F_pareto[:, 0], F_pareto[:, 1], label="Pareto", c="blue", marker="o")

        if nominal_point is not None and len(nominal_point) >= 2:
            plt.scatter(nominal_point[0], nominal_point[1], c="red", s=80, marker="*", label="Nominal")

        plt.xlabel(outputs[0].name)
        plt.ylabel(outputs[1].name)
        plt.title("Frente de Pareto y puntos dominados")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "figures", "pareto_plot.png"), dpi=300)
        plt.close()
        print(f"✅ Gráfico 2D guardado en {os.path.join(output_dir, 'figures', 'pareto_plot.png')}")

