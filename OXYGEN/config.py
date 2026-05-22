"""
Configuración central del juego.
Define constantes, valores por defecto y parámetros del gameplay.
"""

# ============================================================================
# CONFIGURACIÓN DE DIFICULTAD Y GAMEPLAY
# ============================================================================

VIDA_INICIAL = 100
OXIGENO_INICIAL = 100
CHATARRA_INICIAL = 50

# Consumo de recursos por turno
CONSUMO_OXIGENO_POR_TURNO = 5
CONSUMO_VIDA_SIN_OXIGENO = 10

# Parámetros de exploración
DISTANCIA_MAXIMA_EXPLORACION = 1000
VELOCIDAD_MOVIMIENTO = 10

# ============================================================================
# CONFIGURACIÓN DE EVENTOS ALEATORIOS
# ============================================================================

PROBABILIDAD_EVENTO = 0.4  # 40% de probabilidad por turno
RECOMPENSA_CHATARRA_MIN = 10
RECOMPENSA_CHATARRA_MAX = 50
DANIO_EVENTO_MIN = 10
DANIO_EVENTO_MAX = 30

# ============================================================================
# CONFIGURACIÓN DEL MERCADO
# ============================================================================

MEJORAS_DISPONIBLES = {
    "cilindro_oxigeno": {
        "nombre": "Cilindro de Oxígeno Mejorado",
        "costo": 100,
        "efecto": "Aumenta capacidad de oxígeno en +50",
        "tipo": "permanente"
    },
    "armadura_ligera": {
        "nombre": "Armadura Ligera",
        "costo": 150,
        "efecto": "Reduce daño recibido en 20%",
        "tipo": "permanente"
    },
    "detector_recursos": {
        "nombre": "Detector de Recursos",
        "costo": 200,
        "efecto": "Aumenta recolección de chatarra en +30%",
        "tipo": "permanente"
    },
    "medibots": {
        "nombre": "Medibots Reparadores",
        "costo": 250,
        "efecto": "Restaura +30 de vida cada 3 turnos",
        "tipo": "permanente"
    },
    "escudo_temporal": {
        "nombre": "Escudo Temporal",
        "costo": 300,
        "efecto": "Bloquea todo daño por 5 turnos (uso único)",
        "tipo": "consumible"
    }
}

# ============================================================================
# CONFIGURACIÓN DE INTERFAZ
# ============================================================================

MOSTRAR_ESTADISTICAS_CADA_N_TURNOS = 5
ANCHO_CONSOLA = 80

# ============================================================================
# CONFIGURACIÓN DE PERSISTENCIA
# ============================================================================

ARCHIVO_GUARDADO = "datos/progreso_jugador.json"
ARCHIVO_ESTADISTICAS = "datos/estadisticas.json"
