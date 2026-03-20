import tkinter as tk
import random

# ------------------------------
# Cola Circular
# ------------------------------
class ColaCircular:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.cola = [None] * capacidad
        self.frente = -1
        self.final = -1
        self.tamano = 0

    def esta_vacia(self):
        return self.tamano == 0

    def esta_llena(self):
        return self.tamano == self.capacidad

    def encolar(self, valor):
        if self.esta_llena():
            return False

        if self.frente == -1:
            self.frente = 0
            self.final = 0
        else:
            self.final = (self.final + 1) % self.capacidad

        self.cola[self.final] = valor
        self.tamano += 1
        return True

    def desencolar(self):
        if self.esta_vacia():
            return None

        valor = self.cola[self.frente]
        self.cola[self.frente] = None

        if self.frente == self.final:
            self.frente = -1
            self.final = -1
        else:
            self.frente = (self.frente + 1) % self.capacidad

        self.tamano -= 1
        return valor

    def obtener_elementos(self):
        elementos = []
        if self.esta_vacia():
            return elementos

        i = self.frente
        while True:
            elementos.append(self.cola[i])
            if i == self.final:
                break
            i = (i + 1) % self.capacidad

        return elementos


# ------------------------------
# Simulación
# ------------------------------
class SimulacionPeaje:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Peaje")

        self.simulando = False

        self.crear_menu_config()

    # --------------------------
    # Configuración inicial
    # --------------------------
    def crear_menu_config(self):
        self.limpiar_ventana()

        tk.Label(self.root, text="Configuración", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Número de carriles:").pack()
        self.entry_carriles = tk.Entry(self.root)
        self.entry_carriles.pack()

        tk.Label(self.root, text="Capacidad por carril:").pack()
        self.entry_capacidad = tk.Entry(self.root)
        self.entry_capacidad.pack()

        tk.Button(self.root, text="Iniciar Simulación", command=self.iniciar_simulacion).pack(pady=10)

    def iniciar_simulacion(self):
        try:
            num_carriles = int(self.entry_carriles.get())
            capacidad = int(self.entry_capacidad.get())
        except:
            return

        self.carriles = [ColaCircular(capacidad) for _ in range(num_carriles)]
        self.frames_carriles = []
        self.contador_autos = 1
        self.simulando = True

        self.crear_interfaz()

        self.actualizar()

    # --------------------------
    # Interfaz simulación
    # --------------------------
    def crear_interfaz(self):
        self.limpiar_ventana()

        tk.Label(self.root, text="Simulación de Peaje", font=("Arial", 16)).pack(pady=10)

        self.frame_principal = tk.Frame(self.root)
        self.frame_principal.pack()

        for i in range(len(self.carriles)):
            frame = tk.LabelFrame(self.frame_principal, text=f"Carril {i+1}", padx=10, pady=10)
            frame.grid(row=0, column=i, padx=10)
            self.frames_carriles.append(frame)

        self.info = tk.Label(self.root, text="")
        self.info.pack(pady=10)

        # Botón para modificar configuración
        tk.Button(self.root, text="Modificar Configuración", command=self.crear_menu_config).pack(pady=5)

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --------------------------
    # Lógica
    # --------------------------
    def asignar_carril(self):
        disponibles = [c for c in self.carriles if not c.esta_llena()]
        if not disponibles:
            return None
        return min(disponibles, key=lambda c: c.tamano)

    def llegada_vehiculo(self):
        carril = self.asignar_carril()
        if carril:
            carril.encolar(f"A{self.contador_autos}")
            self.contador_autos += 1
            return "Vehículo agregado"
        else:
            return "Todos los carriles llenos"

    def salida_vehiculo(self):
        carriles_no_vacios = [c for c in self.carriles if not c.esta_vacia()]
        if carriles_no_vacios:
            carril = random.choice(carriles_no_vacios)
            carril.desencolar()

    def actualizar_interfaz(self):
        for i, carril in enumerate(self.carriles):
            for widget in self.frames_carriles[i].winfo_children():
                widget.destroy()

            for auto in carril.obtener_elementos():
                tk.Label(self.frames_carriles[i], text=auto, bg="lightblue", width=8).pack(pady=2)

            tk.Label(self.frames_carriles[i], text=f"{carril.tamano}/{carril.capacidad}").pack()

    def actualizar(self):
        if not self.simulando:
            return

        mensaje = self.llegada_vehiculo()

        if random.random() < 0.5:
            self.salida_vehiculo()

        self.info.config(text=mensaje)
        self.actualizar_interfaz()

        self.root.after(1000, self.actualizar)


# ------------------------------
# Ejecutar
# ------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SimulacionPeaje(root)
    root.mainloop()