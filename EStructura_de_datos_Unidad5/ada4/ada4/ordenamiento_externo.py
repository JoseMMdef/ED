"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              LIBRERÍA DE ORDENAMIENTO EXTERNO                                ║
║              Archivo: ordenamiento_externo.py                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Algoritmos incluidos:                                                       ║
║    1. Intercalación       — Fusiona dos listas YA ordenadas                  ║
║    2. Mezcla Directa      — Merge Sort recursivo clásico                     ║
║    3. Mezcla Equilibrada  — Merge Sort iterativo por runs                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ¿QUÉ ES ORDENAMIENTO EXTERNO?                                               ║
║    Los algoritmos externos están diseñados para manejar grandes              ║
║    volúmenes de datos que NO caben completamente en memoria RAM.             ║
║    Trabajan dividiendo los datos en bloques (runs/segmentos) que se          ║
║    procesan por separado y luego se FUSIONAN (mezclan).                      ║
║                                                                              ║
║    En esta librería se simulan los algoritmos con listas en memoria,         ║
║    pero la lógica de fusión es idéntica a la que se usaría con archivos.     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  IMPORTANTE: Todos los algoritmos retornan una NUEVA lista ordenada.        ║
║              La lista original NO se modifica.                               ║
║  ORIGEN:     Basado en ADA3                                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIÓN AUXILIAR COMPARTIDA: _fusionar_dos_listas
# ══════════════════════════════════════════════════════════════════════════════
#
#  Esta función es la "operación fundamental" de todos los algoritmos externos.
#  Toma dos listas YA ORDENADAS y produce una nueva lista también ordenada.
#
#  Funciona con dos punteros (i y j) que recorren simultáneamente ambas listas:
#    - Compara los elementos en las posiciones i y j
#    - Agrega el menor al resultado y avanza ese puntero
#    - Cuando una lista se agota, agrega el resto de la otra
#
#  COMPLEJIDAD: O(n + m) donde n y m son los tamaños de cada lista
# ──────────────────────────────────────────────────────────────────────────────

def _fusionar_dos_listas(lista_a: list, lista_b: list) -> list:
    """
    Función auxiliar interna.
    Fusiona dos listas YA ORDENADAS en una nueva lista también ordenada.

    Usa el algoritmo de dos punteros:
      - i apunta al inicio de lista_a
      - j apunta al inicio de lista_b
      - En cada paso, el menor de los dos se agrega al resultado

    Args:
        lista_a: Primera lista ordenada.
        lista_b: Segunda lista ordenada.

    Returns:
        Nueva lista con todos los elementos de ambas, ordenada.

    Ejemplo:
        >>> _fusionar_dos_listas([1, 3, 5], [2, 4, 6])
        [1, 2, 3, 4, 5, 6]
    """
    resultado = []
    i = 0  # Puntero para lista_a
    j = 0  # Puntero para lista_b

    # Mientras ambas listas tengan elementos sin procesar
    while i < len(lista_a) and j < len(lista_b):
        if lista_a[i] <= lista_b[j]:
            resultado.append(lista_a[i])  # El de lista_a es menor o igual
            i += 1
        else:
            resultado.append(lista_b[j])  # El de lista_b es menor
            j += 1

    # Agrega los elementos restantes (una de las dos listas ya se agotó)
    resultado.extend(lista_a[i:])  # Si quedaron elementos en lista_a
    resultado.extend(lista_b[j:])  # Si quedaron elementos en lista_b

    return resultado


