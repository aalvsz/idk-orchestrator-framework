import os
import pickle
import numpy as np


# =============================================================================
# Clase model: Encapsula el ROM, lo carga desde un pickle y define el método idk_run
# =============================================================================
class model:
    def __init__(self):
        self.pathAplication = None
        self.pathModel = None
        self.rom = None

    def load_model(self):
        """
        Carga el ROM desde el archivo pickle.
        """
        if self.pathModel is None or not os.path.isfile(self.pathModel):
            raise FileNotFoundError("El archivo del modelo no existe: {}".format(self.pathModel))
        with open(self.pathModel, 'rb') as f:
            self.rom = pickle.load(f)
    
    def idk_run(self, input_dict):
        """
        Ejecuta el ROM recibido un diccionario de parámetros en entrada.
        Se asume que el objeto 'rom' tiene implementado un método 'idk_run'
        que recibe un diccionario y devuelve otro diccionario con los resultados.
        """
        if self.rom is None:
            self.load_model()
        # Llamada al método idk_run del ROM (asumiendo que existe)
        # Aquí se espera que input_dict tenga las variables de entrada y que el resultado
        # sea un diccionario cuyas claves correspondan a los nombres de los objetivos.
        result = self.rom.idk_run(input_dict)
        return result
    