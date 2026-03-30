"""
=============================================================
  GRAFO DE ESTADOS DE MÉXICO - Programa Educativo con Tkinter
=============================================================
  Autor: Generado con Claude (Anthropic)
  Descripción: Representa 7 estados mexicanos como un grafo,
               permite hacer recorridos con o sin repetición
               y muestra el costo total de cada ruta.

  Cómo ejecutarlo:
    1. Tener Python 3 instalado (Tkinter viene incluido)
    2. Guardar este archivo como: grafos_mexico.py
    3. Ejecutar en terminal: python grafos_mexico.py
=============================================================
"""

import tkinter as tk
from tkinter import scrolledtext
import random

# ─────────────────────────────────────────────
#  DATOS DEL GRAFO
#  Representamos el grafo como un diccionario:
#    nodo -> lista de (vecino, costo)
# ─────────────────────────────────────────────

# Los 7 estados que usaremos como nodos
ESTADOS = [
    "CDMX",
    "Jalisco",
    "Yucatán",
    "Nuevo León",
    "Oaxaca",
    "Veracruz",
    "Chihuahua",
]

# Conexiones (aristas) entre estados con su costo de traslado
# Formato: (estado_origen, estado_destino, costo)
# El grafo es NO dirigido: si A conecta con B, B conecta con A
CONEXIONES = [
    ("CDMX",       "Jalisco",     3),
    ("CDMX",       "Veracruz",    2),
    ("CDMX",       "Oaxaca",      4),
    ("Jalisco",    "Chihuahua",   5),
    ("Jalisco",    "Nuevo León",  4),
    ("Veracruz",   "Yucatán",     3),
    ("Veracruz",   "Oaxaca",      2),
    ("Oaxaca",     "Yucatán",     4),
    ("Nuevo León", "Chihuahua",   3),
    ("Nuevo León", "CDMX",        5),
    ("Yucatán",    "Nuevo León",  6),
    ("Chihuahua",  "Veracruz",    7),
    ("Chihuahua",  "CDMX",        6),   # conexión adicional para cerrar el ciclo
]

# ─────────────────────────────────────────────
#  FUNCIÓN: Construir el grafo como diccionario
#  Convierte la lista CONEXIONES en un dict
#  para acceder rápidamente a los vecinos.
# ─────────────────────────────────────────────
def construir_grafo():
    grafo = {}

    # Inicializamos cada nodo con lista vacía
    for estado in ESTADOS:
        grafo[estado] = []

    # Llenamos las conexiones en ambas direcciones
    for origen, destino, costo in CONEXIONES:
        grafo[origen].append((destino, costo))
        grafo[destino].append((origen, costo))   # grafo no dirigido

    return grafo


# ─────────────────────────────────────────────
#  FUNCIÓN: Calcular el costo total de una ruta
#  Recibe una lista de estados (la ruta)
#  y suma los costos entre estados consecutivos.
# ─────────────────────────────────────────────
def calcular_costo(grafo, ruta):
    costo_total = 0

    for i in range(len(ruta) - 1):
        origen  = ruta[i]
        destino = ruta[i + 1]
        encontrado = False

        # Buscar el costo entre origen y destino en el grafo
        for vecino, costo in grafo[origen]:
            if vecino == destino:
                costo_total += costo
                encontrado = True
                break

        # Si no hay conexión directa, sumar un costo alto (penalización)
        if not encontrado:
            costo_total += 99  # penalización por no haber ruta directa

    return costo_total


# ─────────────────────────────────────────────
#  FUNCIÓN AUXILIAR: DFS con backtracking
#  Intenta construir un camino que visite
#  todos los nodos exactamente una vez.
#  Devuelve True si lo logra, False si no.
# ─────────────────────────────────────────────
def _dfs_backtrack(grafo, nodo_actual, visitados, ruta):
    ruta.append(nodo_actual)    # añadimos el nodo a la ruta
    visitados.add(nodo_actual)  # lo marcamos como visitado

    # Caso base: si ya visitamos todos los nodos, éxito
    if len(ruta) == len(grafo):
        return True

    # Intentar ir a cada vecino no visitado
    for vecino, _ in grafo[nodo_actual]:
        if vecino not in visitados:
            if _dfs_backtrack(grafo, vecino, visitados, ruta):
                return True   # encontramos un camino completo

    # Si ningún vecino funcionó, deshacemos este paso (backtrack)
    ruta.pop()
    visitados.discard(nodo_actual)
    return False


