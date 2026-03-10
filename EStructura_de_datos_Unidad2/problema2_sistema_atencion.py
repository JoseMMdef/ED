# ============================================================
#  PROBLEMA 2 — Sistema de Atención al Cliente
#  Compañía de Seguros — Manejo de Colas de Servicios
#
#  Comandos disponibles:
#    C<n>  → llega un cliente al servicio n  (ej: C1, C2, C3)
#    A<n>  → se atiende al siguiente cliente del servicio n
#    Q     → salir del sistema
#    L     → listar el estado de todas las colas
# ============================================================


# ──────────────────────────────────────────
#  CLASE COLA (reutilizable)
# ──────────────────────────────────────────
class Cola:
    """
    Implementación de la estructura Cola (FIFO).
    Primer cliente en llegar = primer cliente en ser atendido.
    """

    def __init__(self):
        self._elementos = []

    def enqueue(self, dato):
        """Agrega un elemento al final de la cola."""
        self._elementos.append(dato)

    def dequeue(self):
        """Extrae y devuelve el primer elemento de la cola."""
        if self.is_empty():
            raise IndexError("La cola está vacía.")
        return self._elementos.pop(0)

    def peek(self):
        """Devuelve el primer elemento sin eliminarlo."""
        if self.is_empty():
            return None
        return self._elementos[0]

    def is_empty(self):
        """Retorna True si la cola no tiene elementos."""
        return len(self._elementos) == 0

    def tamanio(self):
        """Retorna la cantidad de elementos en la cola."""
        return len(self._elementos)

    def __str__(self):
        if self.is_empty():
            return "(vacía)"
        return " → ".join(str(e) for e in self._elementos)


# ──────────────────────────────────────────
#  CLASE SISTEMA DE ATENCIÓN
# ──────────────────────────────────────────
class SistemaAtencion:
    """
    Gestiona las colas de atención de una compañía de seguros.

    Cada servicio tiene:
      - Una cola de clientes esperando
      - Un contador que genera números de atención únicos
      - Un nombre descriptivo del servicio
    """

    # Nombres de los servicios disponibles (se puede ampliar)
    NOMBRES_SERVICIO = {
        1: "Consultas Generales",
        2: "Reclamos y Siniestros",
        3: "Contratación de Pólizas",
        4: "Pagos y Facturas",
        5: "Soporte Técnico",
    }

    def __init__(self, num_servicios: int = 3):
        """
        Inicializa el sistema con el número de servicios indicado.

        Parámetro:
            num_servicios: cantidad de colas/servicios disponibles.
        """
        self._num_servicios = num_servicios

        # Diccionario: número de servicio → Cola de clientes
        self._colas = {}

        # Diccionario: número de servicio → contador de turnos emitidos
        self._contadores = {}

        # Inicializamos una cola y un contador por cada servicio
        for i in range(1, num_servicios + 1):
            self._colas[i] = Cola()
            self._contadores[i] = 0    # Empieza en 0, el primer turno será 1

        print(f"\n{'='*50}")
        print(" SISTEMA DE ATENCIÓN — COMPAÑÍA DE SEGUROS")
        print(f"{'='*50}")
        print(f"  Servicios disponibles: {num_servicios}")
        for i in range(1, num_servicios + 1):
            nombre = self.NOMBRES_SERVICIO.get(i, f"Servicio {i}")
            print(f"  [{i}] {nombre}")
        print(f"{'='*50}\n")

    def _validar_servicio(self, num_servicio: int) -> bool:
        """
        Verifica que el número de servicio sea válido.
        Retorna True si es válido, False si no existe.
        """
        if num_servicio not in self._colas:
            print(f"  ✗ Error: el servicio {num_servicio} no existe. "
                  f"Use un número entre 1 y {self._num_servicios}.")
            return False
        return True

    def cliente_llega(self, num_servicio: int):
        """
        Registra la llegada de un cliente al servicio indicado.
        Genera su número de atención y lo coloca en la cola.

        Parámetro:
            num_servicio: número del servicio al que llega el cliente.
        """
        if not self._validar_servicio(num_servicio):
            return

        # Incrementamos el contador para generar un número único
        self._contadores[num_servicio] += 1
        numero_atencion = self._contadores[num_servicio]

        # Añadimos el número a la cola del servicio
        self._colas[num_servicio].enqueue(numero_atencion)

        nombre = self.NOMBRES_SERVICIO.get(num_servicio, f"Servicio {num_servicio}")
        print(f"  ✔ Cliente registrado en [{num_servicio}] {nombre}")
        print(f"    Su número de atención es: *** {numero_atencion:03d} ***")
        print(f"    Personas esperando: {self._colas[num_servicio].tamanio()}")

    def atender_cliente(self, num_servicio: int):
        """
        Atiende al siguiente cliente de la cola del servicio indicado.
        Extrae el primer número de la cola y lo muestra en pantalla.

        Parámetro:
            num_servicio: número del servicio que quiere atender.
        """
        if not self._validar_servicio(num_servicio):
            return

        cola = self._colas[num_servicio]
        nombre = self.NOMBRES_SERVICIO.get(num_servicio, f"Servicio {num_servicio}")

        # Verificamos si hay clientes esperando
        if cola.is_empty():
            print(f"  ✗ No hay clientes esperando en [{num_servicio}] {nombre}.")
            return

        # Sacamos al primer cliente de la cola (FIFO)
        numero_llamado = cola.dequeue()

        print(f"\n  🔔 LLAMANDO AL NÚMERO: *** {numero_llamado:03d} ***")
        print(f"     Servicio: [{num_servicio}] {nombre}")

        if not cola.is_empty():
            print(f"     Próximo en cola: {cola.peek():03d}")
            print(f"     Personas restantes: {cola.tamanio()}")
        else:
            print(f"     La cola quedó vacía.")

    def mostrar_estado(self):
        """
        Muestra el estado actual de todas las colas del sistema.
        """
        print(f"\n{'─'*50}")
        print("  ESTADO ACTUAL DE LAS COLAS")
        print(f"{'─'*50}")
        for i in range(1, self._num_servicios + 1):
            nombre = self.NOMBRES_SERVICIO.get(i, f"Servicio {i}")
            cola = self._colas[i]
            print(f"  [{i}] {nombre:<28} ({cola.tamanio()} esperando)")
            print(f"       {cola}")
        print(f"{'─'*50}\n")


