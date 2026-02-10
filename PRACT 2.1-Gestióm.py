# ============================================
# Programa equivalente al de Java en Python
# Arreglo para guardar 5 calificaciones
# ============================================

# 1. Crear arreglo (lista) de 5 espacios
calificaciones = [0] * 5

# 2. Ciclo para capturar calificaciones
for i in range(5):
    calificaciones[i] = int(input("Captura la calificación: "))

# 3. Mostrar resultados (opcional, en Java no estaba pero ayuda)
print("\nCalificaciones guardadas:")
for i in range(5):
    print(f"Calificación {i+1}: {calificaciones[i]}")
