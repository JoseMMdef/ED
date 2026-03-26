"""
=============================================================
  TDA GRAFO - Implementación completa con interfaz gráfica
  Lenguaje: Python 3 | GUI: Tkinter + Canvas
=============================================================
"""

import tkinter as tk
from tkinter import messagebox
import math


# ─────────────────────────────────────────────────────────────
#  CLASE: Vertice
# ─────────────────────────────────────────────────────────────
class Vertice:
    """Representa un vértice del grafo con etiqueta y posición visual en el canvas."""

    def __init__(self, etiqueta: str):
        self.etiqueta = etiqueta   # nombre visible del vértice
        self.elemento = etiqueta   # elemento almacenado (operaciones posicionales)
        self.x = 0                 # coordenada X en el canvas
        self.y = 0                 # coordenada Y en el canvas

    def __repr__(self):
        return f"V({self.etiqueta})"

    def __eq__(self, other):
        return isinstance(other, Vertice) and self.etiqueta == other.etiqueta

    def __hash__(self):
        return hash(self.etiqueta)


# ─────────────────────────────────────────────────────────────
#  CLASE: Arista
# ─────────────────────────────────────────────────────────────
class Arista:
    """Representa una arista no dirigida que conecta dos vértices."""

    def __init__(self, u: Vertice, v: Vertice):
        self.u = u                                          # primer extremo
        self.v = v                                          # segundo extremo
        self.elemento = f"{u.etiqueta}-{v.etiqueta}"       # representación textual

    def __repr__(self):
        return f"A({self.u.etiqueta}-{self.v.etiqueta})"

    def __eq__(self, other):
        # Las aristas son iguales sin importar el orden de los vértices
        if not isinstance(other, Arista):
            return False
        return (self.u == other.u and self.v == other.v) or \
               (self.u == other.v and self.v == other.u)

    def __hash__(self):
        return hash(frozenset([self.u.etiqueta, self.v.etiqueta]))