# ─────────────────────────────────────────────
#  FUNCIÓN: Recorrido SIN repetir estados
#  Usa DFS con backtracking para garantizar
#  que se visiten los 7 estados exactamente
#  una vez usando aristas existentes del grafo.
# ─────────────────────────────────────────────
def recorrido_sin_repetir(grafo, inicio):
    ruta      = []       # ruta que se va construyendo
    visitados = set()    # estados ya usados

    encontrado = _dfs_backtrack(grafo, inicio, visitados, ruta)

    # Si no encontró camino completo, devuelve lo que pudo recorrer
    if not encontrado:
        return ruta if ruta else [inicio]

    return ruta


# ─────────────────────────────────────────────
#  FUNCIÓN: Recorrido CON repetición
#  Genera una ruta que deliberadamente pasa
#  dos veces por un estado (el nodo de inicio).
#  Simula una "vuelta" al punto de partida.
# ─────────────────────────────────────────────
def recorrido_con_repeticion(grafo, inicio):
    # Primero obtenemos el recorrido sin repetir
    ruta_base = recorrido_sin_repetir(grafo, inicio)

    # Añadimos el inicio al final para crear la repetición
    # Resultado: inicio → ... → ultimo → inicio
    ruta_con_rep = ruta_base + [inicio]

    return ruta_con_rep


# ─────────────────────────────────────────────
#  POSICIONES de los nodos en el Canvas
#  Coordenadas (x, y) de cada estado para
#  dibujarlos en la interfaz gráfica.
# ─────────────────────────────────────────────
POSICIONES = {
    "CDMX":       (340, 240),
    "Jalisco":    (200, 200),
    "Yucatán":    (490, 310),
    "Nuevo León": (290, 130),
    "Oaxaca":     (390, 330),
    "Veracruz":   (450, 220),
    "Chihuahua":  (190, 100),
}

# Paleta de colores del tema
COLOR_FONDO        = "#0d1117"
COLOR_PANEL        = "#161b22"
COLOR_ACENTO       = "#58a6ff"
COLOR_ACENTO2      = "#3fb950"
COLOR_ALERTA       = "#f78166"
COLOR_TEXTO        = "#e6edf3"
COLOR_TEXTO_DIM    = "#8b949e"
COLOR_NODO         = "#21262d"
COLOR_NODO_BORDE   = "#30363d"
COLOR_ARISTA       = "#30363d"
COLOR_ARISTA_ACTIVA= "#f0883e"
RADIO_NODO         = 28


# ─────────────────────────────────────────────
#  FUNCIÓN: Dibujar el grafo en el Canvas
#  Dibuja círculos (estados) y líneas (conexiones)
# ─────────────────────────────────────────────
def dibujar_grafo(canvas, ruta_resaltar=None):
    canvas.delete("all")  # limpiar canvas antes de redibujar

    # Dibujar fondo con cuadrícula sutil
    for i in range(0, 700, 30):
        canvas.create_line(i, 0, i, 420, fill="#1c2128", width=1)
    for j in range(0, 420, 30):
        canvas.create_line(0, j, 700, j, fill="#1c2128", width=1)

    # Construir set de aristas de la ruta a resaltar
    aristas_ruta = set()
    if ruta_resaltar and len(ruta_resaltar) > 1:
        for i in range(len(ruta_resaltar) - 1):
            par = (ruta_resaltar[i], ruta_resaltar[i+1])
            aristas_ruta.add(par)
            aristas_ruta.add((par[1], par[0]))  # ambos sentidos

    # ── Dibujar aristas (líneas entre estados) ──
    for origen, destino, costo in CONEXIONES:
        x1, y1 = POSICIONES[origen]
        x2, y2 = POSICIONES[destino]

        es_activa = (origen, destino) in aristas_ruta

        color_linea = COLOR_ARISTA_ACTIVA if es_activa else COLOR_ARISTA
        grosor      = 3 if es_activa else 1

        canvas.create_line(x1, y1, x2, y2,
                           fill=color_linea,
                           width=grosor,
                           dash=() if es_activa else (4, 4))

        # Etiqueta del costo en el punto medio de la arista
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        canvas.create_rectangle(mx - 12, my - 9, mx + 12, my + 9,
                                 fill=COLOR_PANEL, outline=color_linea)
        canvas.create_text(mx, my,
                           text=str(costo),
                           fill=COLOR_ACENTO if es_activa else COLOR_TEXTO_DIM,
                           font=("Courier", 9, "bold"))

    # ── Dibujar nodos (círculos con nombre del estado) ──
    for estado, (x, y) in POSICIONES.items():
        en_ruta = ruta_resaltar and estado in ruta_resaltar
        es_inicio = ruta_resaltar and estado == ruta_resaltar[0]

        # Efecto de brillo para nodos en la ruta
        if en_ruta:
            for r in range(RADIO_NODO + 12, RADIO_NODO - 1, -3):
                alpha_color = COLOR_ACENTO if not es_inicio else COLOR_ACENTO2
                canvas.create_oval(x - r, y - r, x + r, y + r,
                                   fill="", outline=alpha_color,
                                   width=1)

        color_relleno = "#1f3a5f" if en_ruta else COLOR_NODO
        color_borde   = COLOR_ACENTO if en_ruta else COLOR_NODO_BORDE
        if es_inicio:
            color_relleno = "#1a3a2a"
            color_borde   = COLOR_ACENTO2

        # Círculo principal del nodo
        canvas.create_oval(
            x - RADIO_NODO, y - RADIO_NODO,
            x + RADIO_NODO, y + RADIO_NODO,
            fill=color_relleno, outline=color_borde, width=2
        )

        # Nombre del estado (partido en 2 líneas si es largo)
        nombre = estado
        partes = nombre.split()
        if len(partes) > 1:
            linea1 = partes[0]
            linea2 = " ".join(partes[1:])
            canvas.create_text(x, y - 6, text=linea1,
                               fill=COLOR_TEXTO, font=("Courier", 8, "bold"))
            canvas.create_text(x, y + 6, text=linea2,
                               fill=COLOR_TEXTO, font=("Courier", 8, "bold"))
        else:
            canvas.create_text(x, y, text=nombre,
                               fill=COLOR_TEXTO, font=("Courier", 8, "bold"))

        # Número de orden en la ruta
        if ruta_resaltar and estado in ruta_resaltar:
            indices = [str(i+1) for i, e in enumerate(ruta_resaltar) if e == estado]
            canvas.create_text(x + RADIO_NODO - 2, y - RADIO_NODO + 2,
                               text=",".join(indices),
                               fill=COLOR_ACENTO2,
                               font=("Courier", 8, "bold"))


