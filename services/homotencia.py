import numpy as np
import matplotlib.pyplot as plt

# --- Función para realizar homotecia (escalamiento respecto a un centro) ---
def homotencia(puntos, k, centro):
    # puntos: array Nx2 con coordenadas (x, y)
    # k: factor de escala (mayor que 1 para ampliar, entre 0 y 1 para reducir)
    # centro: punto (x, y) que actúa como centro de la homotecia
    # Calcula la nueva posición de cada punto escalado respecto al centro
    return centro + k * (puntos - centro)

def homotencia_3d(puntos, k, centro):
    """
    Realiza homotecia (escalamiento uniforme) en 3D respecto a un centro.
    :param puntos: array Nx3 con coordenadas (x, y, z)
    :param k: factor de escala (mayor que 1 para ampliar, entre 0 y 1 para reducir)
    :param centro: punto (x, y, z) que actúa como centro de la homotecia
    :return: array Nx3 con los puntos transformados
    """
    # La fórmula es la misma que en 2D pero extendida a 3D
    return centro + k * (puntos - centro)
