import numpy as np
import matplotlib.pyplot as plt

# --- Función para rotar un conjunto de puntos 2D alrededor de un centro dado ---
def rotacion_general(puntos, theta, centro):
    # puntos: array Nx2 con coordenadas (x, y)
    # theta: ángulo de rotación en radianes
    # centro: punto (x, y) alrededor del cual se realiza la rotación
    # Construye la matriz de rotación 2x2
    R = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])
    # Trasladar puntos para que el centro de rotación sea el origen
    puntos_traducidos = puntos - centro
    # Aplicar rotación y luego trasladar de vuelta
    puntos_rotados = (R @ puntos_traducidos.T).T + centro
    return puntos_rotados



# --- Función para rotar un conjunto de puntos 3D alrededor de un eje dado ---
def rotacion_general_3d(puntos, theta, eje='z'):
    """
    Rota un conjunto de puntos 3D alrededor del eje especificado.
    :param puntos: array Nx3 con coordenadas (x, y, z)
    :param theta: ángulo de rotación en radianes
    :param eje: eje de rotación ('x', 'y' o 'z')
    :return: array Nx3 con los puntos rotados
    """
    if eje == 'x':
        R = np.array([
            [1, 0, 0],
            [0, np.cos(theta), -np.sin(theta)],
            [0, np.sin(theta),  np.cos(theta)]
        ])
    elif eje == 'y':
        R = np.array([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)]
        ])
    elif eje == 'z':
        R = np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta),  np.cos(theta), 0],
            [0, 0, 1]
        ])
    else:
        raise ValueError("Eje no válido. Use 'x', 'y' o 'z'.")

    puntos_rotados = (R @ puntos.T).T
    return puntos_rotados