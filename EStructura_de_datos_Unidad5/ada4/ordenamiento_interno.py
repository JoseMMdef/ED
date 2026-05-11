"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              LIBRERÍA DE ORDENAMIENTO INTERNO                                ║
║              Archivo: ordenamiento_interno.py                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Algoritmos incluidos:                                                       ║
║    1. Bubble Sort    — O(n²)       — Intercambia elementos adyacentes        ║
║    2. Insertion Sort — O(n²)/O(n)  — Inserta elemento en posición correcta  ║
║    3. Selection Sort — O(n²)       — Busca el mínimo y lo coloca al frente   ║
║    4. Shell Sort     — O(n log²n)  — Insertion Sort con saltos (gaps)        ║
║    5. Quick Sort     — O(n log n)  — Divide y vencerás con pivote            ║
║    6. Heap Sort      — O(n log n)  — Ordena usando montículo máximo          ║
║    7. Radix Sort     — O(n·k)      — Ordena dígito a dígito sin comparar     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  IMPORTANTE: Todos los algoritmos retornan una NUEVA lista ordenada.        ║
║              La lista original NO se modifica.                               ║
║  ORIGEN:     Basado en ADA1 (Bubble, Insertion, Selection)                  ║
║              y ADA2 (Shell, Quick, Heap, Radix)                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations
from random import randrange


# ══════════════════════════════════════════════════════════════════════════════
# 1. BUBBLE SORT  (Ordenamiento Burbuja)
# ══════════════════════════════════════════════════════════════════════════════
#
#  IDEA PRINCIPAL:
#    Recorre la lista comparando pares adyacentes (arr[j] y arr[j+1]).
#    Si están en el orden incorrecto, los intercambia.
#    El elemento más grande "burbujea" hacia el final en cada pasada.
#    La zona ordenada crece desde el FINAL hacia el inicio.
#
#  COMPLEJIDAD TEMPORAL:
#    - Mejor caso  : O(n)   → lista ya ordenada (con la optimización del flag)
#    - Caso promedio: O(n²)
#    - Peor caso   : O(n²)  → lista ordenada al revés
#
#  COMPLEJIDAD ESPACIAL: O(1) — in-place (no usa memoria extra significativa)
#
#  VENTAJAS:
#    ✔ Fácil de entender e implementar
#    ✔ Detecta lista ya ordenada en O(n) gracias al flag
#    ✔ Estable: no cambia el orden relativo de elementos iguales
#
#  DESVENTAJAS:
#    ✘ Muy lento para listas grandes
#    ✘ Muchos intercambios innecesarios
#    ✘ Raramente usado en producción
# ──────────────────────────────────────────────────────────────────────────────

def bubble_sort(coleccion: list) -> list:
    """
    Ordena una lista usando Bubble Sort.

    Estrategia:
        En cada pasada 'i', compara pares vecinos arr[j] y arr[j+1].
        Si arr[j] > arr[j+1], los intercambia.
        Después de cada pasada, el mayor elemento queda al final.
        El flag 'intercambiado' permite salir temprano si ya está ordenada.

    Args:
        coleccion: Lista de elementos comparables (números, strings, etc.)

    Returns:
        Nueva lista con los elementos ordenados de menor a mayor.

    Ejemplo:
        >>> bubble_sort([5, 3, 1, 4, 2])
        [1, 2, 3, 4, 5]
    """
    # Trabajamos sobre una copia para NO modificar la lista original
    arr = list(coleccion)
    n = len(arr)

    # Pasada exterior: cada iteración coloca el máximo restante al final
    for i in range(n - 1):
        intercambiado = False  # Optimización: si no hay intercambios, ya está ordenada

        # Pasada interior: compara hasta la zona ya ordenada (n - i - 1)
        for j in range(0, n - i - 1):

            # Si el elemento izquierdo es mayor, lo "burbujeamos" hacia la derecha
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # Intercambio en una línea (Python)
                intercambiado = True

        # Si no hubo ningún intercambio en esta pasada, la lista ya está ordenada
        if not intercambiado:
            break  # Salida anticipada → mejor caso O(n)

    return arr