# ─────────────────────────────────────────────
#  FUNCIÓN: Formatear ruta para mostrar en pantalla
# ─────────────────────────────────────────────
def formatear_ruta(ruta, costo):
    flecha = " → "
    linea_ruta = flecha.join(ruta)
    return f"Ruta:  {linea_ruta}\nCosto total: {costo} unidades"


# ─────────────────────────────────────────────
#  INTERFAZ GRÁFICA PRINCIPAL (Tkinter)
# ─────────────────────────────────────────────
def iniciar_interfaz():
    grafo = construir_grafo()  # construir el grafo al arrancar

    # ── Ventana principal ──
    ventana = tk.Tk()
    ventana.title("Grafo de Estados de México")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    # ── Título ──
    tk.Label(
        ventana,
        text="◈  GRAFO DE ESTADOS DE MÉXICO  ◈",
        bg=COLOR_FONDO,
        fg=COLOR_ACENTO,
        font=("Courier", 14, "bold"),
        pady=12,
    ).pack()

    # ── Marco principal (canvas + panel derecho) ──
    marco_principal = tk.Frame(ventana, bg=COLOR_FONDO)
    marco_principal.pack(padx=15, pady=0)

    # ── Canvas para el dibujo del grafo ──
    canvas = tk.Canvas(
        marco_principal,
        width=660,
        height=420,
        bg=COLOR_FONDO,
        highlightthickness=1,
        highlightbackground=COLOR_NODO_BORDE,
    )
    canvas.grid(row=0, column=0, padx=(0, 10))
    dibujar_grafo(canvas)  # dibujo inicial sin ruta resaltada

    # ── Panel derecho: información y botones ──
    panel = tk.Frame(marco_principal, bg=COLOR_PANEL,
                     bd=0, relief="flat",
                     padx=14, pady=14)
    panel.grid(row=0, column=1, sticky="ns")

    # Lista de estados
    tk.Label(panel, text="NODOS (Estados)",
             bg=COLOR_PANEL, fg=COLOR_ACENTO,
             font=("Courier", 10, "bold")).pack(anchor="w")

    for estado in ESTADOS:
        tk.Label(panel, text=f"  ▸ {estado}",
                 bg=COLOR_PANEL, fg=COLOR_TEXTO,
                 font=("Courier", 9)).pack(anchor="w")

    tk.Label(panel, text="", bg=COLOR_PANEL).pack()  # separador

    # Lista de conexiones
    tk.Label(panel, text="ARISTAS (Conexiones)",
             bg=COLOR_PANEL, fg=COLOR_ACENTO,
             font=("Courier", 10, "bold")).pack(anchor="w")

    for origen, destino, costo in CONEXIONES:
        abrev_o = origen[:4]
        abrev_d = destino[:4]
        tk.Label(panel,
                 text=f"  {abrev_o} ↔ {abrev_d}  [{costo}]",
                 bg=COLOR_PANEL, fg=COLOR_TEXTO_DIM,
                 font=("Courier", 8)).pack(anchor="w")

    tk.Label(panel, text="", bg=COLOR_PANEL).pack()

    # ── Selector de estado inicial ──
    tk.Label(panel, text="Estado de inicio:",
             bg=COLOR_PANEL, fg=COLOR_ACENTO,
             font=("Courier", 9, "bold")).pack(anchor="w")

    estado_var = tk.StringVar(value=ESTADOS[0])
    menu_estados = tk.OptionMenu(panel, estado_var, *ESTADOS)
    menu_estados.config(bg=COLOR_NODO, fg=COLOR_TEXTO,
                        font=("Courier", 9),
                        activebackground=COLOR_ACENTO,
                        highlightthickness=0, bd=0)
    menu_estados["menu"].config(bg=COLOR_NODO, fg=COLOR_TEXTO,
                                font=("Courier", 9))
    menu_estados.pack(fill="x", pady=(2, 10))

    # ── Botones de acción ──
    def estilo_boton(texto, color_fondo, comando):
        return tk.Button(
            panel,
            text=texto,
            command=comando,
            bg=color_fondo,
            fg=COLOR_FONDO,
            font=("Courier", 9, "bold"),
            relief="flat",
            pady=8,
            cursor="hand2",
            activebackground=COLOR_TEXTO,
            activeforeground=COLOR_FONDO,
        )

    # ── Área de resultados ──
    area_resultado = scrolledtext.ScrolledText(
        ventana,
        height=6,
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO,
        font=("Courier", 10),
        relief="flat",
        bd=0,
        padx=12,
        pady=10,
        wrap="word",
        state="disabled",
    )
    area_resultado.pack(fill="x", padx=15, pady=(8, 0))

    def mostrar_resultado(titulo, texto, color):
        area_resultado.config(state="normal")
        area_resultado.delete("1.0", "end")
        area_resultado.insert("end", f"{'─'*55}\n")
        area_resultado.insert("end", f"  {titulo}\n")
        area_resultado.insert("end", f"{'─'*55}\n")
        area_resultado.insert("end", f"  {texto}\n")
        area_resultado.config(state="disabled")

    # ── Acción: Recorrido sin repetir ──
    def accion_sin_repetir():
        inicio = estado_var.get()
        ruta   = recorrido_sin_repetir(grafo, inicio)
        costo  = calcular_costo(grafo, ruta)
        texto  = formatear_ruta(ruta, costo)
        mostrar_resultado("RECORRIDO SIN REPETIR ESTADOS", texto, COLOR_ACENTO)
        dibujar_grafo(canvas, ruta_resaltar=ruta)

    # ── Acción: Recorrido con repetición ──
    def accion_con_repeticion():
        inicio = estado_var.get()
        ruta   = recorrido_con_repeticion(grafo, inicio)
        costo  = calcular_costo(grafo, ruta)
        texto  = formatear_ruta(ruta, costo)
        mostrar_resultado("RECORRIDO CON REPETICIÓN (regresa al inicio)", texto, COLOR_ALERTA)
        dibujar_grafo(canvas, ruta_resaltar=ruta)

    # ── Acción: Resetear grafo ──
    def accion_resetear():
        mostrar_resultado("", "Selecciona un tipo de recorrido para comenzar.", "")
        dibujar_grafo(canvas)

    btn_sin  = estilo_boton("▶  Recorrido sin repetir",   COLOR_ACENTO,  accion_sin_repetir)
    btn_con  = estilo_boton("↺  Recorrido con repetición", COLOR_ALERTA,  accion_con_repeticion)
    btn_rst  = estilo_boton("↺  Resetear grafo",           COLOR_TEXTO_DIM, accion_resetear)

    btn_sin.pack(fill="x", pady=3)
    btn_con.pack(fill="x", pady=3)
    btn_rst.pack(fill="x", pady=(10, 0))

    # ── Barra de estado inferior ──
    tk.Label(
        ventana,
        text="  Nodos: 7 estados   |   Aristas: 12 conexiones   |   Grafo no dirigido  ",
        bg=COLOR_NODO_BORDE,
        fg=COLOR_TEXTO_DIM,
        font=("Courier", 8),
        anchor="w",
        pady=4,
    ).pack(fill="x", pady=(10, 0))

    # Mensaje inicial en el área de resultados
    mostrar_resultado("", "Selecciona un estado de inicio y presiona un botón para ver el recorrido.", "")

    ventana.mainloop()


# ─────────────────────────────────────────────
#  PUNTO DE ENTRADA DEL PROGRAMA
# ─────────────────────────────────────────────
if __name__ == "__main__":
    iniciar_interfaz()
