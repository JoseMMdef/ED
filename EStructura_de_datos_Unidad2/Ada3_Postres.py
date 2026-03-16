# ============================================================
#  ESTRUCTURA DE DATOS - LISTA DE POSTRES
#  Programa: Gestión de postres e ingredientes usando listas
# ============================================================

# Estructura inicial: lista de listas [nombre_postre, [ingredientes]]
# Ordenada alfabéticamente por nombre de postre
POSTRES = [
    ["Arroz con leche", ["arroz", "leche", "azúcar", "canela"]],
    ["Flan",            ["leche", "huevo", "azúcar", "vainilla"]],
    ["Gelatina",        ["agua", "gelatina", "azúcar"]],
    ["Helado",          ["leche", "crema", "azúcar", "vainilla"]],
    ["Pastel",          ["harina", "huevo", "azúcar", "mantequilla"]],
]


# ────────────────────────────────────────────────────────────
# FUNCIÓN AUXILIAR: buscar el índice de un postre por nombre
# ────────────────────────────────────────────────────────────
def _buscar_indice(nombre):
    """
    Busca la posición de un postre en POSTRES (búsqueda lineal).
    Retorna el índice entero si lo encuentra, -1 si no existe.
    La comparación es insensible a mayúsculas/minúsculas.
    """
    nombre_lower = nombre.strip().lower()
    for i in range(len(POSTRES)):
        if POSTRES[i][0].lower() == nombre_lower:
            return i
    return -1


# ────────────────────────────────────────────────────────────
# 1. BUSCAR UN POSTRE
# ────────────────────────────────────────────────────────────
def buscar_postre(nombre):
    """
    Dado el nombre de un postre, imprime todos sus ingredientes.
    Caso especial: postre no encontrado.
    """
    idx = _buscar_indice(nombre)
    if idx == -1:
        print(f"  ✗ El postre '{nombre}' no existe en la lista.")
        return

    ingredientes = POSTRES[idx][1]
    if len(ingredientes) == 0:
        print(f"  '{POSTRES[idx][0]}' no tiene ingredientes registrados.")
    else:
        print(f"  Ingredientes de '{POSTRES[idx][0]}':")
        for ing in ingredientes:
            print(f"    • {ing}")


# ────────────────────────────────────────────────────────────
# 2. INSERTAR INGREDIENTES
# ────────────────────────────────────────────────────────────
def insertar_ingrediente(nombre_postre, nuevo_ingrediente):
    """
    Agrega un nuevo ingrediente a la lista del postre indicado.
    Casos especiales:
      - Postre no encontrado.
      - Ingrediente ya existe (evita duplicados dentro de un postre).
      - Ingrediente vacío o solo espacios.
    """
    nuevo_ing = nuevo_ingrediente.strip().lower()
    if not nuevo_ing:
        print("  ✗ El ingrediente no puede estar vacío.")
        return

    idx = _buscar_indice(nombre_postre)
    if idx == -1:
        print(f"  ✗ El postre '{nombre_postre}' no existe.")
        return

    # Verificar duplicado dentro de la lista de ingredientes
    ingredientes = POSTRES[idx][1]
    if nuevo_ing in [i.lower() for i in ingredientes]:
        print(f"  ✗ '{nuevo_ing}' ya es un ingrediente de '{POSTRES[idx][0]}'.")
        return

    ingredientes.append(nuevo_ing)
    print(f"  ✓ Ingrediente '{nuevo_ing}' agregado a '{POSTRES[idx][0]}'.")


# ────────────────────────────────────────────────────────────
# 3. ELIMINAR INGREDIENTES
# ────────────────────────────────────────────────────────────
def eliminar_ingrediente(nombre_postre, ingrediente):
    """
    Elimina un ingrediente específico del postre indicado.
    Casos especiales:
      - Postre no encontrado.
      - Ingrediente no pertenece al postre.
      - Lista de ingredientes vacía.
    """
    idx = _buscar_indice(nombre_postre)
    if idx == -1:
        print(f"  ✗ El postre '{nombre_postre}' no existe.")
        return

    ingredientes = POSTRES[idx][1]
    if len(ingredientes) == 0:
        print(f"  ✗ '{POSTRES[idx][0]}' no tiene ingredientes que eliminar.")
        return

    ing_lower = ingrediente.strip().lower()
    # Buscar el ingrediente (insensible a mayúsculas)
    for i in range(len(ingredientes)):
        if ingredientes[i].lower() == ing_lower:
            ingredientes.pop(i)
            print(f"  ✓ Ingrediente '{ing_lower}' eliminado de '{POSTRES[idx][0]}'.")
            return

    print(f"  ✗ '{ing_lower}' no es un ingrediente de '{POSTRES[idx][0]}'.")


