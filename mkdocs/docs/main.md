# Ejecución de idkSIM

Existen dos maneras de ejecutar `idkSIM`.

**Opcional**: podemos pasar un diccionario personalizado como argumento a la función `idk_run()` para sobrescribir parámetros definidos en el archivo YAML.

---

## Opción 1 – Instalar como paquete

1. Instalamos `idkSIM` y sus dependencias desde GitLab con:

```bash
pip install "idksimulation @ git+https://kodea.danobatgroup.com/dip/precision/ideko/simulation/idksimulation.git@main"
pip install "idkrom @ git+https://kodea.danobatgroup.com/dip/precision/ideko/simulation/idkROM.git@main"
pip install "idkdoe @ git+https://kodea.danobatgroup.com/dip/precision/ideko/simulation/idkdoe.git@main"
pip install "idkopt @ git+https://kodea.danobatgroup.com/dip/precision/ideko/simulation/idkopt.git@main"
```

> ⚠️ Requiere acceso autorizado a los repositorios privados de Kodea.

2. Creamos un script simple como el siguiente:

```python
from idksimulation.model import idkSIM

sim = idkSIM(config_yml_path="path_a_tu_yaml.yml")
sim.idk_run(dict_hyperparams={"population_size": 30, "generations": 50})
```

---

## Opción 2 – Ejecutar directamente el `main.py`

También puedes ejecutar directamente el script `main.py` que se encuentra en la carpeta `src`, modificando el path al archivo YAML que desees usar.

---

## Ejemplo de YAML de configuración para `idkSIM`

```yaml
model:
  type: simulink
  model name: thermal_model
  m file: src/simulink_interface/run_model.m
  output folder: results/nsga2_simulink
  sampling time: 0.1

analysis:
  type: optimization
  objective: minimize
  parallel: true
  variables:
    - name: gain_p
      type: continuous
      bounds: [0.1, 10.0]
    - name: gain_i
      type: continuous
      bounds: [0.1, 5.0]
  objectives:
    - name: overshoot
    - name: rise_time
  constraints:
    - name: overshoot
      type: upper
      limit: 15.0
    - name: rise_time
      type: upper
      limit: 5.0

optimizer:
  type: nsga2
  population_size: 20
  generations: 40
  crossover_probability: 0.9
  mutation_probability: 0.1
  tournament_size: 2

idk_params:
  model_name: [model, model name]
  sampling_time: [model, sampling time]
  output_path: [model, output folder]
  gain_p: [analysis, variables, 0, initial]
  gain_i: [analysis, variables, 1, initial]
  population_size: [optimizer, population_size]
  generations: [optimizer, generations]
```

---

## Sección `model`

Define los detalles del modelo Simulink:

- **`type`**: tipo de modelo (ej. `simulink`).
- **`model name`**: nombre del modelo Simulink.
- **`m file`**: script `.m` para ejecutar la simulación.
- **`output folder`**: carpeta donde se almacenan los resultados.
- **`sampling time`**: tiempo de muestreo del modelo.

---

## Sección `analysis`

Define el tipo de análisis a realizar:

- **`type`**: tipo de análisis (`optimization`).
- **`objective`**: tipo de objetivo (`minimize`, `maximize`, etc.).
- **`parallel`**: si se permite paralelizar las evaluaciones.
- **`variables`**: lista de variables a optimizar, con tipo (`continuous`) y límites.
- **`objectives`**: métricas que se desean optimizar.
- **`constraints`**: restricciones aplicadas sobre los objetivos.

---

## Sección `optimizer`

Configura el algoritmo de optimización (en este caso, NSGA-II):

- **`type`**: algoritmo usado (`nsga2`, `ga`, etc.).
- **`population_size`**: número de individuos por generación.
- **`generations`**: número total de generaciones.
- **`crossover_probability`**: probabilidad de cruce.
- **`mutation_probability`**: probabilidad de mutación.
- **`tournament_size`**: tamaño del torneo para selección.

---

## Sección `idk_params`

### Sistema de asignación de parámetros (`idk_params`)

La sección `idk_params` del archivo de configuración actúa como un **mapa de redirección de claves**. Permite que cualquier clave que se pase al método `idk_run()` como diccionario de hiperparámetros sea vinculada directamente con su correspondiente entrada dentro del archivo YAML.

Esto permite que los usuarios **sobrescriban valores del YAML sin modificar el archivo directamente**, simplemente pasando un diccionario como argumento.

---

### Funcionamiento

- Cada clave de `idk_params` representa un **alias o sinónimo** que el usuario puede usar como entrada en el diccionario `dict_hyperparams`.
- Su valor asociado es una **ruta de acceso** que indica **dónde en el YAML de configuración se encuentra el parámetro real que debe modificarse**.
- Esa ruta es una lista que se interpreta como niveles jerárquicos en el YAML (`sección → subsección → parámetro`).

---

### Ejemplo de uso

Supongamos que en tu archivo `config.yml` tienes:

```yaml
optimizer:
  population_size: 20
```

Y en `idk_params` defines:

```yaml
population_size: [optimizer, population_size]
```

Entonces, al ejecutar:

```python
sim.idk_run({"population_size": 50})
```

El valor original (`20`) será reemplazado por `50` en tiempo de ejecución.