# ══════════════════════════════════════════════════════════════════════════════
# 1. INTERCALACIÓN
# ══════════════════════════════════════════════════════════════════════════════
#
#  IDEA PRINCIPAL:
#    La intercalación NO es un algoritmo de ordenamiento completo por sí mismo.
#    Es la OPERACIÓN BASE de todos los métodos de mezcla.
#    Recibe DOS listas que ya están ordenadas individualmente
#    y las fusiona en una sola lista ordenada.
#
#    Analogía: como mezclar dos mazos de cartas ya ordenadas
#    comparando las cartas del tope de cada mazo.
#
#  EN ORDENAMIENTO EXTERNO:
#    Se usa cuando los datos están divididos en dos archivos/bloques
#    ordenados y necesitamos combinarlos en uno solo.
#
#  IMPORTANTE: Las listas de entrada DEBEN estar ordenadas.
#    Esta función ordena las mitades antes de intercalar
#    para garantizar un resultado correcto.
#
#  COMPLEJIDAD TEMPORAL: O(n log n) en total (O(n) la intercalación pura)
#  COMPLEJIDAD ESPACIAL: O(n) — necesita espacio para el resultado
#
#  VENTAJAS:
#    ✔ O(n) si las listas ya están ordenadas
#    ✔ Estable
#    ✔ Fácil de paralelizar
#    ✔ Fundamental para ordenamiento externo
#
#  DESVENTAJAS:
#    ✘ Requiere que las listas de entrada estén ordenadas
#    ✘ Necesita memoria adicional para el resultado
# ──────────────────────────────────────────────────────────────────────────────

def intercalacion(coleccion: list) -> list:
    """
    Ordena una lista usando el método de Intercalación.

    Estrategia:
        1. Divide la lista en dos mitades
        2. Ordena cada mitad por separado (con sorted())
        3. Intercala las dos mitades ordenadas con el algoritmo de dos punteros

    Nota académica:
        En un escenario real de ordenamiento externo, las dos mitades
        estarían en archivos separados ya ordenados. Aquí simulamos
        ese proceso con listas en memoria.

    Args:
        coleccion: Lista de elementos comparables.

    Returns:
        Nueva lista con los elementos ordenados de menor a mayor.

    Ejemplo:
        >>> intercalacion([5, 1, 4, 2, 8, 3, 7, 6])
        [1, 2, 3, 4, 5, 6, 7, 8]
    """
    # Copia para no modificar la lista original
    arr = list(coleccion)
    n = len(arr)

    if n <= 1:
        return arr  # Lista de 0 o 1 elemento ya está ordenada

    # Paso 1: Dividir en dos mitades
    mitad = n // 2
    parte_a = arr[:mitad]   # Primera mitad
    parte_b = arr[mitad:]   # Segunda mitad

    # Paso 2: Ordenar cada mitad (simulamos que vienen pre-ordenadas del disco)
    parte_a_ordenada = sorted(parte_a)
    parte_b_ordenada = sorted(parte_b)

    # Paso 3: Intercalar las dos partes ordenadas
    return _fusionar_dos_listas(parte_a_ordenada, parte_b_ordenada)


# ══════════════════════════════════════════════════════════════════════════════
# 2. MEZCLA DIRECTA  (Direct Merge Sort)
# ══════════════════════════════════════════════════════════════════════════════
#
#  IDEA PRINCIPAL:
#    Implementación clásica y recursiva de Merge Sort (dividir y mezclar).
#
#    DIVIDE: Si la lista tiene más de 1 elemento, la divide en dos mitades.
#    VENCERÁS: Ordena cada mitad recursivamente.
#    COMBINA: Fusiona las dos mitades ordenadas usando _fusionar_dos_listas.
#
#    Árbol de recursión para [38, 27, 43, 3]:
#      [38, 27, 43, 3]
#        ├── [38, 27]
#        │     ├── [38] ← caso base
#        │     └── [27] ← caso base
#        │     └── fusionar → [27, 38]
#        └── [43, 3]
#              ├── [43] ← caso base
#              └── [3]  ← caso base
#              └── fusionar → [3, 43]
#        └── fusionar → [3, 27, 38, 43]
#
#  EN ORDENAMIENTO EXTERNO:
#    Cada "llamada recursiva" puede representar trabajar con un bloque
#    de datos en disco. La fusión combina bloques ordenados en uno mayor.
#
#  COMPLEJIDAD TEMPORAL: O(n log n) — siempre, en todos los casos
#  COMPLEJIDAD ESPACIAL: O(n) — necesita espacio para copias temporales
#
#  VENTAJAS:
#    ✔ O(n log n) GARANTIZADO
#    ✔ Estable
#    ✔ Rendimiento predecible
#    ✔ Base de muchos algoritmos de ordenamiento externo reales
#
#  DESVENTAJAS:
#    ✘ Requiere O(n) de memoria extra
#    ✘ Muchas llamadas recursivas para listas muy grandes (stack overflow)
#    ✘ Más lento que Quick Sort en la práctica para datos en RAM
# ──────────────────────────────────────────────────────────────────────────────

