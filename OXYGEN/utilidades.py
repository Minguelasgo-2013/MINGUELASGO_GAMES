"""
Módulo de utilidades.
Contiene funciones auxiliares para visualización, formateo y operaciones comunes.
"""

import os
import json
from pathlib import Path
from datetime import datetime

# ============================================================================
# UTILIDADES DE VISUALIZACIÓN
# ============================================================================

def limpiar_consola():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_titulo(titulo, ancho=80):
    """
    Muestra un título formateado con borde.
    
    Args:
        titulo (str): Texto del título
        ancho (int): Ancho del borde
    """
    borde = "=" * ancho
    print(f"\n{borde}")
    print(titulo.center(ancho))
    print(f"{borde}\n")


def mostrar_seccion(titulo):
    """Muestra un título de sección."""
    print(f"\n{'─' * 80}")
    print(f"▶ {titulo}")
    print(f"{'─' * 80}")


def mostrar_barra_progreso(actual, maximo, longitud=30, etiqueta=""):
    """
    Muestra una barra de progreso en la consola.
    
    Args:
        actual (int): Valor actual
        maximo (int): Valor máximo
        longitud (int): Longitud de la barra en caracteres
        etiqueta (str): Etiqueta descriptiva
    
    Returns:
        str: Barra de progreso formateada
    """
    if maximo <= 0:
        porcentaje = 0
    else:
        porcentaje = int((actual / maximo) * 100)
    
    relleno = int((actual / maximo) * longitud) if maximo > 0 else 0
    barra = "█" * relleno + "░" * (longitud - relleno)
    
    color_porcentaje = "🔴" if porcentaje < 25 else "🟡" if porcentaje < 50 else "🟢"
    
    return f"{etiqueta:15} {barra} {porcentaje:3d}% {color_porcentaje}"


def pausa_usuario():
    """Pausa el juego hasta que el usuario presione Enter."""
    input("\n[Presiona ENTER para continuar...]")


# ============================================================================
# UTILIDADES DE ALMACENAMIENTO
# ============================================================================

def crear_directorio_datos():
    """Crea el directorio de datos si no existe."""
    Path("datos").mkdir(exist_ok=True)


def guardar_datos(datos, archivo):
    """
    Guarda datos en formato JSON.
    
    Args:
        datos (dict): Datos a guardar
        archivo (str): Ruta del archivo
    """
    crear_directorio_datos()
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def cargar_datos(archivo, predeterminados=None):
    """
    Carga datos desde un archivo JSON.
    
    Args:
        archivo (str): Ruta del archivo
        predeterminados (dict): Datos por defecto si el archivo no existe
    
    Returns:
        dict: Datos cargados o predeterminados
    """
    if Path(archivo).exists():
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    return predeterminados or {}


# ============================================================================
# UTILIDADES DE FORMATOS
# ============================================================================

def formatear_numero(numero):
    """Formatea un número con separadores de miles."""
    return f"{numero:,}".replace(",", ".")


def obtener_marca_tiempo():
    """Obtiene una marca de tiempo legible."""
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# ============================================================================
# UTILIDADES DE LÓGICA
# ============================================================================

def clamp(valor, minimo, maximo):
    """Limita un valor entre un mínimo y máximo."""
    return max(minimo, min(valor, maximo))


def calcular_porcentaje(parte, total):
    """Calcula el porcentaje de una parte respecto al total."""
    if total <= 0:
        return 0
    return (parte / total) * 100
