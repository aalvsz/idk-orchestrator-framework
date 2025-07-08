import pandas as pd
import os

def parse_solutions_txt(txt_file, output_csv="soluciones_inputs.csv"):
    with open(txt_file, encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    
    data = []
    current = {}
    for line in lines:
        line = line.strip()
        if line.startswith("---"):
            if current:
                data.append(current)
                current = {}
        elif line.startswith("Objetivos"):
            continue  # saltamos la línea "Objetivos:"
        elif ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            val_str = value.strip()
            try:
                val = float(val_str)
            except:
                val = None
            # solo guardamos parámetros de entrada
            if key not in ["Peso", "elastic_energy"]:
                current[key] = val
    # no olvidar la última
    if current:
        data.append(current)
    
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica", output_csv), index=False)
    print(f"✅ Archivo CSV generado: {output_csv}")


def merge_two_csv():
    # Rutas a tus archivos
    inputs_csv = r"C:\Users\aalvarezsanz\OneDrive - DanobatGroup\Documentos\idk_framework\DOE_datos\Carga carro\inputs.csv"
    outputs_csv = r"C:\Users\aalvarezsanz\OneDrive - DanobatGroup\Documentos\idk_framework\DOE_datos\Carga carro\outputs.csv"

    # Cargar
    df_inputs = pd.read_csv(inputs_csv)
    df_outputs = pd.read_csv(outputs_csv)

    # Revisar que tengan el mismo número de filas
    if len(df_inputs) != len(df_outputs):
        raise ValueError(f"Los CSV tienen distinto número de filas: inputs({len(df_inputs)}) vs outputs({len(df_outputs)})")

    # Concatenar horizontalmente
    merged_df = pd.concat([df_inputs, df_outputs], axis=1)

    # Mostrar
    print(merged_df.head())

    # (opcional) guardar a disco
    merged_df.to_csv(r"C:\Users\aalvarezsanz\OneDrive - DanobatGroup\Documentos\idk_framework\DOE_datos\Carga carro\merged.csv", index=False)


if __name__ == "__main__":
    # reemplaza con la ruta real a tu fichero de texto
    #txt_file = r"D:\idk_framework\idksimulation\results\__ROM_travesano_peso_en_elastica\results.csv"
    #parse_solutions_txt(txt_file)

    merge_two_csv()
