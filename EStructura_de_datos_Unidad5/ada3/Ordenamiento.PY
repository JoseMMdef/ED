import json
import csv
import pandas as pd
import datetime
from docx import Document

# ============================================================
# LECTURA DE DATOS
# ============================================================

def leer_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def leer_csv(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def leer_excel(ruta):
    df = pd.read_excel(ruta)
    return df.to_dict(orient="records")

def leer_txt(ruta):
    datos = []
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")
            datos.append({"campo": partes[0]})
    return datos

def leer_docx(ruta):
    doc = Document(ruta)
    datos = []
    for p in doc.paragraphs:
        if p.text.strip():
            datos.append({"campo": p.text.strip()})
    return datos

# ============================================================
# NORMALIZACIÓN DE DATOS
# ============================================================

def normalizar_valor(valor):
    """Convierte cualquier tipo de dato a número"""
    try:
        return float(valor)
    except:
        # Si es fecha
        try:
            fecha = datetime.datetime.fromisoformat(valor)
            return fecha.timestamp()
        except:
            pass
        # Si es hora
        try:
            h, m = valor.split(":")
            return int(h) * 60 + int(m)
        except:
            pass
        # Si es texto
        return len(str(valor))

def normalizar_datos(lista, campo):
    for item in lista:
        item[campo] = normalizar_valor(item[campo])
    return lista

# ============================================================
# MÉTODO 1: INTERCALACIÓN
# ============================================================

def intercalar(lista_a, lista_b, campo):
    resultado = []
    i, j = 0, 0
    while i < len(lista_a) and j < len(lista_b):
        if lista_a[i][campo] <= lista_b[j][campo]:
            resultado.append(lista_a[i])
            i += 1
        else:
            resultado.append(lista_b[j])
            j += 1
    resultado.extend(lista_a[i:])
    resultado.extend(lista_b[j:])
    return resultado

# ============================================================
# MÉTODO 2: MEZCLA DIRECTA (MERGE SORT)
# ============================================================

def mezcla_directa(lista, campo):
    if len(lista) <= 1:
        return lista
    medio = len(lista) // 2
    izq = mezcla_directa(lista[:medio], campo)
    der = mezcla_directa(lista[medio:], campo)
    return fusionar(izq, der, campo)

def fusionar(izq, der, campo):
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i][campo] <= der[j][campo]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

# ============================================================
# MÉTODO 3: MEZCLA EQUILIBRADA
# ============================================================

def fusionar_runs(run_a, run_b, campo):
    resultado = []
    i = j = 0
    while i < len(run_a) and j < len(run_b):
        if run_a[i][campo] <= run_b[j][campo]:
            resultado.append(run_a[i])
            i += 1
        else:
            resultado.append(run_b[j])
            j += 1
    resultado.extend(run_a[i:])
    resultado.extend(run_b[j:])
    return resultado

def mezcla_equilibrada(datos, campo):
    runs = [[d] for d in datos]
    while len(runs) > 1:
        nuevos_runs = []
        for i in range(0, len(runs), 2):
            if i+1 < len(runs):
                nuevos_runs.append(fusionar_runs(runs[i], runs[i+1], campo))
            else:
                nuevos_runs.append(runs[i])
        runs = nuevos_runs
    return runs[0]

# ============================================================
# COMPARACIÓN DE MÉTODOS
# ============================================================

def comparar_metodos(datos, campo):
    mitad = len(datos)//2
    inter = intercalar(datos[:mitad], datos[mitad:], campo)
    merge = mezcla_directa(datos, campo)
    equil = mezcla_equilibrada(datos, campo)

    print("\n--- RESULTADOS ---")
    print("Intercalación:", [d[campo] for d in inter])
    print("Mezcla Directa:", [d[campo] for d in merge])
    print("Mezcla Equilibrada:", [d[campo] for d in equil])

# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":
    # Ejemplo con datos mixtos
    datos = [
        {"valor": "2024-05-07"},
        {"valor": "15:30"},
        {"valor": "Hola"},
        {"valor": 42},
        {"valor": "2023-01-01"},
    ]

    datos = normalizar_datos(datos, "valor")
    comparar_metodos(datos, "valor")
