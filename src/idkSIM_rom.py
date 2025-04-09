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
from idkopt.algorithms.genetic_algorithm import genalg
from src.model.idkrom_model import model
from src.post.plot_pareto import plot_pareto_and_dominated,print_optimization_summary


# =============================================================================
# Función principal runIdkSIM: Define la secuencia de la simulación/optimización
# =============================================================================
def runIdkSIM(pathMain: str):
    """
    Función principal de idkSIM.
    Recibe como entrada el path del archivo YAML principal y ejecuta la
    optimización usando un ROM y el algoritmo NSGA2.
    """
    # Leer archivo YAML principal
    with open(pathMain, 'r') as file:
        data = yaml.safe_load(file)
    
    # Inicializar la clase model y asignar rutas
    objModel = model()
    objModel.pathAplication = data['model']['pathAplication']
    objModel.pathModel = data['model']['pathModel']
    # Se cargará el ROM en la primera llamada a idk_run
    
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
            problem = genalg(data, objModel, algorithm)
            
            # Definir el nombre del archivo de resultados
            savefileName = os.path.join(data['analysis']['params']['tracking']['path'],
                                         os.path.basename(data['model']['pathModel']).replace('.pkl', '_NSGA2_Results.csv'))
            
            # Si existe el archivo, lo borramos para evitar sobreescritura
            if os.path.isfile(savefileName):
                os.remove(savefileName)
            
            # Escribir la cabecera de resultados (nombres de variables y objetivos)
            ParamObjList = ''
            # Variables de decisión
            for key in data['analysis']['params']['variables']:
                ParamObjList += data[key]['name'] + ', '
            # Objetivos
            for key in data['analysis']['params']['fObj']:
                ParamObjList += data[key]['name'] + ', '
            with open(savefileName, 'w') as file:
                file.write(ParamObjList + '\n')
            
            # Ejecutar la optimización utilizando la función minimize de pymoo
            res = minimize(problem,
                           algorithm,
                           ('n_gen', data['analysis']['params']['nGen']),
                           seed=1,
                           verbose=True,
                           save_history=True)
            
        print_optimization_summary(res)
        plot_pareto_and_dominated(res)
