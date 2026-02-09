# ============================================================
# Programa desarrollado con apoyo de Inteligencia Artificial (ChatGPT)
# El estudiante revisa, comprende y modifica el código como parte
# de su aprendizaje académico.
# ============================================================


# ============================================================
# 1. LIBRERÍAS
# ============================================================
import random
import time


# ============================================================
# 2. VARIABLES EDITABLES (MODIFICA SOLO AQUÍ)
# ============================================================
alumnos = 5000
materias = 500

alumno_buscar = 900
materia_buscar = 24


# ============================================================
# ============================================================
# FORMA 1
# FILAS = MATERIAS
# COLUMNAS = ALUMNOS
# (Como en la primera tabla del profesor)
# ============================================================
# ============================================================

print("\n=========== FORMA 1: MATERIAS -> ALUMNOS ===========")

# ----- CREAR MATRIZ -----
inicio = time.time()

matriz1 = [
    [random.randint(0, 100) for _ in range(alumnos)]
    for _ in range(materias)
]

fin = time.time()
print(f"Tiempo generando matriz: {fin - inicio:.6f} segundos")


# ----- BUSCAR DATO -----
inicio = time.time()

valor1 = matriz1[materia_buscar-1][alumno_buscar-1]

fin = time.time()
tiempo_busqueda1 = fin - inicio

print(f"Valor encontrado: {valor1}")
print(f"Tiempo búsqueda forma 1: {tiempo_busqueda1:.10f} segundos")



# ============================================================
# ============================================================
# FORMA 2
# FILAS = ALUMNOS
# COLUMNAS = MATERIAS
# (Como en la segunda tabla del profesor)
# ============================================================
# ============================================================

print("\n=========== FORMA 2: ALUMNOS -> MATERIAS ===========")

# ----- CREAR MATRIZ -----
inicio = time.time()

matriz2 = [
    [random.randint(0, 100) for _ in range(materias)]
    for _ in range(alumnos)
]

fin = time.time()
print(f"Tiempo generando matriz: {fin - inicio:.6f} segundos")


# ----- BUSCAR DATO -----
inicio = time.time()

valor2 = matriz2[alumno_buscar-1][materia_buscar-1]

fin = time.time()
tiempo_busqueda2 = fin - inicio

print(f"Valor encontrado: {valor2}")
print(f"Tiempo búsqueda forma 2: {tiempo_busqueda2:.10f} segundos")


# ============================================================
# 5. COMPARACIÓN FINAL
# ============================================================
print("\n=========== COMPARACIÓN FINAL ===========")

if tiempo_busqueda1 < tiempo_busqueda2:
    print("La forma 1 (Materias -> Alumnos) fue MÁS RÁPIDA")
elif tiempo_busqueda2 < tiempo_busqueda1:
    print("La forma 2 (Alumnos -> Materias) fue MÁS RÁPIDA")
else:
    print("Ambas formas tuvieron velocidad similar")


print("\nPuedes cambiar arriba:")
print("alumnos = ...")
print("materias = ...")
print("y volver a ejecutar para probar con 1000, 10000 o más.")
