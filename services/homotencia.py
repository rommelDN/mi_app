import numpy as np
import matplotlib.pyplot as plt

# --- Función para realizar homotecia (escalamiento respecto a un centro) ---
def homotencia(puntos, k, centro):
    # puntos: array Nx2 con coordenadas (x, y)
    # k: factor de escala (mayor que 1 para ampliar, entre 0 y 1 para reducir)
    # centro: punto (x, y) que actúa como centro de la homotecia
    # Calcula la nueva posición de cada punto escalado respecto al centro
    return centro + k * (puntos - centro)