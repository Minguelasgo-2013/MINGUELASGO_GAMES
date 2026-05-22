"""
Módulo de Eventos.
Gestiona eventos aleatorios que ocurren durante la exploración.
"""

import random
import config
from utilidades import mostrar_seccion

class GestorEventos:
    """
    Clase que gestiona los eventos aleatorios del juego.
    
    Tipos de eventos:
    - Descubrimiento de recursos
    - Encuentros peligrosos
    - Anomalías ambientales
    - Hallazgos especiales
    """
    
    def __init__(self):
        """Inicializa el gestor de eventos."""
        self.eventos_ocurridos = []
        self.eventos_disponibles = self._crear_eventos()
    
    # ════════════════════════════════════════════════════════════════════
    # MÉTODOS DE EVENTO
    # ════════════════════════════════════════════════════════════════════
    
    def _crear_eventos(self):
        """
        Define todos los eventos posibles del juego.
        
        Returns:
            list: Lista de eventos disponibles
        """
        return [
            {
                "nombre": "💎 Depósito de Chatarra",
                "descripcion": "¡Encontraste un depósito de chatarra valiosa!",
                "tipo": "recompensa",
                "valor": random.randint(
                    config.RECOMPENSA_CHATARRA_MIN,
                    config.RECOMPENSA_CHATARRA_MAX
                ),
                "probabilidad": 0.35
            },
            {
                "nombre": "⚠️ Zona Contaminada",
                "descripcion": "¡Entraste a una zona contaminada! Recibes daño.",
                "tipo": "danio",
                "valor": random.randint(
                    config.DANIO_EVENTO_MIN,
                    config.DANIO_EVENTO_MAX
                ),
                "probabilidad": 0.25
            },
            {
                "nombre": "🔥 Explosión Inesperada",
                "descripcion": "¡Una explosión te golpea!",
                "tipo": "danio",
                "valor": random.randint(15, 25),
                "probabilidad": 0.15
            },
            {
                "nombre": "🛡️ Escudo Abandonado",
                "descripcion": "¡Encontraste un generador de escudo antiguo!",
                "tipo": "escudo",
                "valor": 1,
                "probabilidad": 0.10
            },
            {
                "nombre": "🌀 Tormenta de Radiación",
                "descripcion": "¡Una tormenta de radiación te alcanza!",
                "tipo": "danio",
                "valor": random.randint(20, 40),
                "probabilidad": 0.08
            },
            {
                "nombre": "💚 Base de Suministros",
                "descripcion": "¡Encontraste una base con suministros médicos!",
                "tipo": "curacion",
                "valor": 30,
                "probabilidad": 0.07
            }
        ]
    
    def generar_evento_aleatorio(self, jugador):
        """
        Genera un evento aleatorio según la probabilidad.
        
        Args:
            jugador (Jugador): Referencia al jugador
        
        Returns:
            dict or None: Evento ocurrido o None si no hay evento
        """
        # Determinar si ocurre un evento
        if random.random() > config.PROBABILIDAD_EVENTO:
            return None
        
        # Seleccionar un evento aleatorio
        evento = random.choice(self.eventos_disponibles)
        evento_copia = evento.copy()
        
        # Registrar el evento
        self.eventos_ocurridos.append(evento_copia)
        jugador.eventos_experimentados += 1
        
        return evento_copia
    
    # ════════════════════════════════════════════════════════════════════
    # MÉTODOS DE APLICACIÓN DE EFECTOS
    # ════════════════════════════════════════════════════════════════════
    
    def aplicar_evento(self, jugador, evento):
        """
        Aplica los efectos de un evento al jugador.
        
        Args:
            jugador (Jugador): Referencia al jugador
            evento (dict): Evento a aplicar
        """
        mostrar_seccion(evento["nombre"])
        print(f"📝 {evento['descripcion']}\n")
        
        tipo_evento = evento["tipo"]
        valor = evento["valor"]
        
        if tipo_evento == "recompensa":
            jugador.obtener_chatarra(valor)
            print(f"✅ +{int(valor * jugador.bonus_recoleccion)} de chatarra obtenida")
        
        elif tipo_evento == "danio":
            danio_aplicado = jugador.recibir_danio(valor)
            print(f"❌ Recibiste {danio_aplicado} de daño")
            print(f"❤️ Vida actual: {jugador.vida_actual}/{jugador.vida_maxima}")
        
        elif tipo_evento == "curacion":
            jugador.recuperar_vida(valor)
            print(f"💚 Recuperaste {valor} de vida")
            print(f"❤️ Vida actual: {jugador.vida_actual}/{jugador.vida_maxima}")
        
        elif tipo_evento == "escudo":
            jugador.escudo_activo = True
            jugador.turnos_escudo_restantes = 5
            print(f"🛡️ ¡Escudo activado por 5 turnos!")
        
        print()
    
    def obtener_estadisticas_eventos(self):
        """
        Retorna estadísticas sobre los eventos ocurridos.
        
        Returns:
            dict: Estadísticas de eventos
        """
        total_eventos = len(self.eventos_ocurridos)
        
        eventos_por_tipo = {
            "recompensa": 0,
            "danio": 0,
            "curacion": 0,
            "escudo": 0
        }
        
        for evento in self.eventos_ocurridos:
            tipo = evento["tipo"]
            if tipo in eventos_por_tipo:
                eventos_por_tipo[tipo] += 1
        
        return {
            "total": total_eventos,
            "por_tipo": eventos_por_tipo
        }
