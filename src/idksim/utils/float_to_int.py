import pandas as pd

# archivo de entrada
csv_file = r"C:\Users\aalvarezsanz\OneDrive - DanobatGroup\Documentos\csv_idk\soluciones_pareto.csv"

# leer el csv
df = pd.read_csv(csv_file)

# obtener el nombre de la última columna
last_col = df.columns[-1]

# convertir la última columna a int
df[last_col] = df[last_col].astype(int)

# guardar de nuevo el csv si quieres
df.to_csv(r"C:\Users\aalvarezsanz\OneDrive - DanobatGroup\Documentos\csv_idk\salida.csv", index=False)

print(f"✅ Columna {last_col} convertida a int y guardado en salida.csv")
