import os
import pickle
import importlib.util
import logging

class idksimObject:
    def __init__(self, data):
        self.pathModel = data['model']['pathModel']
        self.model_type = data['model']['modelType']
        self.class_name = data['model']['className']
        self.model = None  # modelo pickle o clase

        # Crear directorio del log si no existe
        log_dir = data['analysis']['params']['tracking']['path']
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, 'idk_model.log')

        # Configurar logger propio
        self.logger = logging.getLogger('idksimObjectLogger')
        self.logger.setLevel(logging.INFO)
        
        # Eliminar handlers existentes para evitar duplicados
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            
        # Configurar file handler
        file_handler = logging.FileHandler(log_path, mode='a')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Evitar que los mensajes se propaguen al logger root
        self.logger.propagate = False
        
        # Mensaje de prueba
        self.logger.info("Logger configurado correctamente")

    def load_model(self):
        try:
            if self.pathModel is None or not os.path.isfile(self.pathModel):
                raise FileNotFoundError(f"El archivo del modelo no existe: {self.pathModel}")

            self.logger.info(f"Cargando modelo desde: {self.pathModel}")
            
            if self.model_type != 'class':
                with open(self.pathModel, 'rb') as f:
                    self.model = pickle.load(f)
                self.logger.info("Modelo cargado desde archivo pickle")
            else:
                module_name = os.path.splitext(os.path.basename(self.pathModel))[0]
                spec = importlib.util.spec_from_file_location(module_name, self.pathModel)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                class_ = getattr(module, self.class_name)
                self.model = class_()
                self.logger.info(f"Modelo de clase {self.class_name} instanciado correctamente")
                
        except Exception as e:
            self.logger.error(f"Error al cargar el modelo: {str(e)}")
            raise

    def idk_run(self, input_dict):
        try:
            if self.model is None:
                self.load_model()

            self.logger.info(f"Modelo ejecutado con los parámetros: {input_dict}")
            print(f"Modelo ejecutado con los parámetros: {input_dict}")

            result = self.model.idk_run(input_dict)

            self.logger.info(f"Resultado del modelo: {result}")
            print(f"Resultado del modelo: {result}")

            return result
        except Exception as e:
            self.logger.error(f"Error en idk_run: {str(e)}")
            raise