# ────────────────────────────────────────────────────────────
# 4. ALTA DE POSTRE
# ────────────────────────────────────────────────────────────
def alta_postre(nombre, ingredientes):
    """
    Agrega un nuevo postre manteniendo POSTRES ordenado alfabéticamente.
    Parámetro ingredientes: lista de strings.
    Casos especiales:
      - Nombre vacío.
      - Postre ya existe.
      - Ingredientes duplicados dentro de la nueva lista (se depuran).
    """
    nombre = nombre.strip()
    if not nombre:
        print("  ✗ El nombre del postre no puede estar vacío.")
        return

    if _buscar_indice(nombre) != -1:
        print(f"  ✗ El postre '{nombre}' ya existe.")
        return

    # Limpiar y deduplicar ingredientes recibidos
    ings_limpios = []
    vistos = []
    for ing in ingredientes:
        ing_clean = ing.strip().lower()
        if ing_clean and ing_clean not in vistos:
            ings_limpios.append(ing_clean)
            vistos.append(ing_clean)

    # Insertar en la posición correcta para mantener orden alfabético
    nuevo = [nombre, ings_limpios]
    insertado = False
    for i in range(len(POSTRES)):
        if nombre.lower() < POSTRES[i][0].lower():
            POSTRES.insert(i, nuevo)
            insertado = True
            break
    if not insertado:
        POSTRES.append(nuevo)

    print(f"  ✓ Postre '{nombre}' agregado con {len(ings_limpios)} ingrediente(s).")


# ────────────────────────────────────────────────────────────
# 5. BAJA DE POSTRE
# ────────────────────────────────────────────────────────────
def baja_postre(nombre):
    """
    Elimina un postre completo (nombre + lista de ingredientes).
    Casos especiales:
      - Postre no encontrado.
      - POSTRES vacío.
    """
    if len(POSTRES) == 0:
        print("  ✗ La estructura POSTRES está vacía.")
        return

    idx = _buscar_indice(nombre)
    if idx == -1:
        print(f"  ✗ El postre '{nombre}' no existe.")
        return

    nombre_real = POSTRES[idx][0]
    POSTRES.pop(idx)
    print(f"  ✓ Postre '{nombre_real}' y todos sus ingredientes fueron eliminados.")


# ────────────────────────────────────────────────────────────
# 6. ELIMINAR POSTRES REPETIDOS
# ────────────────────────────────────────────────────────────
def eliminar_repetidos():
    """
    Recorre POSTRES y elimina entradas cuyo nombre esté duplicado.
    Conserva la PRIMERA aparición de cada postre.

    ANÁLISIS (punto 7):
    ─────────────────────────────────────────────────────────
    Cuando dos entradas comparten el MISMO nombre pero tienen
    listas de ingredientes DISTINTAS (objetos distintos en memoria),
    al eliminar el duplicado sólo se pierde esa sublista; la primera
    permanece intacta → sin errores.

    Si, en cambio, ambas entradas apuntan al MISMO objeto lista
    (alias), cualquier modificación previa en una afecta a la otra.
    Al eliminar la entrada duplicada el objeto lista sigue referenciado
    por la entrada que se conserva → no hay error, pero el historial
    de modificaciones compartidas puede ser inesperado para el programador.

    Conclusión: Python no lanza ningún error al eliminar repetidos,
    pero el aliasing (referencias compartidas) puede provocar
    comportamiento inesperado si no se usa copy() al crear duplicados.
    ─────────────────────────────────────────────────────────
    """
    vistos_nombres = []   # nombres ya registrados (lowercase)
    indices_a_borrar = [] # índices de duplicados a eliminar

    for i in range(len(POSTRES)):
        nombre_lower = POSTRES[i][0].lower()
        if nombre_lower in vistos_nombres:
            indices_a_borrar.append(i)
        else:
            vistos_nombres.append(nombre_lower)

    if len(indices_a_borrar) == 0:
        print("  ✓ No hay postres repetidos en la estructura.")
        return

    # Eliminar en orden inverso para no alterar los índices restantes
    for i in reversed(indices_a_borrar):
        print(f"  ✗ Eliminando duplicado: '{POSTRES[i][0]}'")
        POSTRES.pop(i)

    print(f"  ✓ Se eliminaron {len(indices_a_borrar)} postre(s) duplicado(s).")


