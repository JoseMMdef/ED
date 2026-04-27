"""
╔══════════════════════════════════════════════════════════╗
║         PROGRAMA DE ALGORITMOS DE ORDENAMIENTO           ║
║  ShellSort | QuickSort | HeapSort | Radix Sort           ║
╚══════════════════════════════════════════════════════════╝

Implementación pura en Python de cuatro algoritmos clásicos
de ordenamiento, con menú interactivo para el usuario.
"""

from __future__ import annotations
from random import randrange


# ─────────────────────────────────────────────────────────
#  1. SHELL SORT
#  Mejora de Insertion Sort que ordena elementos distantes
#  primero, reduciendo el trabajo total de comparaciones.
#  Complejidad: O(n log² n) promedio
# ─────────────────────────────────────────────────────────

def shell_sort(coleccion: list[int]) -> list[int]:
    """
    Ordena una lista usando el algoritmo Shell Sort.

    Usa la secuencia de gaps de Marcin Ciura, que está
    demostrada empíricamente como una de las mejores.

    Args:
        coleccion: Lista de enteros a ordenar.

    Returns:
        La misma lista ordenada de menor a mayor.

    Ejemplo:
        >>> shell_sort([5, 3, 1, 4, 2])
        [1, 2, 3, 4, 5]
    """
    # Secuencia de gaps de Marcin Ciura (intervalos decrecientes)
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]

    for gap in gaps:
        # Para cada gap, aplicamos insertion sort con ese intervalo
        for i in range(gap, len(coleccion)):
            valor_insertar = coleccion[i]
            j = i

            # Desplazamos elementos que estén a 'gap' posiciones
            # y sean mayores que el valor a insertar
            while j >= gap and coleccion[j - gap] > valor_insertar:
                coleccion[j] = coleccion[j - gap]
                j -= gap

            # Insertamos el valor en su posición correcta
            if j != i:
                coleccion[j] = valor_insertar

    return coleccion


# ─────────────────────────────────────────────────────────
#  2. QUICK SORT
#  Algoritmo "divide y vencerás": elige un pivote y divide
#  la lista en menores y mayores, luego ordena recursivamente.
#  Complejidad: O(n log n) promedio, O(n²) peor caso
# ─────────────────────────────────────────────────────────

def quick_sort(coleccion: list) -> list:
    """
    Ordena una lista usando el algoritmo Quick Sort.

    Selecciona un pivote aleatorio para evitar el peor caso
    con listas ya ordenadas.

    Args:
        coleccion: Lista de elementos comparables.

    Returns:
        Nueva lista ordenada de menor a mayor.

    Ejemplo:
        >>> quick_sort([5, 3, 1, 4, 2])
        [1, 2, 3, 4, 5]
    """
    # Caso base: listas de 0 o 1 elemento ya están ordenadas
    if len(coleccion) < 2:
        return coleccion

    # Elegimos un índice de pivote aleatorio para mejor rendimiento promedio
    indice_pivote = randrange(len(coleccion))
    pivote = coleccion.pop(indice_pivote)

    # Partición: separamos en menores/iguales y mayores al pivote
    menores  = [x for x in coleccion if x <= pivote]
    mayores  = [x for x in coleccion if x > pivote]

    # Ordenamos recursivamente cada partición y las reunimos
    return [*quick_sort(menores), pivote, *quick_sort(mayores)]


# ─────────────────────────────────────────────────────────
#  3. HEAP SORT
#  Construye un montículo máximo (max-heap) y extrae el
#  mayor elemento repetidamente para construir el orden.
#  Complejidad: O(n log n) siempre garantizado
# ─────────────────────────────────────────────────────────

def _heapify(lista: list[int], indice: int, tam_heap: int) -> None:
    """
    Mantiene la propiedad de max-heap en el subárbol con raíz
    en 'indice'. Función auxiliar de heap_sort.

    Args:
        lista:    Lista que representa el heap.
        indice:   Índice de la raíz del subárbol a ajustar.
        tam_heap: Tamaño actual del heap (parte activa de lista).
    """
    mayor     = indice          # Asumimos que la raíz es el mayor
    hijo_izq  = 2 * indice + 1  # Índice del hijo izquierdo
    hijo_der  = 2 * indice + 2  # Índice del hijo derecho

    # ¿El hijo izquierdo es mayor que la raíz actual?
    if hijo_izq < tam_heap and lista[hijo_izq] > lista[mayor]:
        mayor = hijo_izq

    # ¿El hijo derecho es mayor que el mayor encontrado hasta ahora?
    if hijo_der < tam_heap and lista[hijo_der] > lista[mayor]:
        mayor = hijo_der

    # Si la raíz no era el mayor, intercambiamos y seguimos ajustando
    if mayor != indice:
        lista[mayor], lista[indice] = lista[indice], lista[mayor]
        _heapify(lista, mayor, tam_heap)  # Ajuste recursivo hacia abajo