# ══════════════════════════════════════════════════════════════════════════════
# 2. INSERTION SORT  (Ordenamiento por Inserción)
# ══════════════════════════════════════════════════════════════════════════════
#
#  IDEA PRINCIPAL:
#    Simula cómo ordenamos cartas en la mano:
#    Toma un elemento (la "clave") y lo inserta en la posición correcta
#    dentro de la parte ya ordenada (que crece desde el INICIO).
#    Para insertar, desplaza hacia la derecha los elementos mayores.
#
#  COMPLEJIDAD TEMPORAL:
#    - Mejor caso   : O(n)   → lista ya ordenada
#    - Caso promedio: O(n²)
#    - Peor caso    : O(n²)  → lista ordenada al revés
#
#  COMPLEJIDAD ESPACIAL: O(1) — in-place
#
#  VENTAJAS:
#    ✔ Muy eficiente para listas pequeñas o casi ordenadas
#    ✔ Estable
#    ✔ Adaptativo: detecta el orden existente
#    ✔ Útil como componente de otros algoritmos (TimSort, Shell Sort)
#
#  DESVENTAJAS:
#    ✘ O(n²) en el peor caso
#    ✘ Ineficiente para listas grandes y desordenadas
# ──────────────────────────────────────────────────────────────────────────────

def insertion_sort(coleccion: list) -> list:
    """
    Ordena una lista usando Insertion Sort.

    Estrategia:
        Para cada posición i (desde 1 hasta n-1):
          1. Guarda arr[i] como 'clave'
          2. Retrocede con j desde i-1 hacia 0
          3. Mientras arr[j] > clave, desplaza arr[j] a arr[j+1]
          4. Inserta la clave en la posición vacía encontrada

    Args:
        coleccion: Lista de elementos comparables.

    Returns:
        Nueva lista con los elementos ordenados de menor a mayor.

    Ejemplo:
        >>> insertion_sort([5, 3, 1, 4, 2])
        [1, 2, 3, 4, 5]
    """
    # Copia para no modificar la lista original
    arr = list(coleccion)
    n = len(arr)

    # Empezamos en el índice 1: arr[0] ya está "ordenado" por sí solo
    for i in range(1, n):
        clave = arr[i]  # Elemento a insertar en la parte izquierda ya ordenada
        j = i - 1       # Puntero que retrocede por la parte ordenada

        # Desplazar hacia la derecha todos los elementos mayores que la clave
        while j >= 0 and arr[j] > clave:
            arr[j + 1] = arr[j]  # Mueve arr[j] una posición a la derecha
            j -= 1               # Retrocede el puntero

        # Coloca la clave en el hueco generado
        arr[j + 1] = clave

    return arr


# ══════════════════════════════════════════════════════════════════════════════
# 3. SELECTION SORT  (Ordenamiento por Selección)
# ══════════════════════════════════════════════════════════════════════════════
#
#  IDEA PRINCIPAL:
#    En cada pasada busca el MÍNIMO elemento de la parte no ordenada
#    y lo intercambia con la primera posición de esa parte.
#    La zona ordenada crece desde el INICIO igual que Insertion Sort,
#    pero la diferencia es que aquí se busca el mínimo en vez de insertar.
#
#  COMPLEJIDAD TEMPORAL:
#    - Mejor caso   : O(n²)  ← siempre recorre todo aunque esté ordenada
#    - Caso promedio: O(n²)
#    - Peor caso    : O(n²)
#
#  COMPLEJIDAD ESPACIAL: O(1) — in-place
#
#  VENTAJAS:
#    ✔ Mínimo número de intercambios: exactamente n-1 en total
#    ✔ Útil cuando el costo de escribir en memoria es muy alto
#    ✔ Fácil de implementar
#
#  DESVENTAJAS:
#    ✘ Siempre O(n²) sin importar el estado de la lista
#    ✘ Inestable: puede cambiar el orden relativo de iguales
#    ✘ Ineficiente para listas grandes
# ──────────────────────────────────────────────────────────────────────────────

