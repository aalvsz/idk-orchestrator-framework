import os
import pickle
import importlib.util
import logging

class idksimObject:
    """
    Clase para cargar y ejecutar modelos de simulación en idksimulation.

    Permite cargar modelos guardados como archivos pickle o como clases Python,
    y ejecutar su método `idk_run` con un diccionario de parámetros de entrada.
    Incluye registro detallado de eventos y errores en un archivo de log.
    """

    def __init__(self, data):
        """
        Inicializa el objeto idksimObject con la configuración y prepara el logger.

        Args:
            data (dict): Diccionario de configuración, debe incluir:
                - data['model']['pathModel']: Ruta al archivo del modelo.
                - data['model']['modelType']: Tipo de modelo ('pickle' o 'class').
                - data['model']['className']: Nombre de la clase (si aplica).
                - data['analysis']['params']['tracking']['path']: Ruta para guardar logs.
        """
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
        """
        Carga el modelo desde archivo pickle o como clase Python, según la configuración.

        Si el modelo es tipo 'pickle', lo carga usando pickle.
        Si el modelo es tipo 'class', importa dinámicamente el módulo y crea una instancia de la clase.

        Raises:
            FileNotFoundError: Si el archivo del modelo no existe.
            Exception: Si ocurre un error durante la carga.
        """
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

    def idk_run(self, input_dict, **kwargs):
        """
        Ejecuta el método `idk_run` del modelo cargado con los parámetros de entrada dados.

        Si el modelo no está cargado, lo carga automáticamente antes de ejecutar.
        Registra la ejecución y el resultado en el archivo de log.

        Args:
            input_dict (dict): Diccionario con los parámetros de entrada para el modelo.
            kwargs: Diccionario con variables constantes (opcional).

        Returns:
            result: Resultado devuelto por el método `idk_run` del modelo.

        Raises:
            Exception: Si ocurre un error durante la ejecución.
        """
        try:
            if self.model is None:
                self.load_model()

            log_msg = f"Modelo ejecutado con los parámetros: {input_dict}"
            if 'kwargs':
                log_msg += f" + constantes: {kwargs}"
            
            self.logger.info(log_msg)
            print(log_msg)

            result = self.model.idk_run(input_dict, **kwargs)

            self.logger.info(f"Resultado del modelo: {result}")
            print(f"Resultado del modelo: {result}")

            return result

        except Exception as e:
            self.logger.error(f"Error en idk_run: {str(e)}")
            raise
