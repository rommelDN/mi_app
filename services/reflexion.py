import numpy as np
import matplotlib.pyplot as plt

# --- Función para realizar reflexión de puntos 2D usando una matriz de reflexión ---
def reflexion(matriz_reflexion, puntos):
    # matriz_reflexion: matriz 2x2 que define la reflexión
    # puntos: array Nx2 con coordenadas (x, y)
    # Aplica la matriz de reflexión a cada punto
    return (matriz_reflexion @ puntos.T).T