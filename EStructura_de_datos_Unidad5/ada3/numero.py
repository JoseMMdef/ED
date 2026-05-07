# ============================================================
# MÉTODO 1: INTERCALACIÓN
# ============================================================

def intercalar(lista_a, lista_b):
    resultado = []
    i, j = 0, 0
    while i < len(lista_a) and j < len(lista_b):
        if lista_a[i] <= lista_b[j]:
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

def mezcla_directa(lista):
    if len(lista) <= 1:
        return lista
    medio = len(lista) // 2
    izq = mezcla_directa(lista[:medio])
    der = mezcla_directa(lista[medio:])
    return fusionar(izq, der)

def fusionar(izq, der):
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
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

def fusionar_runs(run_a, run_b):
    resultado = []
    i = j = 0
    while i < len(run_a) and j < len(run_b):
        if run_a[i] <= run_b[j]:
            resultado.append(run_a[i])
            i += 1
        else:
            resultado.append(run_b[j])
            j += 1
    resultado.extend(run_a[i:])
    resultado.extend(run_b[j:])
    return resultado

def mezcla_equilibrada(datos):
    runs = [[d] for d in datos]
    while len(runs) > 1:
        nuevos_runs = []
        for i in range(0, len(runs), 2):
            if i+1 < len(runs):
                nuevos_runs.append(fusionar_runs(runs[i], runs[i+1]))
            else:
                nuevos_runs.append(runs[i])
        runs = nuevos_runs
    return runs[0]

# ============================================================
# COMPARACIÓN DE MÉTODOS
# ============================================================

def comparar_metodos(datos):
    mitad = len(datos)//2
    inter = intercalar(sorted(datos[:mitad]), sorted(datos[mitad:]))
    merge = mezcla_directa(datos)
    equil = mezcla_equilibrada(datos)

    print("\n--- RESULTADOS ---")
    print("Intercalación:", inter)
    print("Mezcla Directa:", merge)
    print("Mezcla Equilibrada:", equil)

# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":
    # Ejemplo con números
    datos = [42, 15, 7, 99, 23, 8, 65, 31]

    print("Datos originales:", datos)
    comparar_metodos(datos)
