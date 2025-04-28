import yaml
import sys, os
import plotly.io as pio
pio.renderers.default = 'browser'
from src.model import idksimObject
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

        
    # 3) Inicializar la clase model y asignar rutas
    objModel = idksimObject()
    objModel.pathAplication = data['model']['pathAplication']
    objModel.pathModel = data['model']['pathModel']
    
    problem = None

    # Verificar el tipo de análisis y algoritmo especificado
    if data['analysis']['type'] == 'optimization':
        outputs = []
        for f_key in data['analysis']['params']['fObj']:
            outputs.append(Output(data[f_key]))

        if data['analysis']['params']['algorithm'] == 'NSGA2':
            from idkopt.algorithms.genetic_algorithm import GeneticAlgorithm
            from idkopt.algorithms.mixed_var_genetic import MixedVariableGeneticProblem
            from pymoo.algorithms.moo.nsga2 import NSGA2
            from pymoo.core.mixed import MixedVariableMating, MixedVariableSampling, MixedVariableDuplicateElimination
            from pymoo.operators.crossover.sbx import SBX
            from pymoo.operators.mutation.pm import PM
            from pymoo.optimize import minimize

            # Inicializar el problema de optimización definido en la clase opt_genalg
            problem = MixedVariableGeneticProblem(data, objModel, parameters, outputs)

            # Inicializar el algoritmo NSGA2 para el problema
            pop_size = data['analysis']['params']['popSize']
            n_gen_total = data['analysis']['params']['nGen']

            if data['analysis']['params']['settings'] == 'custom':
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
                    from pymoo.algorithms.moo.nsga2 import RankAndCrowdingSurvival
                    selection = TournamentSelection(func_comp=RankAndCrowdingSurvival,
                                                     pressure=slct.get('n_parents', 2))
                    
            else: 
                crossover = None
                mutation = None
                selection = None

            algorithm = NSGA2(
                pop_size=pop_size,
                sampling=MixedVariableSampling(),
                mating=MixedVariableMating(eliminate_duplicates=MixedVariableDuplicateElimination()),
                eliminate_duplicates=MixedVariableDuplicateElimination(),
                crossover=crossover,
                mutation=mutation,
                selection=selection
            )

            # Ejecutar la optimización utilizando la función minimize de pymoo
            res = minimize(problem,
                   algorithm,
                   ('n_gen', n_gen_total),
                   seed=2,
                   verbose=False,
                   save_history=True)


        elif data['analysis']['params']['algorithm'] == 'NSGA3':
            
            from pymoo.algorithms.moo.nsga3 import NSGA3
            from pymoo.util.ref_dirs import get_reference_directions
            from idkopt.algorithms.genetic_algorithm import GeneticAlgorithm
            from idkopt.algorithms.mixed_var_genetic import MixedVariableGeneticProblem
            from pymoo.core.mixed import MixedVariableMating, MixedVariableSampling, MixedVariableDuplicateElimination
            from pymoo.operators.crossover.sbx import SBX
            from pymoo.operators.mutation.pm import PM
            from pymoo.optimize import minimize

            # Inicializar el problema de optimización definido en la clase opt_genalg
            problem = MixedVariableGeneticProblem(data, objModel, parameters, outputs)

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
            

        elif data['analysis']['params']['algorithm'] == 'MixedVariableGA':
            
            from idkopt.algorithms.mixed_var_genetic import MixedVariableGeneticProblem
            from pymoo.core.mixed import MixedVariableGA
            from pymoo.optimize import minimize

            # Inicializar el problema de optimización definido en la clase opt_genalg
            problem = MixedVariableGeneticProblem(data, objModel, parameters, outputs)

            # Inicializar el algoritmo NSGA2 para el problema
            pop_size = data['analysis']['params']['popSize']
            n_gen_total = data['analysis']['params']['nGen']
            
            algorithm = MixedVariableGA(
                pop_size=pop_size
            )

            # Ejecutar la optimización utilizando la función minimize de pymoo
            res = minimize(problem,
                   algorithm,
                   ('n_gen', n_gen_total),
                   seed=2,
                   verbose=False,
                   save_history=True)
        

        elif data['analysis']['params']['algorithm'] == 'minimize':
            
            from idkopt.algorithms.minimize import Minimization

            problem = Minimization(data, objModel, Parameter, Output)
            res = problem.solve()


        elif data['analysis']['params']['algorithm'] == 'least squares':

            from idkopt.algorithms.least_squares import LeastSquares

            problem = LeastSquares(data, objModel, Parameter, Output)
            res = problem.solve()


    elif data['analysis']['type'] == 'doe':

        from idkdoe.model import idkDOE
        doe = idkDOE(data)
        doe.run_doe(method=data['analysis']['params']['method'].upper(), n_samples=data['analysis']['params'].get('n_samples', 10), output_prefix="doe_lhs_results")




    print_optimization_summary(res, parameters, outputs)
    plot_pareto_and_dominated(res)
    write_results_file(data, res, parameters, outputs)