# ─────────────────────────────────────────────────────────────
#  CLASE: Grafo (TDA completo con lista de adyacencia)
# ─────────────────────────────────────────────────────────────
class Grafo:
    """
    TDA Grafo implementado con lista de adyacencia.

    Soporta:
      ① Información general   : numVertices, numAristas, vertices, aristas
      ② Vértices y aristas    : grado, verticesAdyacentes, aristasIncidentes,
                                verticesFinales, opuesto, esAdyacente
      ③ Operaciones posicion. : tamaño, estaVacio, elementos, posiciones,
                                reemplazar, intercambiar
    """

    def __init__(self):
        # Diccionario: etiqueta (str) -> objeto Vertice
        self._vertices: dict[str, Vertice] = {}
        # Diccionario: Vertice -> lista de Aristas incidentes
        self._adyacencia: dict[Vertice, list] = {}
        # Lista global de aristas (sin duplicados)
        self._aristas: list[Arista] = []

    # ── ① Información general ──────────────────────────────
    def numVertices(self) -> int:
        """Retorna el número total de vértices."""
        return len(self._vertices)

    def numAristas(self) -> int:
        """Retorna el número total de aristas."""
        return len(self._aristas)

    def vertices(self) -> list:
        """Retorna una lista con todos los objetos Vertice."""
        return list(self._vertices.values())

    def aristas(self) -> list:
        """Retorna una lista con todos los objetos Arista."""
        return list(self._aristas)

    # ── ② Operaciones sobre vértices y aristas ─────────────
    def grado(self, etiqueta: str) -> int:
        """Retorna el número de aristas incidentes en el vértice v."""
        v = self._get_vertice(etiqueta)
        return len(self._adyacencia[v])

    def verticesAdyacentes(self, etiqueta: str) -> list:
        """Retorna la lista de vértices adyacentes a v."""
        v = self._get_vertice(etiqueta)
        return [self._opuesto_obj(v, a) for a in self._adyacencia[v]]

    def aristasIncidentes(self, etiqueta: str) -> list:
        """Retorna la lista de aristas incidentes en v."""
        v = self._get_vertice(etiqueta)
        return list(self._adyacencia[v])

    def verticesFinales(self, arista_str: str) -> tuple:
        """
        Dado el string 'A-B', retorna la tupla (VerticeA, VerticeB).
        Lanza ValueError si la arista no existe.
        """
        u_et, v_et = self._parsear_arista_str(arista_str)
        u = self._get_vertice(u_et)
        v = self._get_vertice(v_et)
        for a in self._aristas:
            if (a.u == u and a.v == v) or (a.u == v and a.v == u):
                return (a.u, a.v)
        raise ValueError(f"La arista '{arista_str}' no existe en el grafo.")

    def opuesto(self, etiqueta_v: str, arista_str: str) -> "Vertice":
        """
        Retorna el vértice opuesto a v en la arista e (expresada como 'A-B').
        """
        v = self._get_vertice(etiqueta_v)
        u_et, w_et = self._parsear_arista_str(arista_str)
        u = self._get_vertice(u_et)
        w = self._get_vertice(w_et)
        for a in self._aristas:
            if (a.u == u and a.v == w) or (a.u == w and a.v == u):
                return self._opuesto_obj(v, a)
        raise ValueError(f"La arista '{arista_str}' no existe en el grafo.")

    def esAdyacente(self, etiqueta_v: str, etiqueta_w: str) -> bool:
        """Retorna True si v y w comparten una arista."""
        v = self._get_vertice(etiqueta_v)
        w = self._get_vertice(etiqueta_w)
        for a in self._adyacencia[v]:
            if self._opuesto_obj(v, a) == w:
                return True
        return False

    # ── ③ Operaciones posicionales ──────────────────────────
    def tamaño(self) -> int:
        """Retorna el número total de elementos (vértices + aristas)."""
        return self.numVertices() + self.numAristas()

    def estaVacio(self) -> bool:
        """Retorna True si el grafo no contiene vértices."""
        return self.numVertices() == 0

    def elementos(self) -> list:
        """Retorna lista de todos los elementos almacenados en vértices y aristas."""
        elems = [v.elemento for v in self._vertices.values()]
        elems += [a.elemento for a in self._aristas]
        return elems

    def posiciones(self) -> list:
        """Retorna una lista de índices posicionales de los vértices."""
        return list(range(len(self._vertices)))

    def reemplazar(self, etiqueta_vieja: str, etiqueta_nueva: str) -> str:
        """
        Reemplaza el elemento del vértice en posición p por r.
        Retorna el elemento anterior.
        """
        etiqueta_vieja = etiqueta_vieja.strip().upper()
        etiqueta_nueva = etiqueta_nueva.strip().upper()
        if etiqueta_vieja not in self._vertices:
            raise ValueError(f"El vértice '{etiqueta_vieja}' no existe.")
        if etiqueta_nueva in self._vertices and etiqueta_nueva != etiqueta_vieja:
            raise ValueError(f"Ya existe un vértice con la etiqueta '{etiqueta_nueva}'.")

        v = self._vertices.pop(etiqueta_vieja)
        viejo = v.elemento
        v.etiqueta = etiqueta_nueva
        v.elemento = etiqueta_nueva
        self._vertices[etiqueta_nueva] = v

        # Actualizar el campo 'elemento' de las aristas afectadas
        for a in self._aristas:
            a.elemento = f"{a.u.etiqueta}-{a.v.etiqueta}"

        return viejo

    def intercambiar(self, etiqueta_p: str, etiqueta_q: str):
        """Intercambia los elementos almacenados en dos vértices p y q."""
        etiqueta_p = etiqueta_p.strip().upper()
        etiqueta_q = etiqueta_q.strip().upper()
        if etiqueta_p not in self._vertices:
            raise ValueError(f"El vértice '{etiqueta_p}' no existe.")
        if etiqueta_q not in self._vertices:
            raise ValueError(f"El vértice '{etiqueta_q}' no existe.")

        vp = self._vertices[etiqueta_p]
        vq = self._vertices[etiqueta_q]

        # Intercambiar las etiquetas internas
        vp.etiqueta, vq.etiqueta = vq.etiqueta, vp.etiqueta
        vp.elemento, vq.elemento = vq.elemento, vp.elemento

        # Actualizar el diccionario de vértices
        self._vertices[etiqueta_p] = vq
        self._vertices[etiqueta_q] = vp

        # Refrescar elementos de aristas
        for a in self._aristas:
            a.elemento = f"{a.u.etiqueta}-{a.v.etiqueta}"

    # ── Modificación del grafo ─────────────────────────────
    def agregarVertice(self, etiqueta: str) -> Vertice:
        """Agrega un vértice nuevo al grafo."""
        etiqueta = etiqueta.strip().upper()
        if not etiqueta:
            raise ValueError("La etiqueta no puede estar vacía.")
        if etiqueta in self._vertices:
            raise ValueError(f"El vértice '{etiqueta}' ya existe.")

        v = Vertice(etiqueta)
        self._vertices[etiqueta] = v
        self._adyacencia[v] = []
        return v

    def agregarArista(self, et_u: str, et_v: str) -> Arista:
        """Agrega una arista entre los vértices con etiquetas et_u y et_v."""
        u = self._get_vertice(et_u.strip().upper())
        v = self._get_vertice(et_v.strip().upper())

        if u == v:
            raise ValueError("No se permiten auto-lazos.")

        # Verificar duplicado
        for a in self._aristas:
            if (a.u == u and a.v == v) or (a.u == v and a.v == u):
                raise ValueError(f"La arista '{et_u}-{et_v}' ya existe.")

        arista = Arista(u, v)
        self._aristas.append(arista)
        self._adyacencia[u].append(arista)
        self._adyacencia[v].append(arista)
        return arista

    def eliminarVertice(self, etiqueta: str):
        """Elimina un vértice y todas sus aristas incidentes."""
        v = self._get_vertice(etiqueta)
        for a in list(self._adyacencia[v]):
            op = self._opuesto_obj(v, a)
            self._adyacencia[op].remove(a)
            self._aristas.remove(a)
        del self._adyacencia[v]
        del self._vertices[etiqueta]

    def eliminarArista(self, et_u: str, et_v: str):
        """Elimina la arista que conecta et_u y et_v."""
        u = self._get_vertice(et_u.strip().upper())
        v = self._get_vertice(et_v.strip().upper())
        for a in self._aristas:
            if (a.u == u and a.v == v) or (a.u == v and a.v == u):
                self._aristas.remove(a)
                self._adyacencia[u].remove(a)
                self._adyacencia[v].remove(a)
                return
        raise ValueError(f"La arista '{et_u}-{et_v}' no existe.")

    # ── Auxiliares privados ────────────────────────────────
    def _get_vertice(self, etiqueta: str) -> Vertice:
        etiqueta = etiqueta.strip().upper()
        if etiqueta not in self._vertices:
            raise ValueError(f"El vértice '{etiqueta}' no existe en el grafo.")
        return self._vertices[etiqueta]

    def _opuesto_obj(self, v: Vertice, arista: Arista) -> Vertice:
        if arista.u == v:
            return arista.v
        elif arista.v == v:
            return arista.u
        raise ValueError(f"El vértice {v} no es extremo de {arista}.")

    def _parsear_arista_str(self, arista_str: str):
        """Parsea 'A-B' y retorna ('A', 'B'). Lanza ValueError si el formato es incorrecto."""
        partes = arista_str.strip().split("-")
        if len(partes) != 2 or not partes[0].strip() or not partes[1].strip():
            raise ValueError(f"Formato de arista inválido: '{arista_str}'. Use 'A-B'.")
        return partes[0].strip().upper(), partes[1].strip().upper()


