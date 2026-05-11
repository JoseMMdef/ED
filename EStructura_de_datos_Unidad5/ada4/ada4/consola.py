import ordenamiento_interno as interno
import ordenamiento_externo as externo

class InterfazOrdenamiento:
    def __init__(self, modo: str = "interno"):
        self.modo = modo

    def cargar_datos(self, archivo: str) -> list:
        with open(archivo, "r", encoding="utf-8") as f:
            datos = [line.strip() for line in f if line.strip()]
        try:
            datos = [int(x) for x in datos]
        except ValueError:
            pass
        return datos

    def ordenar(self, datos: list, algoritmo: str) -> list:
        if self.modo == "interno":
            funcion = getattr(interno, algoritmo, None)
        else:
            funcion = getattr(externo, algoritmo, None)

        if funcion is None:
            raise ValueError(f"Algoritmo {algoritmo} no encontrado en {self.modo}.")
        return funcion(datos)


def menu():
    print("=== Interfaz de Ordenamiento ===")
    modo = input("Elige modo (interno/externo): ").strip().lower()
    interfaz = InterfazOrdenamiento(modo=modo)

    archivo = input("Nombre del archivo con datos: ").strip()
    datos = interfaz.cargar_datos(archivo)

    print("Algoritmos disponibles: bubble_sort, insertion_sort, selection_sort, shell_sort, quick_sort, heap_sort, radix_sort")
    algoritmo = input("Elige algoritmo: ").strip()

    resultado = interfaz.ordenar(datos, algoritmo)
    print("Resultado ordenado:", resultado)


if __name__ == "__main__":
    menu()
