import numpy as np
import yaml

class Constraints:
    def __init__(self, config=None, path=None, n_var=None):
        """
        Inicializa las restricciones desde un diccionario o un archivo YAML.
        """
        if path:
            with open(path, 'r') as f:
                config = yaml.safe_load(f)
        self.config = config or {}
        self.n_var = n_var
        self.bounds = self._parse_bounds()
        self.custom_constraints = self._parse_custom_constraints()

    def _parse_bounds(self):
        bounds_cfg = self.config.get('bounds', None)
        if bounds_cfg is not None:
            return [(float(b[0]), float(b[1])) for b in bounds_cfg]
        elif self.n_var:
            return [(0.0, 1.0)] * self.n_var  # Default bounds
        else:
            return None

    def _parse_custom_constraints(self):
        constraints = self.config.get('custom', [])
        funcs = []
        for c in constraints:
            expr = c.get('expression')
            kind = c.get('type', 'ineq')
            if expr:
                func = eval(f"lambda x: {expr}", {"np": np})
                funcs.append((func, kind))
        return funcs

    def as_scipy_constraints(self):
        """
        Devuelve las restricciones en formato compatible con scipy.optimize.minimize.
        """
        return [
            {'type': kind, 'fun': func}
            for func, kind in self.custom_constraints
        ]

    def apply_bounds(self, x):
        """
        Aplica los límites definidos a un vector de variables.
        """
        if self.bounds is None:
            return x
        return np.clip(x, [b[0] for b in self.bounds], [b[1] for b in self.bounds])


    # DOE
    def check_feasibility(self, x):
        """
        Devuelve True si el vector x cumple con todas las restricciones personalizadas.
        """
        for func, kind in self.custom_constraints:
            val = func(x)
            if kind == 'ineq' and val < 0:
                return False
            elif kind == 'eq' and not np.isclose(val, 0.0, atol=1e-6):
                return False
        return True
    
    # DOE
    def sample_feasible(self, sampler, max_tries=1000):
        """
        Genera una muestra válida usando el sampler dado, comprobando factibilidad.
        """
        for _ in range(max_tries):
            x = sampler()
            if self.check_feasibility(x):
                return x
        raise RuntimeError("No se pudo generar un punto factible en el límite de intentos.")

    def get_bounds(self):
        return self.bounds