def mezcla_directa(coleccion: list) -> list:
    """
    Ordena una lista usando Mezcla Directa (Merge Sort recursivo).

    Estrategia (Divide y Vencerás):
        Caso base: lista de 0 o 1 elemento → ya está ordenada, retorna copia.
        Caso recursivo:
          1. Divide la lista en dos mitades iguales
          2. Ordena la mitad izquierda recursivamente
          3. Ordena la mitad derecha recursivamente
          4. Fusiona las dos mitades ordenadas

    Args:
        coleccion: Lista de elementos comparables.

    Returns:
        Nueva lista con los elementos ordenados de menor a mayor.

    Ejemplo:
        >>> mezcla_directa([38, 27, 43, 3, 9, 82, 10])
        [3, 9, 10, 27, 38, 43, 82]
    """
    # Copia para no modificar la lista original
    arr = list(coleccion)

    # Caso base: 0 o 1 elemento → ya está ordenado
    if len(arr) <= 1:
        return arr

    # Paso 1: Dividir en dos mitades
    medio = len(arr) // 2
    mitad_izq = arr[:medio]   # Mitad izquierda
    mitad_der = arr[medio:]   # Mitad derecha

    # Paso 2 y 3: Ordenar recursivamente cada mitad
    izq_ordenada = mezcla_directa(mitad_izq)
    der_ordenada = mezcla_directa(mitad_der)

    # Paso 4: Fusionar las dos mitades ya ordenadas
    return _fusionar_dos_listas(izq_ordenada, der_ordenada)


# ══════════════════════════════════════════════════════════════════════════════
# 3. MEZCLA EQUILIBRADA  (Balanced Merge Sort)
# ══════════════════════════════════════════════════════════════════════════════
#
#  IDEA PRINCIPAL:
#    Versión ITERATIVA (bottom-up / ascendente) del Merge Sort.
#    En vez de dividir recursivamente de arriba hacia abajo,
#    construye la solución de abajo hacia arriba:
#
#    Nivel 0: Cada elemento es un "run" (bloque) de tamaño 1
#      [[42], [15], [7], [99], [23], [8]]
#
#    Nivel 1: Fusiona pares de runs → runs de tamaño 2
#      [[15, 42], [7, 99], [8, 23]]
#
#    Nivel 2: Fusiona pares de runs → runs de tamaño 4
#      [[7, 15, 42, 99], [8, 23]]
#
#    Nivel 3: Fusiona el último par → run de tamaño n
#      [[7, 8, 15, 23, 42, 99]]
#
#  EN ORDENAMIENTO EXTERNO:
#    Cada "run" representa un bloque de datos que cabe en memoria.
#    En cada pasada, los bloques ordenados se fusionan de a pares
#    generando bloques cada vez más grandes, hasta tener uno solo.
#    Esto se llama "Polyphase Merge" en sistemas de archivos reales.
#
#  DIFERENCIA CON MEZCLA DIRECTA:
#    - Mezcla Directa:     recursiva (top-down), divide primero
#    - Mezcla Equilibrada: iterativa (bottom-up), fusiona primero
#    Ambas tienen la misma complejidad, pero la equilibrada evita
#    el overhead de la recursión y es más natural para archivos.
#
#  COMPLEJIDAD TEMPORAL: O(n log n) — siempre
#  COMPLEJIDAD ESPACIAL: O(n) — para las listas de runs temporales
#
#  VENTAJAS:
#    ✔ O(n log n) GARANTIZADO
#    ✔ Sin recursión → sin riesgo de stack overflow
#    ✔ Estable
#    ✔ Modelo natural para ordenamiento externo en disco
#    ✔ Fácil de distribuir en múltiples discos/nodos
#
#  DESVENTAJAS:
#    ✘ Requiere O(n) de memoria extra para los runs
#    ✘ Código más difícil de entender que la versión recursiva
# ──────────────────────────────────────────────────────────────────────────────

