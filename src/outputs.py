class Output:
    """
    Clase que representa un objetivo de optimización.
    
    Permite definir:
      - name: Nombre del objetivo (ej. "metric").
      - function: "minimizar" o "maximizar" (por defecto se asume minimizar).
      - description: Descripción del objetivo.
    
    El método transform() se puede usar para ajustar el valor del objetivo a minimizar
    (por ejemplo, invirtiendo el signo en caso de maximización).
    """
    def __init__(self, config):
        """
        Inicializa el objetivo a partir de un diccionario de configuración.
        
        Se espera que config tenga las claves:
          - name: El nombre real del objetivo.
          - function: Indica "minimizar" o "maximizar" (en min. se deja igual, en máx. se invierte el signo).
          - description: Descripción del objetivo (opcional).
        """
        self.name = config.get("name", "")
        self.type = config.get("type", "results")
        # Por convención: "minimizar" implica dejar el valor tal cual,
        # "maximizar" se convierte a minimizar multiplicando por -1.
        self.function = config.get("function", "minimizar").lower()
        self.description = config.get("description", "")
        self.sign = 1 if self.function == "minimizar" else -1
        self.data = config.get("data", "scalar")
        if self.data == 'array':
            import pandas as pd
            self.parquet_path = config.get("parquet_path", None)
            self.column_name = config.get("column_name", None)
            df = pd.read_parquet(self.parquet_path)
            self.tiempos_obj = df.index.values  # array con los tiempos donde tienes valores objetivo
            self.valores_obj = df[self.column_name].values








    def transform(self, value):
        """
        Aplica la transformación necesaria al valor del objetivo.
        Por ejemplo, en un problema de maximización se multiplica por -1 para convertirlo en minimización.
        """
        return self.sign * value

    def __str__(self):
        return f"Output(name={self.name}, function={self.function}, description={self.description})"