def heap_sort(lista: list[int]) -> list[int]:
    """
    Ordena una lista usando el algoritmo Heap Sort.

    Fase 1 – Construcción del heap: convierte la lista en max-heap.
    Fase 2 – Extracción:  mueve la raíz (mayor) al final y repara.

    Args:
        lista: Lista de enteros a ordenar.

    Returns:
        La misma lista ordenada de menor a mayor.

    Ejemplo:
        >>> heap_sort([5, 3, 1, 4, 2])
        [1, 2, 3, 4, 5]
    """
    n = len(lista)

    # ── Fase 1: Construir el max-heap ──
    # Empezamos desde el último nodo interno y subimos hasta la raíz
    for i in range(n // 2 - 1, -1, -1):
        _heapify(lista, i, n)

    # ── Fase 2: Extraer elementos del heap uno a uno ──
    for i in range(n - 1, 0, -1):
        # El elemento más grande (raíz) va al final de la parte no ordenada
        lista[0], lista[i] = lista[i], lista[0]
        # Restauramos la propiedad de heap en el heap reducido
        _heapify(lista, 0, i)

    return lista


# ─────────────────────────────────────────────────────────
#  4. RADIX SORT
#  Ordena dígito a dígito de menos significativo a más,
#  sin hacer comparaciones directas entre elementos.
#  Complejidad: O(n·k) donde k = número de dígitos del máximo
# ─────────────────────────────────────────────────────────

RADIX = 10  # Base decimal

def radix_sort(lista: list[int]) -> list[int]:
    """
    Ordena una lista de enteros no negativos usando Radix Sort
    (LSD – Least Significant Digit first).

    Itera por cada posición decimal (unidades, decenas, centenas…)
    distribuyendo los números en 10 cubetas (0–9) y recolectándolos.

    Args:
        lista: Lista de enteros no negativos.

    Returns:
        La misma lista ordenada de menor a mayor.

    Ejemplo:
        >>> radix_sort([170, 45, 75, 90, 802, 24, 2, 66])
        [2, 24, 45, 66, 75, 90, 170, 802]
    """
    posicion   = 1                   # Empezamos por el dígito de las unidades
    digito_max = max(lista)          # Valor máximo para saber cuántas pasadas hacer

    while posicion <= digito_max:
        # Crear 10 cubetas vacías (una por cada dígito 0–9)
        cubetas: list[list[int]] = [[] for _ in range(RADIX)]

        # Distribuir cada número en su cubeta según el dígito actual
        for numero in lista:
            digito = int((numero / posicion) % RADIX)
            cubetas[digito].append(numero)

        # Recolectar: vaciar las cubetas en orden de vuelta a la lista
        a = 0
        for cubeta in cubetas:
            for numero in cubeta:
                lista[a] = numero
                a += 1

        # Avanzar a la siguiente posición decimal (×10)
        posicion *= RADIX

    return lista


# ─────────────────────────────────────────────────────────
#  UTILIDADES DE INTERFAZ
# ─────────────────────────────────────────────────────────

def pedir_numeros() -> list[int]:
    """
    Solicita al usuario cuántos números quiere ingresar y luego
    los números uno a uno. Valida que la entrada sea entera.

    Returns:
        Lista de enteros ingresados por el usuario.
    """
    while True:
        try:
            cantidad = int(input("\n  ¿Cuántos números deseas ordenar? "))
            if cantidad < 1:
                print("  ⚠  Ingresa al menos 1 número.")
                continue
            break
        except ValueError:
            print("  ⚠  Por favor ingresa un número entero válido.")

    numeros = []
    print(f"\n  Ingresa {cantidad} número(s), uno por línea:")
    for i in range(1, cantidad + 1):
        while True:
            try:
                num = int(input(f"    Número {i}: "))
                numeros.append(num)
                break
            except ValueError:
                print("    ⚠  Valor inválido. Intenta de nuevo.")

    return numeros


def mostrar_resultado(original: list[int], ordenada: list[int], algoritmo: str) -> None:
    """Muestra la lista original y el resultado ordenado."""
    print(f"\n  {'─'*50}")
    print(f"  Algoritmo usado : {algoritmo}")
    print(f"  Lista original  : {original}")
    print(f"  Lista ordenada  : {ordenada}")
    print(f"  {'─'*50}")


def mostrar_menu() -> None:
    """Imprime el menú principal en pantalla."""
    print("""
╔══════════════════════════════════════════════════════════╗
║         ALGORITMOS DE ORDENAMIENTO EN PYTHON             ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   1.  Shell Sort   — gaps decrecientes                   ║
║   2.  Quick Sort   — divide y vencerás                   ║
║   3.  Heap Sort    — montículo máximo                    ║
║   4.  Radix Sort   — por dígitos (solo enteros ≥ 0)      ║
║   5.  Salir                                              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝""")


# ─────────────────────────────────────────────────────────
#  PROGRAMA PRINCIPAL
# ─────────────────────────────────────────────────────────

def main() -> None:
    """
    Función principal: muestra el menú en bucle hasta que
    el usuario elija salir (opción 5).
    """
    print("\n  Bienvenido al programa de algoritmos de ordenamiento.")

    while True:
        mostrar_menu()

        opcion = input("\n  Elige una opción (1-5): ").strip()

        if opcion == "5":
            print("\n  ¡Hasta luego! :) \n")
            break

        if opcion not in {"1", "2", "3", "4"}:
            print("\n  ⚠  Opción no válida. Elige entre 1 y 5.")
            continue

        # ── Obtener los números del usuario ──
        numeros = pedir_numeros()
        original = numeros.copy()  # Guardamos copia para mostrar al final

        # ── Ejecutar el algoritmo elegido ──
        if opcion == "1":
            resultado = shell_sort(numeros)
            mostrar_resultado(original, resultado, "Shell Sort")

        elif opcion == "2":
            resultado = quick_sort(numeros)
            mostrar_resultado(original, resultado, "Quick Sort")

        elif opcion == "3":
            resultado = heap_sort(numeros)
            mostrar_resultado(original, resultado, "Heap Sort")

        elif opcion == "4":
            # Radix Sort solo funciona con enteros no negativos
            if any(n < 0 for n in numeros):
                print("\n  ⚠  Radix Sort solo admite enteros no negativos (≥ 0).")
                print("     Prueba con otro algoritmo para números negativos.")
                continue
            resultado = radix_sort(numeros)
            mostrar_resultado(original, resultado, "Radix Sort")

        input("\n  Presiona Enter para continuar...")


if __name__ == "__main__":
    main()