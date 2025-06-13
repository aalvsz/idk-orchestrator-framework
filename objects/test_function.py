import numpy as np
import time

class TestFunctionAnalytic:
    """
    Función de prueba Branin–Hoo con interfaz idk_run.
    
    Inputs:
      - 'x1', 'x2' en un dict.
    Outputs:
      - 'time': vector de tiempos dummy (10 puntos entre 0 y 1).
      - 'branin': valor escalar de la función en (x1, x2).
    """

    def __init__(self, simulate_costly=False, sleep_time=0.1):
        # Si simulate_costly=True, duerme sleep_time segundos para simular coste
        self.simulate_costly = simulate_costly
        self.sleep_time = sleep_time

    def idk_run(self, inputs: dict) -> dict:
        # Opcionalmente simulamos un coste elevado
        if self.simulate_costly:
            time.sleep(self.sleep_time)

        x1 = inputs.get('x1', 0.0)
        x2 = inputs.get('x2', 0.0)

        # Parámetros estándar de Branin
        a = 1.0
        b = 5.1 / (4 * np.pi**2)
        c = 5.0 / np.pi
        r = 6.0
        s = 10.0
        t = 1.0 / (8 * np.pi)

        # Cálculo de la función
        branin = a * (x2 - b * x1**2 + c * x1 - r)**2 + s * (1 - t) * np.cos(x1) + s

        return {
            'branin': branin
        }
