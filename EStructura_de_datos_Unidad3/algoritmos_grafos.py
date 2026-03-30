"""
==============================================================
  ALGORITMOS DE GRAFOS EN PYTHON
  Dijkstra | Floyd | Warshall | Kruskal
==============================================================
  Descripción: Implementación educativa de 4 algoritmos
               clásicos de teoría de grafos.
  Autor      : Generado con Claude (Anthropic)
  Uso        : python algoritmos_grafos.py
==============================================================
"""

import math   # para usar math.inf como "infinito"

# ══════════════════════════════════════════════════════════
#  SECCIÓN 1 – ALGORITMO DE DIJKSTRA
#  Encuentra la ruta MÁS CORTA desde un nodo origen
#  hacia todos los demás nodos del grafo.
# ══════════════════════════════════════════════════════════

def dijkstra(grafo, inicio):
    """
    Parámetros:
        grafo  : diccionario { nodo: [(vecino, peso), ...] }
        inicio : nodo desde el que calculamos las distancias
    Retorna:
        distancias : diccionario { nodo: distancia_minima }
        previos    : diccionario { nodo: nodo_anterior } (para reconstruir rutas)
    """

    # Paso 1: inicializar todas las distancias como infinito
    distancias = {nodo: math.inf for nodo in grafo}
    distancias[inicio] = 0          # la distancia al propio inicio es 0

    previos   = {nodo: None for nodo in grafo}   # para reconstruir la ruta
    visitados = set()                             # nodos ya procesados

    # Paso 2: repetir hasta haber procesado todos los nodos
    while len(visitados) < len(grafo):

        # Elegir el nodo NO visitado con la distancia más pequeña
        nodo_actual = None
        for nodo in grafo:
            if nodo not in visitados:
                if nodo_actual is None or distancias[nodo] < distancias[nodo_actual]:
                    nodo_actual = nodo

        if nodo_actual is None or distancias[nodo_actual] == math.inf:
            break   # no hay más nodos alcanzables

        visitados.add(nodo_actual)

        # Paso 3: actualizar distancias a los vecinos
        for vecino, peso in grafo[nodo_actual]:
            nueva_distancia = distancias[nodo_actual] + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                previos[vecino]    = nodo_actual   # guardamos por dónde llegamos

    return distancias, previos


def reconstruir_ruta(previos, destino):
    """Reconstruye la ruta desde el inicio hasta 'destino' usando el dict previos."""
    ruta = []
    nodo = destino
    while nodo is not None:
        ruta.append(nodo)
        nodo = previos[nodo]
    ruta.reverse()
    return ruta


def ejemplo_dijkstra():
    print("=" * 55)
    print("  ALGORITMO DE DIJKSTRA")
    print("=" * 55)

    # Grafo de ejemplo: ciudades con distancias en km
    #
    #      A --4-- B
    #      |       |  \
    #      2       5   1
    #      |       |    \
    #      C --1-- D --3-- E
    #
    grafo = {
        "A": [("B", 4), ("C", 2)],
        "B": [("A", 4), ("D", 5), ("E", 1)],
        "C": [("A", 2), ("D", 1)],
        "D": [("B", 5), ("C", 1), ("E", 3)],
        "E": [("B", 1), ("D", 3)],
    }

    inicio = "A"
    distancias, previos = dijkstra(grafo, inicio)

    print(f"\n  Nodo origen: {inicio}")
    print(f"  {'Destino':<10} {'Distancia':>10}   {'Ruta'}")
    print(f"  {'-'*45}")
    for nodo in sorted(grafo):
        if nodo == inicio:
            continue
        dist = distancias[nodo]
        ruta = reconstruir_ruta(previos, nodo)
        dist_str = str(dist) if dist != math.inf else "∞"
        print(f"  {nodo:<10} {dist_str:>10}   {' → '.join(ruta)}")

    print()


# ══════════════════════════════════════════════════════════
#  SECCIÓN 2 – ALGORITMO DE FLOYD-WARSHALL
#  Encuentra las rutas más cortas entre TODOS los pares
#  de nodos del grafo usando programación dinámica.
# ══════════════════════════════════════════════════════════

INF = math.inf   # abreviación cómoda para infinito

