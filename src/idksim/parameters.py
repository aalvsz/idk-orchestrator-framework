import numpy as np
from pymoo.core.variable import Real, Choice

class Parameter:
    def __init__(self, config):
        """
        Inicializa un parámetro de optimización a partir de su configuración (un diccionario extraído del YAML).
        
        Se espera que config tenga las claves:
          - name: Nombre real del parámetro (ej. "n_capas").
          - default: Valor por defecto.
          - type: "discreto", "continuo" o "constante".
          - value: Valor inicial (por convención, una lista con un valor).
          - value interval: 
              * Para discretos: una lista explícita con todos los valores posibles.  
                Ejemplo: [1, 2, 3, 5, 8, 10]
              * Para continuos: una lista [min, max].
          - description: Descripción del parámetro.
        """
        self.name = config.get("name", "unnamed")
        self.default = config.get("default", None)
        self.var_type = config.get("type", "").lower()  # "discreto", "continuo" o "constante"
        self.value_interval = config.get("value interval", None)
        self.description = config.get("description", "")
        self.is_constant = self.var_type == "constante" 

        # Validaciones importantes
        if self.is_constant and self.default is None:
            raise ValueError(f"❌ El parámetro constante '{self.name}' debe tener un valor 'default' definido.")

        if not self.is_constant and self.value_interval is None:
            raise ValueError(f"❌ El parámetro '{self.name}' necesita una clave 'value interval'.")

    def get_variable(self):
        """
        Retorna la variable de optimización para pymoo.
        
        - Para discretos: Choice con la lista de opciones.
        - Para continuos: Real con los límites [min, max].
        - Para constantes: None (no se optimiza).
        """
        if self.var_type == "constante":
            return None
        elif self.var_type == "discreto":
            return Choice(options=self.value_interval)
        else:
            return Real(bounds=(self.value_interval[0], self.value_interval[1]))
    
    def get_lower(self):
        """
        Retorna el valor mínimo.
        - Para discretos: el mínimo de la lista.
        - Para continuos: el primer elemento de value_interval.
        - Para constantes: el valor por defecto.
        """
        if self.var_type == "constante":
            return self.default
        elif self.var_type == "discreto":
            return min(self.value_interval)
        else:
            return self.value_interval[0]
    
    def get_upper(self):
        """
        Retorna el valor máximo.
        - Para discretos: el máximo de la lista.
        - Para continuos: el segundo elemento de value_interval.
        - Para constantes: el valor por defecto.
        """
        if self.var_type == "constante":
            return self.default
        elif self.var_type == "discreto":
            return max(self.value_interval)
        else:
            return self.value_interval[1]
    
    def __str__(self):
        return f"Parameter(name={self.name}, type={self.var_type}, default={self.default}, " \
               f"value_interval={self.value_interval})"
