"""
Módulo de Jugador.
Define la clase Jugador con sus atributos, métodos y lógica de supervivencia.
"""

from utilidades import clamp, formatear_numero
import config

class Jugador:
    """
    Clase que representa al jugador.
    
    Gestiona:
    - Recursos de supervivencia (vida, oxígeno)
    - Dinero/Chatarra
    - Mejoras permanentes
    - Progreso en exploración
    """
    
    def __init__(self, nombre="Explorador"):
        """
        Inicializa un nuevo jugador.
        
        Args:
            nombre (str): Nombre del jugador
        """
        self.nombre = nombre
        
        # ════════════════════════════════════════════════════════════════
        # RECURSOS DE SUPERVIVENCIA
        # ════════════════════════════════════════════════════════════════
        self.vida_actual = config.VIDA_INICIAL
        self.vida_maxima = config.VIDA_INICIAL
        
        self.oxigeno_actual = config.OXIGENO_INICIAL
        self.oxigeno_maximo = config.OXIGENO_INICIAL
        
        # ════════════════════════════════════════════════════════════════
        # RECURSOS ECONÓMICOS
        # ════════════════════════════════════════════════════════════════
        self.chatarra = config.CHATARRA_INICIAL
        self.chatarra_total_recolectada = 0
        
        # ════════════════════════════════════════════════════════════════
        # ESTADÍSTICAS Y PROGRESO
        # ════════════════════════════════════════════════════════════════
        self.turno_actual = 0
        self.distancia_recorrida = 0
        self.eventos_experimentados = 0
        self.combates_ganados = 0
        self.vidas_perdidas = 0
        
        # ════════════════════════════════════════════════════════════════
        # MEJORAS PERMANENTES
        # ════════════════════════════════════════════════════════════════
        self.mejoras_compradas = []
        self.reduccion_danio = 0  # Porcentaje (0-100)
        self.bonus_recoleccion = 1.0  # Multiplicador
        self.regeneracion_vida = 0  # Por turno
        
        # ════════════════════════════════════════════════════════════════
        # ESTADO ESPECIAL
        # ════════════════════════════════════════════════════════════════
        self.escudo_activo = False
        self.turnos_escudo_restantes = 0
        self.vivo = True
    
    # ════════════════════════════════════════════════════════════════════
    # MÉTODOS DE GESTIÓN DE RECURSOS
    # ════════════════════════════════════════════════════════════════════
    
    def reducir_oxigeno(self, cantidad=None):
        """
        Reduce el oxígeno disponible.
        
        Args:
            cantidad (int): Cantidad a reducir (por defecto, consumo estándar)
        """
        if cantidad is None:
            cantidad = config.CONSUMO_OXIGENO_POR_TURNO
        
        self.oxigeno_actual = clamp(
            self.oxigeno_actual - cantidad,
            0,
            self.oxigeno_maximo
        )
    
    def aumentar_oxigeno(self, cantidad):
        """Aumenta el oxígeno disponible."""
        self.oxigeno_actual = clamp(
            self.oxigeno_actual + cantidad,
            0,
            self.oxigeno_maximo
        )
    
    def recibir_danio(self, danio_base):
        """
        Aplica daño al jugador considerando su armadura/mejoras.
        
        Args:
            danio_base (int): Daño a aplicar antes de reducción
        
        Returns:
            int: Daño final aplicado
        """
        if self.escudo_activo:
            return 0  # El escudo bloquea todo el daño
        
        # Aplicar reducción de daño por mejoras
        danio_final = int(danio_base * (1 - self.reduccion_danio / 100))
        self.vida_actual = clamp(self.vida_actual - danio_final, 0, self.vida_maxima)
        
        if self.vida_actual <= 0:
            self.vivo = False
        
        return danio_final
    
    def recuperar_vida(self, cantidad):
        """Recupera vida."""
        self.vida_actual = clamp(
            self.vida_actual + cantidad,
            0,
            self.vida_maxima
        )
    
    def obtener_chatarra(self, cantidad):
        """
        Añade chatarra (aplicando bonus de recolección).
        
        Args:
            cantidad (int): Cantidad base
        """
        cantidad_final = int(cantidad * self.bonus_recoleccion)
        self.chatarra += cantidad_final
        self.chatarra_total_recolectada += cantidad_final
    
    def gastar_chatarra(self, cantidad):
        """
        Intenta gastar chatarra.
        
        Args:
            cantidad (int): Cantidad a gastar
        
        Returns:
            bool: True si se pudo gastar, False si no hay suficiente
        """
        if self.chatarra >= cantidad:
            self.chatarra -= cantidad
            return True
        return False
    
    # ════════════════════════════════════════════════════════════════════
    # MÉTODOS DE MECÁNICA DE JUEGO
    # ════════════════════════════════════════════════════════════════════
    
    def completar_turno(self):
        """Realiza todas las acciones que ocurren automáticamente cada turno."""
        self.turno_actual += 1
        
        # Consumir oxígeno
        self.reducir_oxigeno()
        
        # Aplicar daño si no hay oxígeno
        if self.oxigeno_actual <= 0:
            self.recibir_danio(config.CONSUMO_VIDA_SIN_OXIGENO)
        
        # Regenerar vida si tiene mejora de medibots
        if self.turno_actual % 3 == 0 and self.regeneracion_vida > 0:
            self.recuperar_vida(self.regeneracion_vida)
        
        # Actualizar duración del escudo
        if self.escudo_activo:
            self.turnos_escudo_restantes -= 1
            if self.turnos_escudo_restantes <= 0:
                self.escudo_activo = False
    
    def aplicar_mejora(self, tipo_mejora):
        """
        Aplica una mejora permanente.
        
        Args:
            tipo_mejora (str): ID de la mejora a aplicar
        """
        if tipo_mejora in self.mejoras_compradas:
            return  # Ya tiene esta mejora
        
        self.mejoras_compradas.append(tipo_mejora)
        
        if tipo_mejora == "cilindro_oxigeno":
            self.oxigeno_maximo += 50
            self.oxigeno_actual = self.oxigeno_maximo
        
        elif tipo_mejora == "armadura_ligera":
            self.reduccion_danio = min(self.reduccion_danio + 20, 80)
        
        elif tipo_mejora == "detector_recursos":
            self.bonus_recoleccion *= 1.3
        
        elif tipo_mejora == "medibots":
            self.regeneracion_vida = 30
        
        elif tipo_mejora == "escudo_temporal":
            self.escudo_activo = True
            self.turnos_escudo_restantes = 5
    
    def explorar(self, distancia=10):
        """
        Avanza en la exploración.
        
        Args:
            distancia (int): Distancia a recorrer
        """
        self.distancia_recorrida += distancia
        self.distancia_recorrida = min(
            self.distancia_recorrida,
            config.DISTANCIA_MAXIMA_EXPLORACION
        )
    
    def obtener_resumen_estado(self):
        """
        Retorna un resumen del estado actual del jugador.
        
        Returns:
            dict: Diccionario con el estado del jugador
        """
        return {
            "nombre": self.nombre,
            "vida": self.vida_actual,
            "vida_maxima": self.vida_maxima,
            "ox
