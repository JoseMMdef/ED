import tkinter as tk
from tkinter import messagebox

class PilaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pila Gráfica en Python")

        # La pila como lista
        self.pila = []

        # Entrada de texto
        self.entry = tk.Entry(root, width=20)
        self.entry.pack(pady=5)

        # Botones principales
        self.push_button = tk.Button(root, text="Push (Apilar)", command=self.push)
        self.push_button.pack(pady=5)

        self.pop_button = tk.Button(root, text="Pop (Desapilar)", command=self.pop)
        self.pop_button.pack(pady=5)

        # Botones nuevos
        self.clear_button = tk.Button(root, text="Vaciar pila", command=self.vaciar)
        self.clear_button.pack(pady=5)

        self.fill_button = tk.Button(root, text="Llenar automáticamente", command=self.llenar_auto)
        self.fill_button.pack(pady=5)

        # Canvas para dibujar la pila
        self.canvas = tk.Canvas(root, width=200, height=300, bg="white")
        self.canvas.pack(pady=10)

    def actualizar_pila(self):
        # Limpiar el canvas
        self.canvas.delete("all")

        # Dibujar cada elemento como un rectángulo
        base_y = 280  # posición inicial (abajo del canvas)
        altura = 30   # altura de cada bloque
        ancho = 150   # ancho de cada bloque

        for i, elemento in enumerate(reversed(self.pila)):
            x1 = 25
            y1 = base_y - i * altura
            x2 = x1 + ancho
            y2 = y1 - altura

            # Rectángulo
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue", outline="black")
            # Texto dentro del rectángulo
            self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(elemento))

    def push(self):
        valor = self.entry.get()
        if valor:
            self.pila.append(valor)
            self.entry.delete(0, tk.END)
            self.actualizar_pila()
        else:
            messagebox.showwarning("Entrada vacía", "Por favor ingresa un valor.")

    def pop(self):
        if self.pila:
            valor = self.pila.pop()
            messagebox.showinfo("Elemento desapilado", f"Se desapiló: {valor}")
            self.actualizar_pila()
        else:
            messagebox.showwarning("Pila vacía", "No hay elementos para desapilar.")

    def vaciar(self):
        if self.pila:
            self.pila.clear()
            self.actualizar_pila()
            messagebox.showinfo("Pila vaciada", "Todos los elementos fueron eliminados.")
        else:
            messagebox.showwarning("Pila vacía", "La pila ya está vacía.")

    def llenar_auto(self):
        # Ejemplo: llenar con números del 1 al 5
        self.pila = ["Elemento 1", "Elemento 2", "Elemento 3", "Elemento 4", "Elemento 5"]
        self.actualizar_pila()
        messagebox.showinfo("Pila llena", "Se agregaron automáticamente 5 elementos.")

# Programa principal
if __name__ == "__main__":
    root = tk.Tk()
    app = PilaGUI(root)
    root.mainloop()
