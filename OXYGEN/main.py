"""
OXYGEN - Juego Roguelite de Supervivencia
================================================
Punto de entrada principal del juego.
Gestiona el bucle principal, menús y flujo de juego.
"""

import os
import random
from jugador import Jugador
from mercado import Mercado
from eventos import GestorEventos
from utilidades import (
    limpiar_consola,
    mostrar_titulo,
    mostrar_seccion,
    mostrar_barra_progreso,
    pausa_usuario,
    guardar_datos,
    cargar_datos,
    obtener_marca_tiempo
)
import config

# ════════════════════════════════════════════════════════════════════════════
# CLASE PRINCIPAL DEL JUEGO
# ════════════════════════════════════════════════════════════════════════════

class Juego:
    """
    Clase principal que gestiona todo el flujo del juego.
    
    Responsabilidades:
    - Bucle principal del juego
    - Menús y decisiones del jugador
    - Estados del juego
    - Guardado y carga
    """
    
    def __init__(self):
        """Inicializa el juego."""
        self.jugador = None
        self.mercado = Mercado()
        self.gestor_eventos = GestorEventos()
        self.en_juego = False
        self.en_pausa = False
    
    # ════════════════════════════════════════════════════════════════════
    # MÉTODOS DE INICIO
    # ════════════════════════════════════════════════════════════════════
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal del juego."""
        while True:
            
