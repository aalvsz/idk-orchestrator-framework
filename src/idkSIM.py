import os
import yaml
import plotly.io as pio
pio.renderers.default = 'browser'

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.mixed import MixedVariableMating, MixedVariableSampling, MixedVariableDuplicateElimination
from pymoo.optimize import minimize
from pymoo.visualization.pcp import PCP
import sys
#sys.path.append('D:/idk-Suite/venvs/Lib/site-packages')
sys.path.append('D:/idk_framework')
sys.path.append('D:/idk_framework/idkROM')
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
    problem = None
    # Leer archivo YAML principal
    with open(pathMain, 'r') as file:
        data = yaml.safe_load(file)
    
    # Inicializar la clase model y asignar rutas
    objModel = idksimObject()
    objModel.pathAplication = data['model']['pathAplication']
    objModel.pathModel = data['model']['pathModel']
    
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
            problem = GeneticAlgorithm(data, objModel, algorithm, Parameter, Output)
            
            # Ejecutar la optimización utilizando la función minimize de pymoo
            res = minimize(problem,
                           algorithm,
                           ('n_gen', data['analysis']['params']['nGen']),
                           seed=1,
                           verbose=True,
                           save_history=True)
            

        elif data['analysis']['params']['algorithm'] == 'minimize':

            
            # Ejemplo de uso (suponiendo que 'data', 'objModel', 'Parameter' y 'Output' están definidos):
             try:
                 problem = Minimization(data, objModel, Parameter, Output)
                 resultado = problem.solve()
             except ValueError as e:
                 print(e)



        elif data['analysis']['params']['algorithm'] == 'least squares':

            try:
                problem = LeastSquares(data, objModel, Parameter, Output)
                resultado = problem.solve()
            except ValueError as e:
                print("Error:", e)

            
    print_optimization_summary(problem, res)
    plot_pareto_and_dominated(res)
    write_results_file(data, res)
