class Pila:
    def __init__(self, capacidad=8):
        self.capacidad = capacidad
        self.elementos = []
    
    def push(self, valor):
        if len(self.elementos) >= self.capacidad:
            print(f"Error: Overflow al insertar {valor}")
        else:
            self.elementos.append(valor)
            print(f"Insertar {valor} -> Pila: {self.elementos}, TOPE: {len(self.elementos)}")
    
    def pop(self, etiqueta):
        if not self.elementos:
            print(f"Error: Underflow al eliminar {etiqueta}")
        else:
            eliminado = self.elementos.pop()
            print(f"Eliminar {etiqueta} (sale {eliminado}) -> Pila: {self.elementos}, TOPE: {len(self.elementos)}")

# Simulación de operaciones
pila = Pila()

pila.push("X")
pila.push("Y")
pila.pop("Z")
pila.pop("T")
pila.pop("U")
pila.push("V")
pila.push("W")
pila.pop("P")
pila.push("R")
