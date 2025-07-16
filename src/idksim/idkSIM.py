import os
import yaml
import plotly.io as pio
from multiprocessing import Process
pio.renderers.default = 'browser'
from idksim.model import idksimObject
from idksim.postprocessing import optimization_summary
from idksim.parameters import Parameter
from idksim.outputs import Output
from idksim.profiling import monitor_memory

# =============================================================================
# Función principal runIdkSIM: Define la secuencia de la simulación/optimización
# =============================================================================
def runIdkSIM(pathMain: str):
    """
    Función principal de idkSIM.

    Esta función orquesta la ejecución de simulaciones, optimizaciones y experimentos DOE
    (Design of Experiments) usando modelos ROM y algoritmos de optimización como NSGA2, NSGA3,
    minimize y least squares. Lee la configuración desde un archivo YAML, inicializa los objetos
    necesarios y ejecuta el flujo correspondiente según el tipo de análisis especificado.

    Args:
        pathMain (str): Ruta al archivo YAML principal de configuración.

    Flujo general:
        1. Lee el archivo YAML de configuración.
        2. Inicializa el modelo (idksimObject) y determina el tipo de análisis.
        3. Si es optimización:
            - Construye listas de parámetros y objetivos.
            - Ejecuta el algoritmo de optimización seleccionado (NSGA2, NSGA3, minimize, least squares).
            - Guarda los resultados y realiza post-procesamiento.
        4. Si es DOE (Design of Experiments):
            - Inicializa el objeto DOE y ejecuta el flujo interactivo para muestreo y evaluación.
        5. Si es entrenamiento de ROM:
            - Llama al pipeline de entrenamiento de idkROM.
        6. Lanza errores si el tipo de análisis no está soportado.

    Raises:
        ValueError: Si el tipo de análisis especificado en el YAML no está soportado.
    """
    # 1) Leer el YAML
    with open(pathMain, 'r') as f:
        data = yaml.safe_load(f)

    # 3) Inicializar la clase model
    objModel = idksimObject(data)
    problem = None

    output_path = data['analysis']['params']['tracking']['path']

    # Verificar el tipo de análisis y algoritmo especificado
    if data['analysis']['type'] == 'optimization':
        #################### MOVER ESTO A IDKDOE E IDKOPT EN ESPECIAL??###############
        # 2) Construir listas de Parameter y Output
        # Crear lista de parámetros variables (optimizables)
        parameters = []
        for key in data['analysis']['params']['variables']:
            parameters.append(Parameter(data[key]))

        # Crear lista de parámetros constantes (no optimizables)
        constant_parameters = []
        for key in data['analysis']['params'].get('constants', []):
            constant_parameters.append(Parameter(data[key]))

        # Crear diccionario con nombre y valor por defecto de las constantes
        constants_dict = {p.name: p.default for p in constant_parameters}

        outputs = []
        for f_key in data['analysis']['params']['fObj']:
            outputs.append(Output(data[f_key]))

        if data['analysis']['params']['algorithm'] == 'NSGA2':

            from idkopt.algorithms.mixed_var_genetic import MixedVariableGeneticProblem
            
            problem = MixedVariableGeneticProblem(data, objModel, parameters, outputs, kwargs=constants_dict)

            res = problem.solve(resume=False if data['analysis']['state']=='new' else True,
                                checkpoint_path=os.path.join(output_path, "genetic_alg_checkpoint.pkl"))

            import dill
            with open(os.path.join(output_path, "resX.pkl"), "wb") as f:
                dill.dump(res.X, f)

        elif data['analysis']['params']['algorithm'] == 'NSGA3':
            
            from pymoo.algorithms.moo.nsga3 import NSGA3
            from pymoo.util.ref_dirs import get_reference_directions
            from idkopt.algorithms.mixed_var_genetic import MixedVariableGeneticProblem
            from pymoo.core.mixed import MixedVariableMating, MixedVariableSampling, MixedVariableDuplicateElimination
            from pymoo.operators.crossover.sbx import SBX
            from pymoo.operators.mutation.pm import PM
            from pymoo.optimize import minimize

            # Inicializar el problema de optimización definido en la clase opt_genalg
            problem = MixedVariableGeneticProblem(data, objModel, parameters, outputs, kwargs=constants_dict)

            # Número de objetivos
            n_dim = len(outputs)

            # Direcciones de referencia para NSGA3
            ref_dirs = get_reference_directions("das-dennis", n_dim, n_partitions=12)

            # Configuración del algoritmo
            pop_size = data['analysis']['params']['popSize']
            n_gen_total = data['analysis']['params']['nGen']

            if data['analysis']['params'].get('settings', 'default') == 'custom':
                crossover = SBX(prob=data['analysis']['params']['operators']['crossover']['prob'],
                                eta=data['analysis']['params']['operators']['crossover']['eta'])
                mutation = PM(prob=data['analysis']['params']['operators']['mutation']['prob'],
                              eta=data['analysis']['params']['operators']['mutation']['eta'])
                
                slct = data['analysis']['params']['operators']['selection']
                if slct['name'] == 'random':
                    from pymoo.operators.selection.rnd import RandomSelection
                    selection = RandomSelection()
                else:
                    from pymoo.operators.selection.tournament import TournamentSelection
                    from pymoo.algorithms.moo.nsga3 import ReferenceDirectionSurvival
                    selection = TournamentSelection(func_comp=ReferenceDirectionSurvival(ref_dirs),
                                                    pressure=slct.get('n_parents', 2))
            else:
                crossover = None
                mutation = None
                selection = None

            algorithm = NSGA3(
                ref_dirs=ref_dirs,
                pop_size=pop_size,
                sampling=MixedVariableSampling(),
                mating=MixedVariableMating(eliminate_duplicates=MixedVariableDuplicateElimination()),
                eliminate_duplicates=MixedVariableDuplicateElimination(),
                crossover=crossover,
                mutation=mutation,
                selection=selection
            )

            res = minimize(problem,
                   algorithm,
                   ('n_gen', n_gen_total),
                   seed=data['analysis']['params'].get('seed', 1),
                   verbose=False,
                   save_history=True)
            
            import dill
            with open(os.path.join(output_path, "resX.pkl"), "wb") as f:
                dill.dump(res.X, f)   

        elif data['analysis']['params']['algorithm'] == 'minimize':

            from idkopt.algorithms.minimize import Minimization

            problem = Minimization(data, objModel, Parameter, Output, kwargs=constants_dict)
            res = problem.solve()
            
        elif data['analysis']['params']['algorithm'] == 'least squares':

            from idkopt.algorithms.least_squares import LeastSquares

            problem = LeastSquares(data, objModel, Parameter, Output, kwargs=constants_dict)
            res = problem.solve()

        try:
            optimization_summary(data, res, parameters, outputs, problem)
        except Exception as e:
            import traceback
            print(f"Error: {e}")
            traceback.print_exc()

    elif data['analysis']['type'] == 'doe':
        """
        Ejecuta un experimento de diseño de experimentos (DOE) según la configuración YAML.

        Permite al usuario elegir entre ejecutar el DOE completo, solo muestrear o ejecutar
        a partir de un CSV ya generado. Soporta ejecución paralela y configuración de muestras.

        Flujo:
            - Inicializa el objeto DOE.
            - Solicita al usuario la opción deseada.
            - Ejecuta el método correspondiente del objeto DOE.
        """
        #from idkdoe.model import idkDOE
        from idkdoe import idkDOE
        problem = idkDOE(data, objModel)
        method = data['analysis']['params']['method'].upper()
        n_samples=data['analysis']['params'].get('n_samples', 10)
        parallel = data['analysis']['params'].get('parallel', False)
        n_workers = data['analysis']['params'].get('n_workers', 1)
        ejecutar_doe = data['analysis'].get('tipo de ejecucion', 0)


        if ejecutar_doe == 0:
            input_csv = data['analysis']['input_csv']

            problem.run_doe(method=method,
                            n_samples=n_samples,
                            parallel=parallel,
                            n_workers=n_workers)

        elif ejecutar_doe == 1:
            input_csv = data['analysis']['input_csv']

            problem.run_doe_from_csv(
                input_csv=input_csv,
                parallel=parallel,
                n_workers=n_workers
                )

        elif ejecutar_doe == 2:
            problem.generate_samples(method=method, n_samples=n_samples)
            print("Solo se generaron las muestras. No se ejecutaron simulaciones.")

    elif data['analysis']['type'] == 'rom training':
        """
        Ejecuta el pipeline de entrenamiento de un modelo ROM según la configuración YAML.

        Inicializa el objeto idkROM y ejecuta el método de entrenamiento, mostrando la ruta
        del modelo entrenado al finalizar.
        """
        from idkrom.model import idkROM
        print(f"Este es el diccionario que se le va a pasar a idkROM: {data}.")
        rom = idkROM(data_dict=data)
        model_path = rom.rom_training_pipeline(data)
        print(f"Este es el path del modelo: {model_path}.")
    
    else:
        raise ValueError(f"Tipo de análisis '{data['analysis']['type']}' no soportado.")