def selection_sort(coleccion: list) -> list:
    """
    Ordena una lista usando Selection Sort.

    Estrategia:
        Para cada posición i (desde 0 hasta n-2):
          1. Asume que arr[i] es el mínimo
          2. Recorre arr[i+1 .. n-1] buscando un elemento menor
          3. Si encuentra uno, actualiza el índice del mínimo
          4. Al terminar la búsqueda, intercambia arr[i] con el mínimo encontrado

    Args:
        coleccion: Lista de elementos comparables.

    Returns:
        Nueva lista con los elementos ordenados de menor a mayor.

    Ejemplo:
        >>> selection_sort([5, 3, 1, 4, 2])
        [1, 2, 3, 4, 5]
    """
    # Copia para no modificar la lista original
    arr = list(coleccion)
    n = len(arr)

    for i in range(n - 1):
        # Suponemos que el mínimo de la parte no ordenada está en la posición i
        idx_min = i

        # Buscamos el verdadero mínimo en la parte no ordenada arr[i+1 .. n-1]
        for j in range(i + 1, n):
            if arr[j] < arr[idx_min]:
                idx_min = j  # Encontramos un nuevo mínimo

        # Solo intercambiamos si el mínimo no era ya arr[i]
        if idx_min != i:
            arr[i], arr[idx_min] = arr[idx_min], arr[i]

    return arr


# ══════════════════════════════════════════════════════════════════════════════
# 4. SHELL SORT
# ══════════════════════════════════════════════════════════════════════════════
#
#  IDEA PRINCIPAL:
#    Mejora de Insertion Sort. En vez de comparar solo elementos adyacentes,
#    compara elementos separados por un "gap" (intervalo).
#    El gap va disminuyendo en cada pasada hasta llegar a 1,
#    momento en que se convierte en Insertion Sort normal, pero con
#    la lista casi ordenada → muy pocos desplazamientos.
#
#  SECUENCIA DE GAPS: [701, 301, 132, 57, 23, 10, 4, 1] (Ciura, 2001)
#    Esta secuencia está demostrada empíricamente como una de las mejores.
#
#  COMPLEJIDAD TEMPORAL:
#    - Depende de la secuencia de gaps
#    - Con gaps de Ciura: O(n^(4/3)) aproximadamente en promedio
#    - Peor caso conocido: O(n log² n)
#
#  COMPLEJIDAD ESPACIAL: O(1) — in-place
#
#  VENTAJAS:
#    ✔ Mucho más rápido que Insertion Sort para listas grandes
#    ✔ No necesita memoria extra
#    ✔ Simple de implementar
#
#  DESVENTAJAS:
#    ✘ No es estable
#    ✘ La complejidad exacta depende de la secuencia de gaps elegida
#    ✘ Superado por Quick Sort y Merge Sort en la práctica
# ──────────────────────────────────────────────────────────────────────────────

def shell_sort(coleccion: list) -> list:
    """
    Ordena una lista usando Shell Sort con la secuencia de gaps de Ciura.

    Estrategia:
        Para cada gap en [701, 301, 132, 57, 23, 10, 4, 1]:
          Aplica una versión de Insertion Sort donde los elementos
          se comparan con los que están a 'gap' posiciones de distancia.
        Al llegar a gap=1, es Insertion Sort puro pero con lista casi ordenada.

    Args:
        coleccion: Lista de enteros a ordenar.

    Returns:
        Nueva lista con los elementos ordenados de menor a mayor.

    Ejemplo:
        >>> shell_sort([5, 3, 1, 4, 2])
        [1, 2, 3, 4, 5]
    """
    # Copia para no modificar la lista original
    arr = list(coleccion)

    # Secuencia de gaps de Marcin Ciura (2001) — empíricamente óptima
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]

    for gap in gaps:
        # Insertion Sort con salto 'gap' en vez de salto 1
        for i in range(gap, len(arr)):
            valor_insertar = arr[i]
            j = i

            # Desplazamos elementos a 'gap' posiciones hacia la derecha
            while j >= gap and arr[j - gap] > valor_insertar:
                arr[j] = arr[j - gap]
                j -= gap

            # Insertamos el valor en su posición correcta
            if j != i:
                arr[j] = valor_insertar

    return arr