# ────────────────────────────────────────────────────────────
# UTILIDAD: mostrar toda la estructura POSTRES
# ────────────────────────────────────────────────────────────
def mostrar_todos():
    """Imprime la estructura POSTRES completa."""
    if len(POSTRES) == 0:
        print("  (La estructura POSTRES está vacía)")
        return
    print("  ESTRUCTURA POSTRES:")
    print(f"  {'#':<4} {'Postre':<20} Ingredientes")
    print("  " + "─" * 55)
    for i, entrada in enumerate(POSTRES):
        ings = ", ".join(entrada[1]) if entrada[1] else "(sin ingredientes)"
        print(f"  {i:<4} {entrada[0]:<20} {ings}")


# ════════════════════════════════════════════════════════════
#  PROGRAMA PRINCIPAL – DEMOSTRACIÓN DE TODAS LAS FUNCIONES
# ════════════════════════════════════════════════════════════
if __name__ == "__main__":

    separador = "\n" + "═" * 60

    # ── Estado inicial ───────────────────────────────────────
    print(separador)
    print(" ESTADO INICIAL")
    print(separador)
    mostrar_todos()

    # ── 1. Buscar postre ─────────────────────────────────────
    print(separador)
    print(" 1. BUSCAR POSTRE")
    print(separador)
    buscar_postre("Flan")
    buscar_postre("Churros")          # no existe

    # ── 2. Insertar ingrediente ──────────────────────────────
    print(separador)
    print(" 2. INSERTAR INGREDIENTE")
    print(separador)
    insertar_ingrediente("Pastel", "chocolate")
    insertar_ingrediente("Pastel", "azúcar")    # ya existe
    insertar_ingrediente("Tarta", "fresa")      # postre no existe
    insertar_ingrediente("Flan", "")            # ingrediente vacío
    buscar_postre("Pastel")

    # ── 3. Eliminar ingrediente ──────────────────────────────
    print(separador)
    print(" 3. ELIMINAR INGREDIENTE")
    print(separador)
    eliminar_ingrediente("Gelatina", "azúcar")
    eliminar_ingrediente("Gelatina", "sal")     # no pertenece
    eliminar_ingrediente("Brownie", "harina")   # postre no existe
    buscar_postre("Gelatina")

    # ── 4. Alta de postre ────────────────────────────────────
    print(separador)
    print(" 4. ALTA DE POSTRE")
    print(separador)
    alta_postre("Brownie", ["chocolate", "harina", "mantequilla", "azúcar"])
    alta_postre("Flan", ["leche"])              # ya existe
    alta_postre("", ["harina"])                 # nombre vacío
    alta_postre("Churros", ["harina", "agua", "sal", "harina"])  # ing duplicado en entrada
    mostrar_todos()

    # ── 5. Baja de postre ────────────────────────────────────
    print(separador)
    print(" 5. BAJA DE POSTRE")
    print(separador)
    baja_postre("Helado")
    baja_postre("Pizza")                        # no existe
    mostrar_todos()

    # ── 6. Eliminar repetidos ────────────────────────────────
    print(separador)
    print(" 6. ELIMINAR POSTRES REPETIDOS")
    print(separador)

    # Agregar duplicados manualmente para demostrar
    POSTRES.append(["Flan", ["leche", "huevo"]])          # duplicado nombre, lista distinta
    lista_compartida = ["azúcar", "agua"]
    POSTRES.append(["Gelatina", lista_compartida])        # duplicado con referencia externa
    POSTRES.append(["Brownie", ["chocolate", "nuez"]])    # duplicado nombre, lista distinta

    print("  Antes de limpiar:")
    mostrar_todos()
    print()
    eliminar_repetidos()
    print()
    print("  Después de limpiar:")
    mostrar_todos()

    # ── 7. Análisis impreso ──────────────────────────────────
    print(separador)
    print(" 7. ANÁLISIS: ¿Qué pasa con los ingredientes al eliminar repetidos?")
    print(separador)
    print("""
  Caso A – Listas de ingredientes DISTINTAS (objetos distintos):
    • Cada entrada del postre duplicado tiene su propia lista.
    • Al hacer pop() del duplicado, esa lista queda sin referencia
      y Python la libera (garbage collection).
    • La entrada original conserva su lista intacta.
    → No ocurre error ni comportamiento inesperado.

  Caso B – Listas COMPARTIDAS (aliasing):
    • Si dos entradas apuntan al MISMO objeto lista, cualquier
      .append() o .remove() hecho en una afecta a la otra.
    • Al eliminar el duplicado la lista NO desaparece; sigue
      siendo referenciada por la entrada conservada.
    → No hay error, pero los cambios previos "se cuelan"
      entre entradas, lo que puede ser inesperado.

  Conclusión:
    Python NO lanza ningún error al eliminar postres repetidos.
    La diferencia clave está en si las listas de ingredientes son
    objetos independientes o aliases. Para evitar aliasing se debe
    usar lista.copy() (copia superficial) o copy.deepcopy()
    (copia profunda) al duplicar entradas.
""")