def floyd_warshall(nodos, aristas):
    """
    Parámetros:
        nodos  : lista de nodos  ['A', 'B', 'C', ...]
        aristas: lista de tuplas (origen, destino, peso)
    Retorna:
        dist : matriz de distancias mínimas entre todos los pares
    """
    n = len(nodos)
    idx = {nodo: i for i, nodo in enumerate(nodos)}   # mapa nodo → índice

    # Paso 1: inicializar la matriz con INF
    dist = [[INF] * n for _ in range(n)]

    # La distancia de cada nodo a sí mismo es 0
    for i in range(n):
        dist[i][i] = 0

    # Cargar las aristas conocidas
    for origen, destino, peso in aristas:
        i, j = idx[origen], idx[destino]
        dist[i][j] = peso
        dist[j][i] = peso   # grafo no dirigido

    # Paso 2: el corazón de Floyd – probar cada nodo como intermediario
    for k in range(n):            # k = nodo intermediario
        for i in range(n):        # i = nodo origen
            for j in range(n):    # j = nodo destino
                # ¿Es más corto ir de i → k → j que ir de i → j directo?
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist, nodos, idx


def ejemplo_floyd():
    print("=" * 55)
    print("  ALGORITMO DE FLOYD-WARSHALL")
    print("=" * 55)

    nodos = ["A", "B", "C", "D"]

    # Aristas del grafo (grafo no dirigido con pesos)
    aristas = [
        ("A", "B", 3),
        ("A", "C", 8),
        ("B", "C", 2),
        ("B", "D", 5),
        ("C", "D", 1),
    ]

    dist, nodos_lista, idx = floyd_warshall(nodos, aristas)
    n = len(nodos_lista)

    print(f"\n  Matriz de distancias mínimas entre todos los pares:\n")
    encabezado = "        " + "  ".join(f"{n:>5}" for n in nodos_lista)
    print(f"  {encabezado}")
    print(f"  {'  ' + '-' * (7 * n)}")

    for i, origen in enumerate(nodos_lista):
        fila = f"  {origen}  |  "
        for j in range(n):
            valor = dist[i][j]
            celda = f"{valor:>5}" if valor != INF else "  INF"
            fila += celda + "  "
        print(fila)

    print()


# ══════════════════════════════════════════════════════════
#  SECCIÓN 3 – ALGORITMO DE WARSHALL
#  Calcula la CERRADURA TRANSITIVA de un grafo:
#  determina si existe ALGÚN camino entre cada par de nodos
#  (no importa el costo, solo si hay conexión o no).
# ══════════════════════════════════════════════════════════

def warshall(nodos, aristas_dirigidas):
    """
    Parámetros:
        nodos           : lista de nodos
        aristas_dirigidas: lista de tuplas (origen, destino)  ← SIN peso
    Retorna:
        alcanzable : matriz booleana  alcanzable[i][j] = True si i puede llegar a j
    """
    n   = len(nodos)
    idx = {nodo: i for i, nodo in enumerate(nodos)}

    # Paso 1: inicializar la matriz de alcanzabilidad
    alcanzable = [[False] * n for _ in range(n)]

    # Un nodo siempre se alcanza a sí mismo
    for i in range(n):
        alcanzable[i][i] = True

    # Cargar las conexiones directas
    for origen, destino in aristas_dirigidas:
        i, j = idx[origen], idx[destino]
        alcanzable[i][j] = True

    # Paso 2: si i→k y k→j, entonces i→j (transitividad)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if alcanzable[i][k] and alcanzable[k][j]:
                    alcanzable[i][j] = True

    return alcanzable, nodos


def ejemplo_warshall():
    print("=" * 55)
    print("  ALGORITMO DE WARSHALL (Cerradura Transitiva)")
    print("=" * 55)

    nodos = ["A", "B", "C", "D"]

    # Grafo DIRIGIDO (sin pesos, solo conexiones)
    #   A → B → C → D
    #   A → C
    aristas = [
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("A", "C"),
    ]

    alcanzable, nodos_lista = warshall(nodos, aristas)
    n = len(nodos_lista)

    print(f"\n  Aristas directas: {aristas}")
    print(f"\n  Matriz de alcanzabilidad (True = existe camino):\n")

    encabezado = "        " + "  ".join(f"{nd:>6}" for nd in nodos_lista)
    print(f"  {encabezado}")
    print(f"  {'  ' + '-' * (9 * n)}")

    for i, origen in enumerate(nodos_lista):
        fila = f"  {origen}  |  "
        for j in range(n):
            celda = "  True" if alcanzable[i][j] else " False"
            fila += celda + "  "
        print(fila)

    print()
    print("  Interpretación:")
    for i, origen in enumerate(nodos_lista):
        for j, destino in enumerate(nodos_lista):
            if i != j and alcanzable[i][j]:
                print(f"    {origen} puede llegar a {destino}")

    print()