# ══════════════════════════════════════════════════════════════════════════════
# 5. QUICK SORT  (Ordenamiento Rápido)
# ══════════════════════════════════════════════════════════════════════════════
#
#  IDEA PRINCIPAL:
#    Algoritmo "Divide y Vencerás":
#      1. Elige un elemento como PIVOTE
#      2. PARTICIONA: separa en menores/iguales y mayores al pivote
#      3. Aplica Quick Sort recursivamente a cada partición
#      4. Combina: [menores_ordenados] + [pivote] + [mayores_ordenados]
#
#    El pivote se elige ALEATORIAMENTE para evitar el peor caso con
#    listas ya ordenadas o con muchos elementos iguales.
#
#  COMPLEJIDAD TEMPORAL:
#    - Mejor caso   : O(n log n) → pivote divide siempre a la mitad
#    - Caso promedio: O(n log n)
#    - Peor caso    : O(n²)      → pivote siempre es el mínimo o máximo
#
#  COMPLEJIDAD ESPACIAL: O(log n) — pila de recursión
#
#  VENTAJAS:
#    ✔ En la práctica el más rápido para listas grandes
#    ✔ Buen uso de caché del procesador
#    ✔ El pivote aleatorio casi elimina el peor caso
#
#  DESVENTAJAS:
#    ✘ No es estable
#    ✘ O(n²) en peor caso (aunque raro con pivote aleatorio)
#    ✘ No es óptimo para listas muy pequeñas
# ──────────────────────────────────────────────────────────────────────────────

def quick_sort(coleccion: list) -> list:
    """
    Ordena una lista usando Quick Sort con pivote aleatorio.

    Estrategia:
        Caso base: lista de 0 o 1 elemento → ya está ordenada.
        Caso recursivo:
          1. Elige pivote aleatorio y lo extrae de la lista
          2. Separa el resto en 'menores' (≤ pivote) y 'mayores' (> pivote)
          3. Retorna quick_sort(menores) + [pivote] + quick_sort(mayores)

    Args:
        coleccion: Lista de elementos comparables.

    Returns:
        Nueva lista con los elementos ordenados de menor a mayor.

    Ejemplo:
        >>> quick_sort([5, 3, 1, 4, 2])
        [1, 2, 3, 4, 5]
    """
    # Copia para no modificar la lista original (solo en la llamada inicial)
    arr = list(coleccion)

    # Caso base: 0 o 1 elementos → ya está ordenado
    if len(arr) < 2:
        return arr

    # Elegir índice de pivote ALEATORIO → evita O(n²) con listas ya ordenadas
    indice_pivote = randrange(len(arr))
    pivote = arr.pop(indice_pivote)  # Extrae el pivote de la lista

    # Particionar: elementos menores o iguales vs. elementos mayores
    menores = [x for x in arr if x <= pivote]
    mayores = [x for x in arr if x > pivote]

    # Construir resultado: recursión en cada parte + pivote en el centro
    return [*quick_sort(menores), pivote, *quick_sort(mayores)]


# ══════════════════════════════════════════════════════════════════════════════
# 6. HEAP SORT  (Ordenamiento por Montículo)
# ══════════════════════════════════════════════════════════════════════════════
#
#  IDEA PRINCIPAL:
#    Usa una estructura de datos llamada MAX-HEAP (montículo máximo):
#    un árbol binario donde cada padre es mayor que sus hijos.
#    Representado como array: el padre de arr[i] está en arr[(i-1)//2],
#    hijos en arr[2i+1] y arr[2i+2].
#
#    FASE 1 — Construir el heap: convierte el array en un max-heap.
#    FASE 2 — Extraer: el mayor (raíz) se pone al final, se reduce
#             el heap y se repara la propiedad. Repite n-1 veces.
#
#  COMPLEJIDAD TEMPORAL:
#    - Mejor caso   : O(n log n)  ← siempre, sin importar la entrada
#    - Caso promedio: O(n log n)
#    - Peor caso    : O(n log n)  ← garantizado
#
#  COMPLEJIDAD ESPACIAL: O(1) — in-place (no necesita memoria extra)
#
#  VENTAJAS:
#    ✔ O(n log n) GARANTIZADO en todos los casos
#    ✔ In-place: no necesita memoria adicional
#    ✔ Útil cuando se necesita garantía de rendimiento
#
#  DESVENTAJAS:
#    ✘ No es estable
#    ✘ En la práctica más lento que Quick Sort (mal uso de caché)
#    ✘ Código más complejo de entender
# ──────────────────────────────────────────────────────────────────────────────

