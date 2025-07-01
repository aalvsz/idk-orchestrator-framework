import os
import pandas as pd
import ast

def expand_list_columns(df, keywords=["pos_list", "energy_list"]):
    """
    Busca columnas que contengan los keywords y expande las listas en columnas separadas.
    """
    new_columns = {}
    for col in df.columns:
        if any(kw in col for kw in keywords):
            sample_val = df[col].iloc[0]
            if isinstance(sample_val, str):
                try:
                    sample_val = ast.literal_eval(sample_val)
                except:
                    continue
            if isinstance(sample_val, list):
                max_len = max(df[col].apply(lambda x: len(ast.literal_eval(x)) if isinstance(x,str) else len(x)))
                for i in range(max_len):
                    new_col = f"{col}_{i}"
                    df[new_col] = df[col].apply(
                        lambda x: ast.literal_eval(x)[i] if isinstance(x,str) and len(ast.literal_eval(x))>i else (
                            x[i] if isinstance(x,list) and len(x)>i else None
                        )
                    )
                new_columns[col] = True
    df.drop(columns=list(new_columns.keys()), inplace=True)
    return df


def concat_clean_and_split(folder_path, merged_file="merged_clean.csv"):
    """
    Lee todos los CSV de una carpeta, concatena su contenido, limpia las
    filas que empiezan con coma, y divide en inputs/outputs.
    Además expande columnas de listas con nombres que contengan 'pos_list' o 'energy_list'
    y elimina columnas CO2 y dofs de outputs.
    """
    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    if not csv_files:
        print("⚠️ No se encontraron archivos CSV en la carpeta.")
        return

    dataframes = []
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, encoding="utf-8") as f:
            lines = [line for line in f if not line.startswith(",")]
        from io import StringIO
        clean_text = "".join(lines)
        df = pd.read_csv(StringIO(clean_text))
        dataframes.append(df)

    merged_df = pd.concat(dataframes, ignore_index=True)
    merged_csv_path = os.path.join(folder_path, merged_file)
    merged_df.to_csv(merged_csv_path, index=False)
    print(f"✅ Archivo limpio y combinado guardado en {merged_csv_path}")

    # Dividir en inputs y outputs
    input_df = merged_df.iloc[:, :16]
    output_df = merged_df.iloc[:, 16:]

    # expandir listas si hace falta
    output_df = expand_list_columns(output_df)

    # borrar columnas CO2 y dofs si existen
    output_df.drop(columns=[c for c in ["CO2","dofS"] if c in output_df.columns], inplace=True, errors="ignore")

    input_csv = os.path.join(folder_path, "inputs.csv")
    output_csv = os.path.join(folder_path, "outputs.csv")

    input_df.to_csv(input_csv, index=False)
    output_df.to_csv(output_csv, index=False)

    print(f"✅ Inputs guardados en {input_csv}")
    print(f"✅ Outputs guardados en {output_csv}")

    return input_df, output_df


merged = concat_clean_and_split(r"C:\Users\aalvarezsanz\OneDrive - DanobatGroup\Documentos\idk_framework\DOE_datos\Carga carro")
