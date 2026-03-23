"""
MyLinkedList.py
===============
Implementación propia de una Linked List (Lista Enlazada) en Python.
Biblioteca: MyLinkedList

Estructuras incluidas:
  - Node         : Nodo individual de la lista.
  - MyLinkedList : Lista enlazada simple con operaciones completas.
"""


# ──────────────────────────────────────────────
#  NODO
# ──────────────────────────────────────────────
class Node:
    """
    Representa un nodo dentro de la lista enlazada.

    Atributos
    ----------
    data : any
        El valor almacenado en el nodo.
    next : Node | None
        Referencia al siguiente nodo (None si es el último).
    """

    def __init__(self, data):
        self.data = data
        self.next = None          # apunta al siguiente nodo

    def __repr__(self):
        return f"Node({self.data!r})"


# ──────────────────────────────────────────────
#  LINKED LIST
# ──────────────────────────────────────────────
class MyLinkedList:
    """
    Lista enlazada simple (singly linked list).

    Métodos principales
    -------------------
    append(data)           → agrega al final          O(n)
    prepend(data)          → agrega al inicio         O(1)
    insert(index, data)    → inserta en posición dada O(n)
    delete(data)           → elimina primera ocurr.   O(n)
    delete_at(index)       → elimina por índice       O(n)
    search(data)           → busca un valor           O(n)
    get(index)             → valor por índice         O(n)
    size()                 → cantidad de elementos    O(n)
    is_empty()             → verifica si está vacía   O(1)
    reverse()              → invierte la lista        O(n)
    to_list()              → convierte a lista Python O(n)
    clear()                → vacía la lista           O(1)
    """

    def __init__(self):
        self.head = None          # primer nodo de la lista

    # ── Repesentación ────────────────────────
    def __repr__(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(repr(current.data))
            current = current.next
        return " -> ".join(nodes) + " -> None"

    def __len__(self):
        return self.size()

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __contains__(self, data):
        return self.search(data) is not None

    # ── Inserción ─────────────────────────────
    def append(self, data):
        """Agrega un nuevo nodo al FINAL de la lista."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def prepend(self, data):
        """Agrega un nuvo nodo al INICIO de la lista."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert(self, index, data):
        """
        Inserta un nodo en la posición indicada (base 0).

        Parámetros
        ----------
        index : int
            Posición donde se insertará el nodo.
        data  : any
            Valor del nuevo nodo.

        Lanza
        -----
        IndexError si el índice está fuera de rango.
        """
        if index < 0:
            raise IndexError("El índice no puede ser negativo.")
        if index == 0:
            self.prepend(data)
            return

        new_node = Node(data)
        current = self.head
        for i in range(index - 1):
            if current is None:
                raise IndexError(f"Índice {index} fuera de rango.")
            current = current.next

        if current is None:
            raise IndexError(f"Índice {index} fuera de rango.")

        new_node.next = current.next
        current.next = new_node

    # ── Eliminación ───────────────────────────
    def delete(self, data):
        """
        Elimina la PRIMERA ocurrencia del valor dado.

        Retorna True si se eliminó, False si no se encontró.
        """
        if self.head is None:
            return False

        # El nodo a eliminar es la cabeza
        if self.head.data == data:
            self.head = self.head.next
            return True

        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                return True
            current = current.next

        return False   # no encontrado

    def delete_at(self, index):
        """
        Elimina el nodo en la posición indicada (base 0).

        Retorna el valor eliminado.

        Lanza
        -----
        IndexError si el índice está fuera de rango.
        """
        if self.head is None or index < 0:
            raise IndexError("Índice fuera de rango.")

        if index == 0:
            value = self.head.data
            self.head = self.head.next
            return value

        current = self.head
        for i in range(index - 1):
            if current.next is None:
                raise IndexError(f"Índice {index} fuera de rango.")
            current = current.next

        if current.next is None:
            raise IndexError(f"Índice {index} fuera de rango.")

        value = current.next.data
        current.next = current.next.next
        return value

    # ── Búsqueda / Acceso :D ─────────────────────
    def search(self, data):
        """
        Busca el primer nodo con el valor dado.

        Retorna el objeto Node si existe, o None si no se encontró.
        """
        current = self.head
        while current:
            if current.data == data:
                return current
            current = current.next
        return None

    def get(self, index):
        """
        Retorna el valor del nodo en la posición indicada (base 0).

        Lanza
        -----
        IndexError si el índice está fuera de rango.
        """
        if index < 0:
            raise IndexError("El índice no puede ser negativo.")
        current = self.head
        for i in range(index):
            if current is None:
                raise IndexError(f"Índice {index} fuera de rango.")
            current = current.next
        if current is None:
            raise IndexError(f"Índice {index} fuera de rango.")
        return current.data

    # ── Utilidades ────────────────────────────
    def size(self):
        """Retorna la cantidad de nodos en la lista."""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def is_empty(self):
        """Retorna True si la lista está vacía."""
        return self.head is None

    def reverse(self):
        """Invierte el orden de los nodos en la lista (in-place)."""
        prev = None
        current = self.head
        while current:
            nxt = current.next   # guardar siguiente
            current.next = prev  # invertir enlace
            prev = current       # avanzar prev
            current = nxt        # avanzar current
        self.head = prev

    def to_list(self):
        """Convierte la lista enlazada en una lista de Python."""
        return list(self)

    def clear(self):
        """Elimina todos los nodos de la lista."""
        self.head = None


# ──────────────────────────────────────────────
#  DEMO / PRUEBA RÁPIDA
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("       Demo de MyLinkedList")
    print("=" * 50)

    ll = MyLinkedList()

    # Agregar elementos
    ll.append(10)
    ll.append(20)
    ll.append(30)
    ll.prepend(5)
    print("Después de append/prepend:", ll)

    # Insertar en posición
    ll.insert(2, 15)
    print("Insert(2, 15)           :", ll)

    # Buscar
    nodo = ll.search(15)
    print(f"search(15)              : {nodo}")

    # Obtener por índice
    print(f"get(0)                  : {ll.get(0)}")
    print(f"get(3)                  : {ll.get(3)}")

    # Tamaño
    print(f"size()                  : {ll.size()}")

    # Contiene
    print(f"20 in ll                : {20 in ll}")
    print(f"99 in ll                : {99 in ll}")

    # Eliminar por valor
    ll.delete(15)
    print("delete(15)              :", ll)

    # Eliminar por índice
    eliminado = ll.delete_at(0)
    print(f"delete_at(0) → {eliminado}      :", ll)

    # Invertir
    ll.reverse()
    print("reverse()               :", ll)

    # Convertir a lista Python
    print("to_list()               :", ll.to_list())

    # Iterar
    print("Iteración               :", [x for x in ll])

    # Limpiar
    ll.clear()
    print("clear() → is_empty()    :", ll.is_empty())