def _heapify(arr: list, indice: int, tam_heap: int) -> None:
    """
    Función auxiliar interna. Mantiene la propiedad de MAX-HEAP
    en el subárbol cuya raíz está en 'indice'.

    Si algún hijo es mayor que la raíz, los intercambia y
    llama recursivamente hacia abajo (sift-down).

    Args:
        arr:      Lista que representa el heap.
        indice:   Índice de la raíz del subárbol a ajustar.
        tam_heap: Tamaño activo del heap (el resto ya está ordenado).
    """
    mayor    = indice          # Asumimos que la raíz es el mayor
    hijo_izq = 2 * indice + 1  # Fórmula: hijo izquierdo en árbol binario
    hijo_der = 2 * indice + 2  # Fórmula: hijo derecho en árbol binario

    # ¿El hijo izquierdo existe Y es mayor que la raíz?
    if hijo_izq < tam_heap and arr[hijo_izq] > arr[mayor]:
        mayor = hijo_izq

    # ¿El hijo derecho existe Y es mayor que el mayor hasta ahora?
    if hijo_der < tam_heap and arr[hijo_der] > arr[mayor]:
        mayor = hijo_der

    # Si la raíz no era el mayor, intercambiar y continuar hacia abajo
    if mayor != indice:
        arr[mayor], arr[indice] = arr[indice], arr[mayor]
        _heapify(arr, mayor, tam_heap)  # Recursión: ajusta el subárbol afectado


def heap_sort(coleccion: list) -> list:
    """
    Ordena una lista usando Heap Sort.

    Estrategia:
        Fase 1 — Construir max-heap:
          Aplica _heapify desde el último nodo interno hasta la raíz.
          Resultado: arr[0] es siempre el elemento más grande.

        Fase 2 — Ordenar extrayendo el máximo:
          Para i desde n-1 hasta 1:
            - Intercambia arr[0] (máximo) con arr[i] (último del heap)
            - Reduce el tamaño del heap en 1 (arr[i] ya está en su lugar)
            - Repara el heap con _heapify desde la raíz

    Args:
        coleccion: Lista de enteros a ordenar.

    Returns:
        Nueva lista con los elementos ordenados de menor a mayor.

    Ejemplo:
        >>> heap_sort([5, 3, 1, 4, 2])
        [1, 2, 3, 4, 5]
    """
    # Copia para no modificar la lista original
    arr = list(coleccion)
    n = len(arr)

    # ── FASE 1: Construir el max-heap ──
    # El último nodo interno está en n//2 - 1
    # Aplicamos heapify de abajo hacia arriba
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, i, n)

    # ── FASE 2: Extraer elementos del heap en orden ──
    for i in range(n - 1, 0, -1):
        # El mayor elemento (raíz = arr[0]) va a su posición final
        arr[0], arr[i] = arr[i], arr[0]
        # Reparar el heap ignorando los elementos ya ordenados (tam = i)
        _heapify(arr, 0, i)

    return arr


# ══════════════════════════════════════════════════════════════════════════════
# 7. RADIX SORT  (Ordenamiento por Base/Dígitos)
# ══════════════════════════════════════════════════════════════════════════════
#
#  IDEA PRINCIPAL:
#    A diferencia de todos los anteriores, NO compara elementos entre sí.
#    En cambio, ordena dígito a dígito de MENOS significativo a MÁS:
#      Pasada 1: ordena por unidades (dígito 1)
#      Pasada 2: ordena por decenas  (dígito 10)
#      Pasada 3: ordena por centenas (dígito 100)
#      ... y así hasta el dígito más alto del número máximo.
#    En cada pasada, distribuye en 10 "cubetas" (0-9) y las reagrupa.
#
#  ¡SOLO FUNCIONA CON ENTEROS NO NEGATIVOS!
#
#  COMPLEJIDAD TEMPORAL: O(n·k)
#    donde n = cantidad de elementos, k = número de dígitos del máximo
#    Para números pequeños (k constante) → O(n) lineal
#
#  COMPLEJIDAD ESPACIAL: O(n + b) donde b = base (10 para decimal)
#
#  VENTAJAS:
#    ✔ Lineal O(n·k) → puede superar a Quick Sort para muchos enteros
#    ✔ Estable
#    ✔ No hace comparaciones directas
#
#  DESVENTAJAS:
#    ✘ Solo funciona con enteros no negativos
#    ✘ Usa memoria extra para las cubetas
#    ✘ Para números con muchos dígitos (k grande) puede ser lento
# ──────────────────────────────────────────────────────────────────────────────

