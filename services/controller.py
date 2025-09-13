
"""
class ControladorTransformaciones:
    def __init__(self):
        self.vertices = []
        self.num_vertices = 0

    def set_vertices(self, num_vertices, vertices):
        self.num_vertices = num_vertices
        self.vertices = vertices
        print(f"Cantidad de vértices: {num_vertices}")
        print(f"Vértices recibidos: {vertices}")
"""
"""import numpy as np
import matplotlib.pyplot as plt

    class ControladorTransformaciones:
        def __init__(self):
            self.vertices = []
            self.num_vertices = 0
            self.matriz = None

        def set_vertices(self, num_vertices, vertices):
            self.num_vertices = num_vertices
            self.vertices = np.array(vertices, dtype=float)
            print(f"Cantidad de vértices: {num_vertices}")
            print(f"Vértices recibidos: {vertices}")

        def aplicar_transformacion(self, matriz):
            
            if self.vertices is None or len(self.vertices) == 0:
                print("No hay vértices para transformar")
                return None

            # Asegurar que la matriz sea 2x2 y los vértices Nx2
            transformados = self.vertices @ matriz.T
            return transformados
"""
"""
class ControladorMatriz:
    @staticmethod
    def identidad():
        return np.eye(2)

    @staticmethod
    def rotacion(theta):
        return np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta),  np.cos(theta)]
        ])

    @staticmethod
    def escala(sx, sy):
        return np.array([
            [sx, 0],
            [0, sy]
        ])
"""
"""
class ControladorGrafico:
    @staticmethod
    def graficar(vertices, vertices_transformados=None, titulo="Polígono"):
        plt.figure()
        plt.title(titulo)
        plt.axis("equal")

        # Graficar original
        x, y = zip(*vertices)
        plt.fill(x, y, alpha=0.3, label="Original")

        # Graficar transformado (si existe)
        if vertices_transformados is not None:
            xt, yt = zip(*vertices_transformados)
            plt.fill(xt, yt, alpha=0.3, label="Transformado")

        plt.legend()
        plt.show()
"""

class ControladorGrafico:
    @staticmethod
    def preparar(vertices, vertices_transformados=None):
        """Devuelve los datos listos para graficar en CanvasMPL"""
        data = {"original": vertices}
        if vertices_transformados is not None:
            data["transformado"] = vertices_transformados
        return data