# ══════════════════════════════════════════════════════════
#  SECCIÓN 4 – ALGORITMO DE KRUSKAL
#  Encuentra el ÁRBOL DE EXPANSIÓN MÍNIMA (MST):
#  conecta todos los nodos con el menor costo total posible
#  sin formar ciclos.
# ══════════════════════════════════════════════════════════

# ── Estructura Union-Find (conjuntos disjuntos) ──
# Ayuda a saber si dos nodos ya están conectados (para evitar ciclos)

def encontrar_raiz(padre, nodo):
    """Encuentra la raíz del conjunto al que pertenece 'nodo'."""
    while padre[nodo] != nodo:
        padre[nodo] = padre[padre[nodo]]   # compresión de camino (optimización simple)
        nodo = padre[nodo]
    return nodo

def unir_conjuntos(padre, rango, a, b):
    """Une los conjuntos de a y b. Retorna False si ya estaban unidos (ciclo)."""
    raiz_a = encontrar_raiz(padre, a)
    raiz_b = encontrar_raiz(padre, b)

    if raiz_a == raiz_b:
        return False   # ya están en el mismo conjunto → formaría ciclo

    # Unir el árbol más pequeño bajo el más grande (por rango)
    if rango[raiz_a] < rango[raiz_b]:
        padre[raiz_a] = raiz_b
    elif rango[raiz_a] > rango[raiz_b]:
        padre[raiz_b] = raiz_a
    else:
        padre[raiz_b] = raiz_a
        rango[raiz_a] += 1

    return True


def kruskal(nodos, aristas):
    """
    Parámetros:
        nodos  : lista de nodos
        aristas: lista de tuplas (peso, origen, destino)
    Retorna:
        mst   : lista de aristas seleccionadas  [(peso, orig, dest), ...]
        costo : costo total del árbol mínimo
    """
    # Paso 1: ordenar aristas de menor a mayor peso
    aristas_ordenadas = sorted(aristas, key=lambda a: a[0])

    # Inicializar Union-Find: cada nodo es su propio conjunto
    padre = {nodo: nodo for nodo in nodos}
    rango  = {nodo: 0    for nodo in nodos}

    mst   = []    # aristas del árbol de expansión mínima
    costo = 0

    # Paso 2: recorrer aristas de menor a mayor
    for peso, origen, destino in aristas_ordenadas:
        # Agregar solo si no forma un ciclo
        if unir_conjuntos(padre, rango, origen, destino):
            mst.append((peso, origen, destino))
            costo += peso

            # Si ya tenemos n-1 aristas, el árbol está completo
            if len(mst) == len(nodos) - 1:
                break

    return mst, costo


def ejemplo_kruskal():
    print("=" * 55)
    print("  ALGORITMO DE KRUSKAL (Árbol de Expansión Mínima)")
    print("=" * 55)

    nodos = ["A", "B", "C", "D", "E"]

    # Aristas: (peso, origen, destino)
    aristas = [
        (1, "A", "B"),
        (3, "A", "C"),
        (4, "B", "C"),
        (2, "B", "D"),
        (5, "C", "D"),
        (6, "C", "E"),
        (3, "D", "E"),
    ]

    mst, costo_total = kruskal(nodos, aristas)

    print(f"\n  Todas las aristas disponibles (ordenadas por peso):")
    for peso, orig, dest in sorted(aristas):
        print(f"    {orig} — {dest}  (peso: {peso})")

    print(f"\n  Aristas seleccionadas para el árbol mínimo:")
    for peso, orig, dest in mst:
        print(f"    ✓  {orig} — {dest}  (peso: {peso})")

    print(f"\n  Costo total del árbol de expansión mínima: {costo_total}")
    print()


# ══════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA – ejecutar todos los ejemplos
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "═" * 55)
    print("  ALGORITMOS DE GRAFOS EN PYTHON")
    print("  Dijkstra | Floyd | Warshall | Kruskal")
    print("═" * 55 + "\n")

    ejemplo_dijkstra()
    ejemplo_floyd()
    ejemplo_warshall()
    ejemplo_kruskal()

    print("═" * 55)
    print("  Fin de la ejecución.")
    print("═" * 55 + "\n")
