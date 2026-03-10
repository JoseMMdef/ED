# ============================================================
#  PROBLEMA 1 — Suma de dos Colas
#  Estructura de Datos: Cola (Queue)
#  Descripción: Recibe dos colas de enteros y devuelve
#               una nueva cola con la suma elemento a elemento.
# ============================================================


# ──────────────────────────────────────────
#  CLASE COLA (implementación con lista)
# ──────────────────────────────────────────
class Cola:
    """
    Implementación de la estructura de datos Cola (Queue).
    Principio FIFO: el primer elemento en entrar es el primero en salir.
    """

    def __init__(self):
        """Inicializa una cola vacía."""
        self._elementos = []          # Lista interna que almacena los datos

    def enqueue(self, dato):
        """
        Inserta un elemento al FINAL de la cola.
        Parámetro:
            dato: el valor que se quiere agregar.
        """
        self._elementos.append(dato)

    def dequeue(self):
        """
        Elimina y devuelve el elemento del FRENTE de la cola.
        Lanza un error si la cola está vacía.
        """
        if self.is_empty():
            raise IndexError("No se puede hacer dequeue: la cola está vacía.")
        return self._elementos.pop(0)   # Extrae el primer elemento

    def is_empty(self):
        """Devuelve True si la cola no tiene elementos."""
        return len(self._elementos) == 0

    def tamanio(self):
        """Devuelve la cantidad de elementos en la cola."""
        return len(self._elementos)

    def __str__(self):
        """Representación legible de la cola para imprimir."""
        return "Cola: [" + " | ".join(str(e) for e in self._elementos) + "]"


# ──────────────────────────────────────────
#  FUNCIÓN PRINCIPAL: sumar_colas
# ──────────────────────────────────────────
def sumar_colas(cola_a: Cola, cola_b: Cola) -> Cola:
    """
    Recibe dos colas de numeros enteros y devuelve una nueva cola
    cuyo contenido es la suma de los elementos correspondientes.

    Precondición: ambas colas deben tener el mismo número de elementos.

    Parámetros:
        cola_a (Cola): primera cola de enteros.
        cola_b (Cola): segunda cola de enteros.

    Retorna:
        Cola: nueva cola con los resultados de la suma.
    """

    # Validación: las dos colas deben tener el mismo tamaño
    if cola_a.tamanio() != cola_b.tamanio():
        raise ValueError("Las colas deben tener el mismo número de elementos.")

    cola_resultado = Cola()   # Cola que almacenará las sumas

    # Usamos colas auxiliares para NO destruir las originales
    aux_a = Cola()
    aux_b = Cola()

    # Recorremos ambas colas al mismo tiempo
    while not cola_a.is_empty() and not cola_b.is_empty():

        # Extraemos el primer elemento de cada cola
        elemento_a = cola_a.dequeue()
        elemento_b = cola_b.dequeue()

        # Sumamos los dos elementos
        suma = elemento_a + elemento_b

        # Guardamos la suma en la cola resultado
        cola_resultado.enqueue(suma)

        # Guardamos los elementos en las auxiliares para restaurar las originales
        aux_a.enqueue(elemento_a)
        aux_b.enqueue(elemento_b)

    # Restauramos las colas originales (buena práctica: no destruir los datos)
    while not aux_a.is_empty():
        cola_a.enqueue(aux_a.dequeue())
    while not aux_b.is_empty():
        cola_b.enqueue(aux_b.dequeue())

    return cola_resultado


# ──────────────────────────────────────────
#  PROGRAMA PRINCIPAL
# ──────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 45)
    print("   SUMA DE DOS COLAS — Problema 1")
    print("=" * 45)

    # --- Crear y cargar Cola A ---
    cola_a = Cola()
    datos_a = [3, 4, 2, 8, 12]
    for numero in datos_a:
        cola_a.enqueue(numero)

    # --- Crear y cargar Cola B ---
    cola_b = Cola()
    datos_b = [6, 2, 9, 11, 3]
    for numero in datos_b:
        cola_b.enqueue(numero)

    # --- Mostrar las colas originales ---
    print(f"\nCola A    → {cola_a}")
    print(f"Cola B    → {cola_b}")

    # --- Calcular la suma ---
    cola_resultado = sumar_colas(cola_a, cola_b)

    # --- Mostrar resultado ---
    print(f"\nResultado → {cola_resultado}")

    # --- Verificar que las originales no fueron alteradas ---
    print("\n(Las colas originales se mantienen intactas)")
    print(f"Cola A    → {cola_a}")
    print(f"Cola B    → {cola_b}")

    print("\n" + "=" * 45)
    print("Tabla de sumas:")
    print(f"  {'Cola A':>8} {'Cola B':>8} {'Resultado':>10}")
    print("-" * 30)

    # Imprimir tabla de resultados
    temp_a = list(datos_a)
    temp_b = list(datos_b)
    temp_r = Cola()
    temp_resultado = sumar_colas(Cola(), Cola())   # ya calculada arriba

    for a, b in zip(datos_a, datos_b):
        print(f"  {a:>8} {b:>8} {a+b:>10}")

    print("=" * 45)