# ──────────────────────────────────────────
#  FUNCIÓN: procesar_comando
# ──────────────────────────────────────────
def procesar_comando(sistema: SistemaAtencion, comando: str) -> bool:
    """
    Interpreta el comando ingresado por el usuario y ejecuta la acción.

    Formatos válidos:
        C<n>  → cliente llega al servicio n
        A<n>  → atender siguiente cliente del servicio n
        L     → listar estado de las colas
        Q     → salir del sistema

    Retorna:
        bool: False si el usuario quiere salir, True para continuar.
    """
    comando = comando.strip().upper()   # Normalizamos: sin espacios y mayúsculas

    if not comando:
        return True   # Comando vacío: simplemente continuamos

    # ── Comando SALIR ──────────────────────
    if comando == "Q":
        print("\n  Sistema cerrado. ¡Hasta luego!\n")
        return False

    # ── Comando LISTAR ─────────────────────
    if comando == "L":
        sistema.mostrar_estado()
        return True

    # ── Comandos C y A ─────────────────────
    # Deben tener al menos 2 caracteres: la letra + el número
    if len(comando) < 2:
        print(f"  ✗ Comando no reconocido: '{comando}'. "
              "Use C<n>, A<n>, L o Q.")
        return True

    letra = comando[0]          # Primera letra: C o A
    numero_str = comando[1:]    # El resto debe ser el número de servicio

    # Verificamos que el número de servicio sea un entero válido
    if not numero_str.isdigit():
        print(f"  ✗ Número de servicio inválido: '{numero_str}'. "
              "Debe ser un número entero.")
        return True

    num_servicio = int(numero_str)

    if letra == "C":
        # Llega un cliente
        sistema.cliente_llega(num_servicio)

    elif letra == "A":
        # Se atiende un cliente
        sistema.atender_cliente(num_servicio)

    else:
        print(f"  ✗ Comando no reconocido: '{comando}'. "
              "Use C<n>, A<n>, L o Q.")

    return True


# ──────────────────────────────────────────
#  PROGRAMA PRINCIPAL
# ──────────────────────────────────────────
if __name__ == "__main__":

    # Creamos el sistema con 3 servicios (puede cambiarse)
    sistema = SistemaAtencion(num_servicios=3)

    print("  Comandos disponibles:")
    print("    C<n>  → llega un cliente al servicio n   (ej: C1)")
    print("    A<n>  → atender siguiente cliente         (ej: A1)")
    print("    L     → listar estado de las colas")
    print("    Q     → salir\n")

    # Bucle principal: el sistema corre hasta que el usuario escribe Q
    while True:
        try:
            comando = input("  Ingrese comando: ").strip()
            continuar = procesar_comando(sistema, comando)
            if not continuar:
                break
            print()   # Línea en blanco para mejor legibilidad

        except KeyboardInterrupt:
            # Manejo elegante de Ctrl+C
            print("\n\n  Sistema interrumpido. ¡Hasta luego!\n")
            break
