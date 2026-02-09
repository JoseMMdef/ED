# ============================================================
# Programa desarrollado con apoyo de Inteligencia Artificial (ChatGPT)
# El estudiante revisa, comprende y modifica el código como parte
# de su aprendizaje académico.
# ============================================================

# ============================================================
# SISTEMA DE VENTAS POR DEPARTAMENTO (ARREGLO BIDIMENSIONAL)
# Filas = meses
# Columnas = departamentos
# ============================================================

# -----------------------------
# 1. DATOS BASE
# -----------------------------
meses = [
    "Enero","Febrero","Marzo","Abril","Mayo","Junio",
    "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
]

departamentos = ["Ropa","Deportes","Juguetería"]

# Matriz 12x3 llena de ceros
ventas = [[0 for _ in range(len(departamentos))] for _ in range(len(meses))]


# ============================================================
# 2. MÉTODO INSERTAR VENTA
# ============================================================
def insertar_venta():
    print("\n--- INSERTAR VENTA ---")
    
    mes = input("Ingresa el mes: ").capitalize()
    depto = input("Ingresa departamento (Ropa/Deportes/Juguetería): ").capitalize()
    
    if mes in meses and depto in departamentos:
        monto = float(input("Ingresa monto de venta: "))
        
        fila = meses.index(mes)
        col = departamentos.index(depto)
        
        ventas[fila][col] = monto
        print("Venta registrada correctamente")
    else:
        print("Mes o departamento inválido")


# ============================================================
# 3. MÉTODO BUSCAR VENTA
# ============================================================
def buscar_venta():
    print("\n--- BUSCAR VENTA ---")
    
    mes = input("Ingresa el mes: ").capitalize()
    depto = input("Ingresa departamento: ").capitalize()
    
    if mes in meses and depto in departamentos:
        fila = meses.index(mes)
        col = departamentos.index(depto)
        
        print(f"Venta en {mes} [{depto}]: {ventas[fila][col]}")
    else:
        print("Mes o departamento inválido")


# ============================================================
# 4. MÉTODO ELIMINAR VENTA
# ============================================================
def eliminar_venta():
    print("\n--- ELIMINAR VENTA ---")
    
    mes = input("Ingresa el mes: ").capitalize()
    depto = input("Ingresa departamento: ").capitalize()
    
    if mes in meses and depto in departamentos:
        fila = meses.index(mes)
        col = departamentos.index(depto)
        
        ventas[fila][col] = 0
        print("Venta eliminada correctamente")
    else:
        print("Mes o departamento inválido")


# ============================================================
# 5. MOSTRAR MATRIZ COMPLETA
# ============================================================
def mostrar_matriz():
    print("\n========== TABLA DE VENTAS ==========")
    print(f"{'Mes':<12}{'Ropa':<12}{'Deportes':<12}{'Juguetería':<12}")
    
    for i in range(len(meses)):
        print(f"{meses[i]:<12}{ventas[i][0]:<12}{ventas[i][1]:<12}{ventas[i][2]:<12}")


# ============================================================
# 6. MENÚ PRINCIPAL
# ============================================================
while True:
    print("\n====== SISTEMA DE VENTAS ======")
    print("1. Insertar venta")
    print("2. Buscar venta")
    print("3. Eliminar venta")
    print("4. Mostrar tabla completa")
    print("5. Salir")
    
    opcion = input("Selecciona una opción: ")
    
    if opcion == "1":
        insertar_venta()
    elif opcion == "2":
        buscar_venta()
    elif opcion == "3":
        eliminar_venta()
    elif opcion == "4":
        mostrar_matriz()
    elif opcion == "5":
        print("Saliendo del sistema...")
        break
    else:
        print("Opción inválida")
