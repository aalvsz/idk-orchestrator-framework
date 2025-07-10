import os
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.result import Result

def optimization_summary(data, res, parameters, outputs, problem):
    """
    Realiza el post-procesamiento principal de los resultados de optimización.

    Imprime un resumen, guarda los resultados en archivos y genera gráficos de Pareto si corresponde.

    Args:
        data (dict): Diccionario de configuración y datos de la simulación.
        res: Resultado de la optimización (puede ser un objeto Result de pymoo o resultado de scipy).
        parameters (list): Lista de parámetros de entrada optimizados.
        outputs (list): Lista de objetivos o salidas optimizadas.
        problem: Objeto problema de optimización (no siempre usado).
    """
    print("\n\n\n\n ################# POST-PROCESSING #################\n\n\n\n")
    print_optimization_summary(data, res, parameters, outputs)
    write_results_file(data, res, parameters, outputs, 'results.txt')
    if data['analysis']['params']['algorithm'] == 'NSGA2' or data['analysis']['params']['algorithm'] == 'NSGA3':
        plot_pareto_and_dominated(data, res, outputs, plotly=True)


def write_results_file(data, res, parameters: list, outputs: list, filename=None):
    """
    Guarda los resultados de la optimización en archivos de texto o CSV.

    - Si `res` es un objeto Result de pymoo:
        - Monoobjetivo: guarda la mejor solución en un .txt.
        - Multiobjetivo: guarda el frente de Pareto completo en un .csv.
    - Si es resultado de scipy minimize: guarda la mejor solución en un .txt.

    Args:
        data (dict): Diccionario de configuración y datos de la simulación.
        res: Resultado de la optimización (Result de pymoo o resultado de scipy).
        parameters (list): Lista de parámetros de entrada optimizados.
        outputs (list): Lista de objetivos o salidas optimizadas.
        filename (str, opcional): Nombre base del archivo de salida.

    Returns:
        int: 0 si se guarda correctamente.
    """
    if isinstance(res, Result) and len(outputs) == 0:
        raise ValueError("⚠️ La lista 'outputs' está vacía. No se pueden escribir los objetivos.")

    output_dir = data['analysis']['params']['tracking']['path']
    os.makedirs(output_dir, exist_ok=True)

    savefile = os.path.join(output_dir, filename)

    # para NSGA
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

        # MULTIOBJETIVO - guardar frente de Pareto en CSV
        else:
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

    # ------------------------------
    # Caso Least Squares (scipy)
    # ------------------------------
    else:
        savefile = savefile.replace('.txt', '_minimize.txt')
        with open(savefile, 'w') as f:
            f.write("=== MEJOR SOLUCIÓN ENCONTRADA ===\n\n")
            f.write("Parámetros:\n")
            for i, param in enumerate(parameters):
                f.write(f"  {param.name}: {float(res.x_orig[i])}\n")

            # Manejo robusto para mono o multi objetivo
            f.write("\nObjetivo:\n")
            f_vals = np.atleast_1d(res.fun)

            for j, f_raw in enumerate(f_vals):
                if j < len(outputs):
                    f_trans = outputs[j].transform(f_raw)
                    f.write(f"  {outputs[j].name} (raw): {f_raw}\n")
                    f.write(f"  {outputs[j].name} (transformed): {f_trans}\n")
                else:
                    f.write(f"  f{j}: {f_raw}\n")

            # Historial de evaluaciones si existe
            if hasattr(res, 'eval_history'):
                f.write("\nHistorial de evaluaciones:\n")
                for i, e in enumerate(res.eval_history):
                    raw_vals = np.atleast_1d(e['f_raw'])
                    f.write(f"  {i}: " + ", ".join([f"{float(v)}" for v in raw_vals]) + "\n")

        print(f"Resultados guardados en: {savefile}")
    return 0


def print_optimization_summary(data, res, parameters: list, outputs: list):
    """
    Imprime un resumen de los resultados de la optimización en consola.

    Muestra información relevante como número de generaciones, individuos evaluados,
    soluciones en el frente de Pareto y valores de los objetivos.

    Args:
        data (dict): Diccionario de configuración y datos de la simulación.
        res: Resultado de la optimización (Result de pymoo o resultado de scipy).
        parameters (list): Lista de parámetros de entrada optimizados.
        outputs (list): Lista de objetivos o salidas optimizadas.

    Returns:
        int: 0 si se imprime correctamente.
    """
    print("\n🔎 RESUMEN DE LA OPTIMIZACIÓN")
    print("-" * 50)

    from pymoo.core.result import Result
    import numpy as np

    # === Caso PYMOO (NSGA2/NSGA3)
    if isinstance(res, Result):
        n_gen = len(res.history)
        print(f"🧬 Generaciones totales: {n_gen}")
        total_inds = sum(len(algo.pop) for algo in res.history)
        print(f"👥 Individuos evaluados (en total): {total_inds}") 

        X_list = list(res.X)
        print(f"🏁 Soluciones en el frente de Pareto: {len(X_list)}")

        for i, x in enumerate(X_list):
            print(f"\n--- Solución {i + 1} ---")
            for k, v in x.items():
                print(f"  {k}: {v:.6f}")

            f_vals = res.F[i] if res.F.ndim > 1 else res.F
            f_vals = np.atleast_1d(f_vals)
            print("🎯 Objetivos:")
            for j, raw in enumerate(f_vals):
                val = outputs[j].transform(raw)
                print(f"  {outputs[j].goal} {outputs[j].name}: {float(val):.6f}")

    # === Caso Least Squares o Scalar Minimize (SciPy)
    else:
        print("📌 Tipo: SciPy minimize / least_squares")

        print("\n--- Mejor solución ---")
        for i, param in enumerate(parameters):
            print(f"  {param.name}: {float(res.x_orig[i]):.6f}")

        print("\n🎯 Objetivos:")
        f_vals = np.atleast_1d(res.fun)
        for j, f_raw in enumerate(f_vals):
            if j < len(outputs):
                f_trans = outputs[j].transform(f_raw)
                print(f"  {outputs[j].goal} {outputs[j].name}: {f_trans:.6f}")
            else:
                print(f"  f{j}: {f_raw:.6f}")

    return 0


def plot_pareto_and_dominated(data, res, outputs: list, nominal_point=None, plotly=False):
    """
    Dibuja el frente de Pareto y los puntos dominados, en 2D con Matplotlib
    o en 3D con Plotly si plotly=True.

    Args:
        data (dict): Diccionario de configuración y datos de la simulación.
        res: Resultado de la optimización (Result de pymoo).
        outputs (list): Lista de objetivos o salidas optimizadas.
        nominal_point (list, opcional): Punto nominal a destacar en el gráfico.
        plotly (bool): Si True, genera un gráfico 3D interactivo con Plotly.

    El gráfico se guarda en la carpeta de resultados correspondiente.
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

