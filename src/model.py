import os
import pickle

# =============================================================================
# Clase model: Encapsula el modelo, lo carga desde un pickle y define el método idk_run
# =============================================================================
class idksimObject:
    def __init__(self):
        self.pathAplication = None
        self.pathModel = None
        self.model = None # es el modelo en formato pickle

    def load_model(self):
        """
        Carga el modelo desde el archivo pickle.
        """
        if self.pathModel is None or not os.path.isfile(self.pathModel):
            raise FileNotFoundError("El archivo del modelo no existe: {}".format(self.pathModel))
        with open(self.pathModel, 'rb') as f:
            self.model = pickle.load(f)
    
    def idk_run(self, input_dict):
        """
        Ejecuta el modelo recibido un diccionario de parámetros en entrada.
        Se asume que el objeto 'model' tiene implementado un método 'idk_run'
        que recibe un diccionario y devuelve otro diccionario con los resultados.
        """
        print(f"Modelo ejecutado con los parámetros: {input_dict}")

        #if self.model is None:
        self.load_model()
        result = self.model.idk_run(input_dict) # aqui entramos al metodo idk_run del modelo (.pkl)

        print(f"Resultado del modelo: {result}")
        return result
    