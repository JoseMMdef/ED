import tkinter as tk
import time

class TorreDeHanoiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Torre de Hanoi - Interfaz Gráfica")

        # Entrada para número de discos
        self.label_entry = tk.Label(root, text="Número de discos:")
        self.label_entry.pack()
        self.entry_discos = tk.Entry(root, width=5)
        self.entry_discos.pack(pady=5)

        # Botón para iniciar
        self.start_button = tk.Button(root, text="Resolver", command=self.iniciar)
        self.start_button.pack(pady=10)

        # Canvas para dibujar las torres
        self.canvas = tk.Canvas(root, width=600, height=300, bg="white")
        self.canvas.pack()

        # Etiqueta para mostrar resultados
        self.result_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
        self.result_label.pack(pady=10)

        # Variables de control
        self.torres_x = [100, 300, 500]
        self.base_y = 250
        self.altura_disco = 20
        self.torres = []
        self.num_discos = 0
        self.movimientos = 0

    def dibujar_torres(self):
        self.canvas.delete("all")
        # Dibujar postes
        for x in self.torres_x:
            self.canvas.create_line(x, self.base_y, x, 100, width=4)

        # Dibujar discos
        colores = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "cyan"]
        for i, torre in enumerate(self.torres):
            for j, disco in enumerate(torre):
                ancho = disco * 20
                x1 = self.torres_x[i] - ancho // 2
                y1 = self.base_y - (j+1) * self.altura_disco
                x2 = self.torres_x[i] + ancho // 2
                y2 = y1 + self.altura_disco
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=colores[disco % len(colores)],
                                             outline="black")
        self.root.update()

    def mover(self, n, origen, destino, auxiliar):
        if n == 1:
            disco = self.torres[origen].pop()
            self.torres[destino].append(disco)
            self.movimientos += 1
            self.dibujar_torres()
            time.sleep(0.2)
        else:
            self.mover(n-1, origen, auxiliar, destino)
            self.mover(1, origen, destino, auxiliar)
            self.mover(n-1, auxiliar, destino, origen)

    def iniciar(self):
        try:
            self.num_discos = int(self.entry_discos.get())
        except ValueError:
            self.result_label.config(text="Por favor ingresa un número válido.")
            return

        # Inicializar torres
        self.torres = [list(range(self.num_discos, 0, -1)), [], []]
        self.movimientos = 0
        self.dibujar_torres()

        inicio = time.time()
        self.mover(self.num_discos, 0, 2, 1)
        fin = time.time()

        tiempo_total = fin - inicio
        self.result_label.config(
            text=f"Movimientos: {self.movimientos} | Tiempo: {tiempo_total:.4f} segundos"
        )

# Programa principal
if __name__ == "__main__":
    root = tk.Tk()
    app = TorreDeHanoiGUI(root)
    root.mainloop()
