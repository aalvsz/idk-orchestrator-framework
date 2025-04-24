import yaml
import sys, os
import plotly.io as pio
pio.renderers.default = 'browser'
from tqdm import tqdm
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.mixed import MixedVariableMating, MixedVariableSampling, MixedVariableDuplicateElimination
from pymoo.optimize import minimize

sys.path.insert(0, os.path.abspath(r"D:/idk_framework"))

from idkopt.algorithms.genetic_algorithm import GeneticAlgorithm
from idkopt.algorithms.minimize import Minimization
from idkopt.algorithms.least_squares import LeastSquares

from src.idkrom_model import idksimObject
from src.postprocessing import plot_pareto_and_dominated, print_optimization_summary, write_results_file
from src.parameters import Parameter
from src.outputs import Output

# =============================================================================
# Función principal runIdkSIM: Define la secuencia de la simulación/optimización
# =============================================================================
def runIdkSIM(pathMain: str):
    """
    Función principal de idkSIM.
    Recibe como entrada el path del archivo YAML principal y ejecuta la
    optimización usando un ROM y el algoritmo NSGA2.
    """
    # 1) Leer el YAML
    with open(pathMain, 'r') as f:
        data = yaml.safe_load(f)

    # 2) Construir listas de Parameter y Output
    parameters = []
    for key in data['analysis']['params']['variables']:
        parameters.append(Parameter(data[key]))

    outputs = []
    for f_key in data['analysis']['params']['fObj']:
        outputs.append(Output(data[f_key]))
    
    # Inicializar la clase model y asignar rutas
    objModel = idksimObject()
    objModel.pathAplication = data['model']['pathAplication']
    objModel.pathModel = data['model']['pathModel']
    
    problem = None

    # Verificar el tipo de análisis y algoritmo especificado
    if data['analysis']['type'] == 'optimization':

        if data['analysis']['params']['algorithm'] == 'NSGA2':

            # Inicializar el algoritmo NSGA2 para el problema
            algorithm = NSGA2(
            pop_size=data['analysis']['params']['popSize'],
            sampling=MixedVariableSampling(),   # Se define un muestreador para variables mixtas
            mating=MixedVariableMating(eliminate_duplicates=MixedVariableDuplicateElimination()),
            eliminate_duplicates=MixedVariableDuplicateElimination()
            )
            
            # Inicializar el problema de optimización definido en la clase opt_genalg
            problem = GeneticAlgorithm(data, objModel, algorithm, parameters, outputs)
            
            # Obtener el número total de generaciones del YAML
            n_gen_total = data['analysis']['params']['nGen']
            print(f"Iniciando optimización NSGA2 con {n_gen_total} generaciones...") # Mensaje inicial

            # Usar tqdm en modo manual, con el total de generaciones
            # La barra se inicializará a 0 y llegará al 100% cuando se actualice 'n_gen_total' veces.
            with tqdm(total=n_gen_total, desc="Optimizando (Generaciones)") as pbar:

                def pymoo_callback(algorithm):
                    pbar.update(1) # Incrementa la barra en 1

                # Ejecutar la optimización utilizando la función minimize de pymoo
                res = minimize(problem,
                                algorithm,
                                ('n_gen', n_gen_total), # Usamos la variable n_gen_total aquí
                                seed=2,
                                verbose=False, # Desactivamos el verbose de pymoo
                                save_history=True,
                                callback=pymoo_callback) # <-- Pasamos nuestra función de callback
            

        elif data['analysis']['params']['algorithm'] == 'minimize':

            problem = Minimization(data, objModel, Parameter, Output)
            res = problem.solve()


        elif data['analysis']['params']['algorithm'] == 'least squares':

            problem = LeastSquares(data, objModel, Parameter, Output)
            res = problem.solve()


    print_optimization_summary(res, parameters, outputs)
    plot_pareto_and_dominated(res)
    write_results_file(data, res, parameters, outputs)