# ─────────────────────────────────────────────────────────────
#  CLASE: Interfaz (GUI Tkinter)
# ─────────────────────────────────────────────────────────────
class Interfaz:
    """
    Interfaz gráfica completa para el TDA Grafo.
    Panel de controles + Canvas de visualización + Área de resultados.
    """

    # ── Paleta de colores ──────────────────────────────────
    BG        = "#0F0F1A"
    PANEL_BG  = "#161625"
    ACCENT    = "#7C3AED"
    ACCENT2   = "#10B981"
    ACCENT3   = "#F59E0B"
    TEXT      = "#E2E8F0"
    TEXT_DIM  = "#94A3B8"
    BORDER    = "#2D2D4E"
    ERROR     = "#EF4444"
    SUCCESS   = "#10B981"
    NODE_CLR  = "#7C3AED"
    CANVAS_BG = "#0D0D1F"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.grafo = Grafo()
        self._node_items = {}       # etiqueta -> oval id en canvas
        self._node_text_items = {}  # etiqueta -> text id en canvas

        self._configurar_ventana()
        self._crear_ui()

    # ── Configuración inicial ──────────────────────────────
    def _configurar_ventana(self):
        self.root.title("TDA Grafo — Visualizador Interactivo")
        self.root.geometry("1300x820")
        self.root.minsize(1000, 680)
        self.root.configure(bg=self.BG)

    # ── Construcción de la UI ──────────────────────────────
    def _crear_ui(self):
        self._crear_header()
        main = tk.Frame(self.root, bg=self.BG)
        main.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self._crear_panel_izquierdo(main)
        self._crear_panel_derecho(main)

    def _crear_header(self):
        h = tk.Frame(self.root, bg=self.ACCENT, height=52)
        h.pack(fill="x")
        h.pack_propagate(False)
        tk.Label(h, text="⬡  TDA GRAFO  —  Visualizador Interactivo",
                 bg=self.ACCENT, fg="white",
                 font=("Courier New", 15, "bold"),
                 anchor="w", padx=18).pack(side="left", fill="y")
        tk.Label(h, text="Python · Tkinter · Lista de Adyacencia",
                 bg=self.ACCENT, fg="#C4B5FD",
                 font=("Courier New", 9),
                 anchor="e", padx=18).pack(side="right", fill="y")

    def _crear_panel_izquierdo(self, parent):
        frame = tk.Frame(parent, bg=self.PANEL_BG, width=310)
        frame.pack(side="left", fill="y", padx=(0, 8))
        frame.pack_propagate(False)

        # Scrollable interior
        canvas_scroll = tk.Canvas(frame, bg=self.PANEL_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas_scroll.yview,
                                 bg=self.BORDER, troughcolor=self.PANEL_BG)
        canvas_scroll.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas_scroll.pack(side="left", fill="both", expand=True)

        interior = tk.Frame(canvas_scroll, bg=self.PANEL_BG)
        canvas_scroll.create_window((0, 0), window=interior, anchor="nw")

        def on_configure(e):
            canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
        interior.bind("<Configure>", on_configure)

        self._poblar_panel(interior)

    def _poblar_panel(self, frame):
        tk.Label(frame, text="OPERACIONES", bg=self.PANEL_BG, fg=self.ACCENT,
                 font=("Courier New", 11, "bold"), anchor="w", padx=14, pady=10
                 ).pack(fill="x")
        self._sep(frame)

        # ── Sección Vértices
        self._label_sec(frame, "① VÉRTICES")
        self.e_vertice = self._entry(frame, "Etiqueta del vértice (ej: A)")
        self._btn(frame, "＋  Agregar Vértice",   self._agregar_vertice,  self.ACCENT)
        self._btn(frame, "－  Eliminar Vértice",  self._eliminar_vertice, "#64748B")
        self._btn(frame, "◉  Mostrar Vértices",   self._mostrar_vertices)
        self._sep(frame)

        # ── Sección Aristas
        self._label_sec(frame, "② ARISTAS")
        self.e_arista = self._entry(frame, "Arista: A-B  (origen-destino)")
        self._btn(frame, "＋  Agregar Arista",    self._agregar_arista,   self.ACCENT)
        self._btn(frame, "－  Eliminar Arista",   self._eliminar_arista,  "#64748B")
        self._btn(frame, "◉  Mostrar Aristas",    self._mostrar_aristas)
        self._sep(frame)

        # ── Consultas
        self._label_sec(frame, "③ CONSULTAS")
        self._btn(frame, "📊  Info General", self._info_general, self.ACCENT2)

        tk.Label(frame, text="Vértice V para consultar:",
                 bg=self.PANEL_BG, fg=self.TEXT_DIM,
                 font=("Courier New", 8), anchor="w", padx=14).pack(fill="x", pady=(6,0))
        self.e_v = self._entry(frame, "Vértice V (ej: A)")

        self._btn(frame, "⊕  Grado del vértice",       self._grado,            self.ACCENT3)
        self._btn(frame, "↔  Vértices Adyacentes",      self._adyacentes,       self.ACCENT3)
        self._btn(frame, "⊂  Aristas Incidentes",       self._incidentes,       self.ACCENT3)

        tk.Label(frame, text="Vértice W  (o arista 'A-B' para opuesto):",
                 bg=self.PANEL_BG, fg=self.TEXT_DIM,
                 font=("Courier New", 8), anchor="w", padx=14, wraplength=270
                 ).pack(fill="x", pady=(6,0))
        self.e_w = self._entry(frame, "Vértice W  o  A-B")

        self._btn(frame, "🔗  ¿Son Adyacentes V-W?",   self._es_adyacente,     self.ACCENT3)
        self._btn(frame, "↩  Opuesto(V, arista A-B)",   self._opuesto,          self.ACCENT3)
        self._btn(frame, "🔎  Vértices Finales(A-B)",   self._vertices_finales,  self.ACCENT3)
        self._sep(frame)

        # ── Posicional
        self._label_sec(frame, "④ POSICIONAL")

        tk.Label(frame, text="Reemplazar:", bg=self.PANEL_BG, fg=self.TEXT_DIM,
                 font=("Courier New", 8), anchor="w", padx=14).pack(fill="x", pady=(4,0))
        fr1 = tk.Frame(frame, bg=self.PANEL_BG)
        fr1.pack(fill="x", padx=14, pady=2)
        self.e_rep_old = self._entry_inline(fr1, "Viejo")
        self.e_rep_new = self._entry_inline(fr1, "Nuevo")
        self._btn(frame, "✏  Reemplazar(p, nuevo)",    self._reemplazar,        "#0EA5E9")

        tk.Label(frame, text="Intercambiar:", bg=self.PANEL_BG, fg=self.TEXT_DIM,
                 font=("Courier New", 8), anchor="w", padx=14).pack(fill="x", pady=(4,0))
        fr2 = tk.Frame(frame, bg=self.PANEL_BG)
        fr2.pack(fill="x", padx=14, pady=2)
        self.e_int_p = self._entry_inline(fr2, "Vértice P")
        self.e_int_q = self._entry_inline(fr2, "Vértice Q")
        self._btn(frame, "⇄  Intercambiar(p, q)",       self._intercambiar,      "#0EA5E9")
        self._btn(frame, "📐  Tamaño / Vacío / Posic.",  self._info_posicional,   "#0EA5E9")
        self._sep(frame)

        self._btn(frame, "🗑  Limpiar Grafo",            self._limpiar_grafo,     self.ERROR)

    def _crear_panel_derecho(self, parent):
        frame = tk.Frame(parent, bg=self.BG)
        frame.pack(side="left", fill="both", expand=True)

        # Canvas del grafo
        cv_frame = tk.Frame(frame, bg=self.BORDER, bd=0)
        cv_frame.pack(fill="both", expand=True, pady=(0,8))

        self.canvas = tk.Canvas(cv_frame, bg=self.CANVAS_BG, highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill="both", expand=True, padx=1, pady=1)

        tk.Label(cv_frame, text="Canvas del grafo — los nodos se distribuyen en círculo automáticamente",
                 bg=self.CANVAS_BG, fg="#334155", font=("Courier New", 8)
                 ).place(relx=0.5, rely=0.97, anchor="center")

        # Área de resultados
        res = tk.Frame(frame, bg=self.PANEL_BG, height=195)
        res.pack(fill="x")
        res.pack_propagate(False)

        hdr = tk.Frame(res, bg=self.PANEL_BG)
        hdr.pack(fill="x", padx=10, pady=(8,4))
        tk.Label(hdr, text="▸  RESULTADO", bg=self.PANEL_BG, fg=self.ACCENT,
                 font=("Courier New", 10, "bold")).pack(side="left")
        tk.Button(hdr, text="Limpiar salida", bg=self.BORDER, fg=self.TEXT_DIM,
                  font=("Courier New", 8), relief="flat", bd=0, cursor="hand2",
                  command=self._limpiar_salida,
                  activebackground=self.ACCENT, activeforeground="white", padx=8
                  ).pack(side="right")

        tf = tk.Frame(res, bg=self.PANEL_BG)
        tf.pack(fill="both", expand=True, padx=10, pady=(0,8))

        self.out = tk.Text(tf, bg="#090912", fg=self.TEXT,
                           font=("Courier New", 10), relief="flat", bd=0,
                           state="disabled", wrap="word",
                           insertbackground=self.ACCENT, selectbackground=self.ACCENT)
        self.out.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(tf, command=self.out.yview,
                          bg=self.BORDER, troughcolor=self.PANEL_BG, relief="flat")
        sb.pack(side="right", fill="y")
        self.out.configure(yscrollcommand=sb.set)

        # Tags de color
        self.out.tag_config("ok",    foreground=self.SUCCESS)
        self.out.tag_config("err",   foreground=self.ERROR)
        self.out.tag_config("info",  foreground=self.ACCENT3)
        self.out.tag_config("title", foreground=self.ACCENT, font=("Courier New", 10, "bold"))

        self._write("Bienvenido al TDA Grafo 🔷\n", "title")
        self._write("Agrega vértices y aristas con el panel izquierdo.\n", "info")

    # ── Widgets helpers ────────────────────────────────────
    def _sep(self, p):
        tk.Frame(p, bg=self.BORDER, height=1).pack(fill="x", pady=6)

    def _label_sec(self, p, txt):
        tk.Label(p, text=txt, bg=self.PANEL_BG, fg=self.TEXT_DIM,
                 font=("Courier New", 9, "bold"), anchor="w", padx=14, pady=4
                 ).pack(fill="x")

    def _entry(self, parent, placeholder):
        entry = tk.Entry(parent, bg="#1E1E35", fg=self.TEXT,
                         font=("Courier New", 10), relief="flat", bd=0,
                         insertbackground=self.ACCENT, selectbackground=self.ACCENT)
        entry.pack(fill="x", padx=14, pady=3, ipady=6)
        entry.insert(0, placeholder)
        entry.config(fg=self.TEXT_DIM)

        def fi(e):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(fg=self.TEXT)

        def fo(e):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=self.TEXT_DIM)

        entry.bind("<FocusIn>", fi)
        entry.bind("<FocusOut>", fo)
        entry._placeholder = placeholder
        return entry

    def _entry_inline(self, parent, placeholder):
        entry = tk.Entry(parent, bg="#1E1E35", fg=self.TEXT,
                         font=("Courier New", 9), relief="flat", bd=0,
                         insertbackground=self.ACCENT, width=12)
        entry.pack(side="left", fill="x", expand=True, padx=2, ipady=5)
        entry.insert(0, placeholder)
        entry.config(fg=self.TEXT_DIM)

        def fi(e):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(fg=self.TEXT)

        def fo(e):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=self.TEXT_DIM)

        entry.bind("<FocusIn>", fi)
        entry.bind("<FocusOut>", fo)
        entry._placeholder = placeholder
        return entry

    def _btn(self, parent, texto, cmd, color=None):
        color = color or "#2D2D4E"
        tk.Button(parent, text=texto, bg=color, fg="white",
                  font=("Courier New", 9), relief="flat", bd=0, cursor="hand2",
                  command=cmd, activebackground=self.ACCENT, activeforeground="white",
                  anchor="w", padx=12, pady=6
                  ).pack(fill="x", padx=14, pady=2)

    def _val(self, entry):
        """Obtiene el valor de un Entry, ignorando su placeholder."""
        v = entry.get().strip()
        ph = getattr(entry, "_placeholder", "")
        return "" if v == ph else v

    # ── Salida de texto ────────────────────────────────────
    def _write(self, txt, tag=None):
        self.out.configure(state="normal")
        if tag:
            self.out.insert("end", txt, tag)
        else:
            self.out.insert("end", txt)
        self.out.see("end")
        self.out.configure(state="disabled")

    def _line(self):
        self._write("─" * 52 + "\n", "title")

    def _limpiar_salida(self):
        self.out.configure(state="normal")
        self.out.delete("1.0", "end")
        self.out.configure(state="disabled")

    # ── Handlers de operaciones ────────────────────────────
    def _agregar_vertice(self):
        et = self._val(self.e_vertice)
        if not et:
            self._write("⚠ Ingresa una etiqueta para el vértice.\n", "err"); return
        try:
            self.grafo.agregarVertice(et)
            self._write(f"✔ Vértice '{et.upper()}' agregado.\n", "ok")
            self.e_vertice.delete(0, "end")
            self._redibujar()
        except ValueError as e:
            self._write(f"✘ {e}\n", "err")

    def _eliminar_vertice(self):
        et = self._val(self.e_vertice)
        if not et:
            self._write("⚠ Ingresa la etiqueta del vértice a eliminar.\n", "err"); return
        try:
            self.grafo.eliminarVertice(et.upper())
            self._write(f"✔ Vértice '{et.upper()}' eliminado.\n", "ok")
            self.e_vertice.delete(0, "end")
            self._redibujar()
        except ValueError as e:
            self._write(f"✘ {e}\n", "err")

    def _agregar_arista(self):
        raw = self._val(self.e_arista)
        if not raw:
            self._write("⚠ Ingresa una arista con formato A-B.\n", "err"); return
        try:
            u, v = self.grafo._parsear_arista_str(raw)
            self.grafo.agregarArista(u, v)
            self._write(f"✔ Arista '{u}-{v}' agregada.\n", "ok")
            self.e_arista.delete(0, "end")
            self._redibujar()
        except ValueError as e:
            self._write(f"✘ {e}\n", "err")

    def _eliminar_arista(self):
        raw = self._val(self.e_arista)
        if not raw:
            self._write("⚠ Ingresa la arista a eliminar (A-B).\n", "err"); return
        try:
            u, v = self.grafo._parsear_arista_str(raw)
            self.grafo.eliminarArista(u, v)
            self._write(f"✔ Arista '{u}-{v}' eliminada.\n", "ok")
            self.e_arista.delete(0, "end")
            self._redibujar()
        except ValueError as e:
            self._write(f"✘ {e}\n", "err")

    def _mostrar_vertices(self):
        self._line()
        self._write("VÉRTICES DEL GRAFO\n", "title")
        vs = self.grafo.vertices()
        if not vs:
            self._write("  (sin vértices)\n", "info")
        else:
            self._write(f"  numVertices() = {len(vs)}\n", "ok")
            for v in vs:
                self._write(f"  • {v.etiqueta}\n")
        self._line()

    def _mostrar_aristas(self):
        self._line()
        self._write("ARISTAS DEL GRAFO\n", "title")
        ars = self.grafo.aristas()
        if not ars:
            self._write("  (sin aristas)\n", "info")
        else:
            self._write(f"  numAristas() = {len(ars)}\n", "ok")
            for a in ars:
                self._write(f"  • {a.u.etiqueta}  ⟷  {a.v.etiqueta}\n")
        self._line()

    def _info_general(self):
        self._line()
        self._write("INFO GENERAL\n", "title")
        self._write(f"  numVertices() = {self.grafo.numVertices()}\n", "ok")
        self._write(f"  numAristas()  = {self.grafo.numAristas()}\n", "ok")
        vs  = [v.etiqueta for v in self.grafo.vertices()]
        ars = [f"{a.u.etiqueta}-{a.v.etiqueta}" for a in self.grafo.aristas()]
        self._write(f"  vertices()    = {vs}\n")
        self._write(f"  aristas()     = {ars}\n")
        self._line()

    def _grado(self):
        v = self._val(self.e_v)
        if not v:
            self._write("⚠ Ingresa el vértice V.\n", "err"); return
        try:
            self._write(f"  grado('{v.upper()}') = {self.grafo.grado(v)}\n", "ok")
        except ValueError as e:
            self._write(f"✘ {e}\n", "err")

    def _adyacentes(self):
        v = self._val(self.e_v)
        if not v:
            self._write("⚠ Ingresa el vértice V.\n", "err"); return
        try:
            ady = [x.etiqueta for x in self.grafo.verticesAdyacentes(v)]
            self._write(f"  verticesAdyacentes('{v.upper()}') = {ady}\n", "ok")
        except ValueError as e:
            self._write(f"✘ {e}\n", "err")

    def _incidentes(self):
        v = self._val(self.e_v)
        if not v:
            self._write("⚠ Ingresa el vértice V.\n", "err"); return
        try:
            ars = [f"{a.u.etiqueta}-{a.v.etiqueta}" for a in self.grafo.aristasIncidentes(v)]
            self._write(f"  aristasIncidentes('{v.upper()}') = {ars}\n", "ok")
        except ValueError as e:
            self._write(f"✘ {e}\n", "err")

    def _es_adyacente(self):
        v = self._val(self.e_v)
        w = self._val(self.e_w)
        if not v or not w:
            self._write("⚠ Ingresa los vértices V y W.\n", "err"); return
        try:
            res = self.grafo.esAdyacente(v, w)
            tag = "ok" if res else "err"
            self._write(f"  esAdyacente('{v.upper()}', '{w.upper()}') = {res}\n", tag)
        except ValueError as e:
            self._write(f"✘ {e}\n", "err")

    def _opuesto(self):
        v = self._val(self.e_v)
        ar = self._val(self.e_w)
        if not v or not ar:
            self._write("⚠ Ingresa V y la arista A-B en el campo W.\n", "err"); return
        try:
            op = self.grafo.opuesto(v, ar)
            self._write(f"  opuesto('{v.upper()}', '{ar.upper()}') = '{op.etiqueta}'\n", "ok")
        except ValueError as e:
            self._write(f"✘ {e}\n", "err")

    def _vertices_finales(self):
        ar = self._val(self.e_w)
        if not ar:
            self._write("⚠ Ingresa la arista A-B en el campo W.\n", "err"); return
        try:
            u, v = self.grafo.verticesFinales(ar)
            self._write(f"  verticesFinales('{ar.upper()}') = ('{u.etiqueta}', '{v.etiqueta}')\n", "ok")
        except ValueError as e:
            self._write(f"✘ {e}\n", "err")

    def _reemplazar(self):
        viejo = self._val(self.e_rep_old)
        nuevo = self._val(self.e_rep_new)
        if not viejo or not nuevo:
            self._write("⚠ Ingresa el vértice viejo y el nuevo.\n", "err"); return
        try:
            ant = self.grafo.reemplazar(viejo, nuevo)
            self._write(f"  reemplazar('{viejo.upper()}','{nuevo.upper()}') → ant='{ant}'\n", "ok")
            self._redibujar()
        except ValueError as e:
            self._write(f"✘ {e}\n", "err")

    def _intercambiar(self):
        p = self._val(self.e_int_p)
        q = self._val(self.e_int_q)
        if not p or not q:
            self._write("⚠ Ingresa los vértices P y Q.\n", "err"); return
        try:
            self.grafo.intercambiar(p, q)
            self._write(f"  intercambiar('{p.upper()}','{q.upper()}') → elementos intercambiados.\n", "ok")
            self._redibujar()
        except ValueError as e:
            self._write(f"✘ {e}\n", "err")

    def _info_posicional(self):
        self._line()
        self._write("OPERACIONES POSICIONALES\n", "title")
        self._write(f"  tamaño()    = {self.grafo.tamaño()}\n",     "ok")
        self._write(f"  estaVacio() = {self.grafo.estaVacio()}\n",  "ok")
        self._write(f"  elementos() = {self.grafo.elementos()}\n")
        self._write(f"  posiciones()= {self.grafo.posiciones()}\n")
        self._line()

    def _limpiar_grafo(self):
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar todos los vértices y aristas?"):
            self.grafo = Grafo()
            self._redibujar()
            self._write("🗑 Grafo limpiado.\n", "info")

    # ── Visualización en Canvas ────────────────────────────
    def _redibujar(self):
        """Redibuja el grafo completo: nodos en círculo + aristas."""
        self.canvas.delete("all")
        self._node_items.clear()
        self._node_text_items.clear()

        vertices = self.grafo.vertices()
        if not vertices:
            return

        # Dimensiones actuales del canvas
        w = self.canvas.winfo_width() or 700
        h = self.canvas.winfo_height() or 420

        # ── Cuadrícula de fondo ──
        paso, gc = 40, "#13132A"
        for x in range(0, w + paso, paso):
            self.canvas.create_line(x, 0, x, h, fill=gc)
        for y in range(0, h + paso, paso):
            self.canvas.create_line(0, y, w, y, fill=gc)

        # ── Calcular posiciones en círculo ──
        n = len(vertices)
        cx, cy = w / 2, h / 2
        R_circle = min(w, h) * 0.36
        for i, v in enumerate(vertices):
            ang = (2 * math.pi * i / n) - (math.pi / 2)
            v.x = cx + R_circle * math.cos(ang)
            v.y = cy + R_circle * math.sin(ang)

        # ── Dibujar aristas ──
        for a in self.grafo.aristas():
            x1, y1 = a.u.x, a.u.y
            x2, y2 = a.v.x, a.v.y
            self.canvas.create_line(x1, y1, x2, y2, fill="#2D2D6E", width=2)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            # Etiqueta de arista desplazada levemente para no solapar el segmento
            self.canvas.create_text(mx + 4, my - 8,
                                    text=f"{a.u.etiqueta}–{a.v.etiqueta}",
                                    fill="#4B5563", font=("Courier New", 7))

        # ── Dibujar nodos ──
        R = 22
        for v in vertices:
            # Sombra suave
            self.canvas.create_oval(v.x-R+3, v.y-R+3, v.x+R+3, v.y+R+3,
                                    fill="#0A0A14", outline="")
            # Círculo del nodo
            item = self.canvas.create_oval(v.x-R, v.y-R, v.x+R, v.y+R,
                                           fill=self.NODE_CLR, outline="#A855F7", width=2)
            # Etiqueta del nodo
            txt = self.canvas.create_text(v.x, v.y, text=v.etiqueta,
                                          fill="white", font=("Courier New", 11, "bold"))
            self._node_items[v.etiqueta] = item
            self._node_text_items[v.etiqueta] = txt


# ─────────────────────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────
def main():
    root = tk.Tk()
    app = Interfaz(root)

    # Redibujar grafo cuando cambie el tamaño de la ventana
    def on_resize(event):
        if event.widget == root:
            app._redibujar()

    root.bind("<Configure>", on_resize)
    root.mainloop()


if __name__ == "__main__":
    main()