RADIX_BASE = 10  # Base decimal: dígitos del 0 al 9

def radix_sort(coleccion: list) -> list:
    """
    Ordena una lista de enteros no negativos usando Radix Sort LSD.
    LSD = Least Significant Digit first (del dígito menos al más significativo).

    PRECONDICIÓN: Todos los elementos deben ser enteros >= 0.
                  Si hay negativos, se lanza ValueError.

    Estrategia:
        Para cada posición decimal (1, 10, 100, 1000, ...):
          1. Crear 10 cubetas vacías (una por cada dígito 0-9)
          2. Calcular el dígito de cada número en esa posición
          3. Colocar cada número en su cubeta correspondiente
          4. Recolectar todas las cubetas en orden → nueva lista
        Repetir hasta procesar el dígito más alto del número máximo.

    Args:
        coleccion: Lista de enteros no negativos.

    Returns:
        Nueva lista con los elementos ordenados de menor a mayor.

    Raises:
        ValueError: Si algún elemento es negativo.

    Ejemplo:
        >>> radix_sort([170, 45, 75, 90, 802, 24, 2, 66])
        [2, 24, 45, 66, 75, 90, 170, 802]
    """
    # Copia para no modificar la lista original
    arr = list(coleccion)

    # Validación: Radix Sort solo funciona con enteros no negativos
    if any(n < 0 for n in arr):
        raise ValueError(
            "Radix Sort solo admite enteros no negativos (>= 0). "
            "Usa otro algoritmo para números negativos."
        )

    if not arr:
        return arr  # Lista vacía: nada que ordenar

    posicion  = 1           # Empezamos por el dígito de las UNIDADES
    valor_max = max(arr)    # Determina cuántas pasadas necesitamos

    while posicion <= valor_max:
        # Crear 10 cubetas vacías (dígitos del 0 al 9)
        cubetas: list[list[int]] = [[] for _ in range(RADIX_BASE)]

        # Distribuir cada número en su cubeta según el dígito actual
        for numero in arr:
            digito = int((numero / posicion) % RADIX_BASE)
            cubetas[digito].append(numero)

        # Recolectar: vaciar cubetas en orden y refill la lista
        idx = 0
        for cubeta in cubetas:
            for numero in cubeta:
                arr[idx] = numero
                idx += 1

        # Siguiente posición decimal (unidades → decenas → centenas → ...)
        posicion *= RADIX_BASE

    return arr


# ══════════════════════════════════════════════════════════════════════════════
# TABLA RESUMEN DE COMPLEJIDADES
# ══════════════════════════════════════════════════════════════════════════════
#
#  Algoritmo      │ Mejor     │ Promedio  │ Peor      │ Espacio │ Estable
#  ───────────────┼───────────┼───────────┼───────────┼─────────┼────────
#  Bubble Sort    │ O(n)      │ O(n²)     │ O(n²)     │ O(1)    │  Sí
#  Insertion Sort │ O(n)      │ O(n²)     │ O(n²)     │ O(1)    │  Sí
#  Selection Sort │ O(n²)     │ O(n²)     │ O(n²)     │ O(1)    │  No
#  Shell Sort     │ O(n log n)│ O(n log²n)│ O(n log²n)│ O(1)    │  No
#  Quick Sort     │ O(n log n)│ O(n log n)│ O(n²)     │ O(log n)│  No
#  Heap Sort      │ O(n log n)│ O(n log n)│ O(n log n)│ O(1)    │  No
#  Radix Sort     │ O(n·k)    │ O(n·k)    │ O(n·k)    │ O(n+b)  │  Sí
#
# ══════════════════════════════════════════════════════════════════════════════
