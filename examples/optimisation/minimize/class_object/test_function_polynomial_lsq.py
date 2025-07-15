import numpy as np
import time

class TestFitParabolaLeastSquares:
    """
    Función de prueba simple para least_squares: ajuste de una parábola a datos objetivos.

    Inputs:
      - 'a', 'b', 'c' en un dict.
    Outputs:
      - 'residuals': vector con los residuos (diferencias entre predicción y valores reales).
    """

    def __init__(self, simulate_costly=False, sleep_time=0.1):
        self.simulate_costly = simulate_costly
        self.sleep_time = sleep_time

        # Datos de referencia (x, y) de la curva objetivo: y = 2x² - 3x + 1
        self.x_data = np.linspace(-5, 5, 11)
        self.y_target = 2 * self.x_data**2 - 3 * self.x_data + 1

    def idk_run(self, inputs: dict, **kwargs) -> dict:
        if self.simulate_costly:
            time.sleep(self.sleep_time)


        # Fusionar constantes si vienen por kwargs
        if isinstance(kwargs, dict):
            inputs = {**inputs, **kwargs}

        # Obtener parámetros del modelo
        a = inputs.get('a', 0.0)
        b = inputs.get('b', 0.0)
        c = inputs.get('c', 0.0)

        # Evaluar modelo con los parámetros
        y_model = a * self.x_data**2 + b * self.x_data + c

        # Calcular residuos
        residuals = y_model - self.y_target

        return {
            'residuals': residuals
        }