def mezcla_equilibrada(coleccion: list) -> list:
    """
    Ordena una lista usando Mezcla Equilibrada (Merge Sort iterativo bottom-up).

    Estrategia:
        1. Cada elemento comienza como un run (lista de 1 elemento)
        2. En cada pasada, fusiona runs de a pares:
             runs[0]+runs[1], runs[2]+runs[3], ...
           Si hay número impar de runs, el último pasa tal cual.
        3. Repite hasta que quede solo 1 run (la lista completa ordenada)

    Número de pasadas: ceil(log₂(n)) → O(log n) pasadas de O(n) cada una.

    Args:
        coleccion: Lista de elementos comparables.

    Returns:
        Nueva lista con los elementos ordenados de menor a mayor.

    Ejemplo:
        >>> mezcla_equilibrada([42, 15, 7, 99, 23, 8])
        [7, 8, 15, 23, 42, 99]
    """
    # Copia para no modificar la lista original
    arr = list(coleccion)

    if len(arr) <= 1:
        return arr  # Caso trivial

    # Paso 1: Inicializar — cada elemento es un run individual
    # Ejemplo: [42, 15, 7] → [[42], [15], [7]]
    runs: list[list] = [[elemento] for elemento in arr]

    # Paso 2: Fusionar pares de runs hasta que quede solo 1
    while len(runs) > 1:
        nuevos_runs = []  # Lista de runs resultantes de esta pasada

        # Procesar de a pares: (runs[0], runs[1]), (runs[2], runs[3]), ...
        for i in range(0, len(runs), 2):
            if i + 1 < len(runs):
                # Hay un par: fusionar runs[i] con runs[i+1]
                run_fusionado = _fusionar_dos_listas(runs[i], runs[i + 1])
                nuevos_runs.append(run_fusionado)
            else:
                # Número impar de runs: el último pasa sin fusionar
                nuevos_runs.append(runs[i])

        # Los nuevos runs reemplazan a los anteriores
        runs = nuevos_runs

    # Al terminar, runs tiene exactamente 1 elemento: la lista completa ordenada
    return runs[0]


# ══════════════════════════════════════════════════════════════════════════════
# TABLA RESUMEN DE COMPLEJIDADES
# ══════════════════════════════════════════════════════════════════════════════
#
#  Algoritmo           │ Mejor      │ Promedio   │ Peor       │ Espacio │ Estable
#  ────────────────────┼────────────┼────────────┼────────────┼─────────┼────────
#  Intercalación       │ O(n)  (*)  │ O(n log n) │ O(n log n) │ O(n)    │  Sí
#  Mezcla Directa      │ O(n log n) │ O(n log n) │ O(n log n) │ O(n)    │  Sí
#  Mezcla Equilibrada  │ O(n log n) │ O(n log n) │ O(n log n) │ O(n)    │  Sí
#
#  (*) La intercalación PURA de dos listas ya ordenadas es O(n).
#      Aquí incluye el sorted() de las mitades, por eso O(n log n) en promedio.
#
# ══════════════════════════════════════════════════════════════════════════════
#
#  COMPARACIÓN CONCEPTUAL:
#
#  Mezcla Directa (recursiva)    │  Mezcla Equilibrada (iterativa)
#  ─────────────────────────────────────────────────────────────────
#  Divide primero (top-down)     │  Fusiona primero (bottom-up)
#  Usa la pila de llamadas       │  No usa recursión
#  Más intuitiva de entender     │  Más natural para archivos/disco
#  Riesgo de stack overflow      │  Sin riesgo de stack overflow
#  Idéntica complejidad O(n logn)│  Idéntica complejidad O(n log n)
#
# ══════════════════════════════════════════════════════════════════════════════
