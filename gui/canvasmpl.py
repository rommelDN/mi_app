from mpl_toolkits.mplot3d import Axes3D
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class CanvasMPL(FigureCanvas):
    # Lienzo personalizado basado en Matplotlib embebido en Qt para dibujar gráficos.
    def __init__(self):
        # Crear la figura de Matplotlib que contendrá el gráfico.
        self.fig = Figure()
        # Inicializar el canvas con la figura creada.
        super().__init__(self.fig)
        # Añadir un subplot (área de dibujo) a la figura.
        self.ax = self.fig.add_subplot(111)
        # Configurar la relación de aspecto para que sea igual (cuadrado).
        self.ax.set_aspect('equal')
        # Establecer los límites iniciales para los ejes X e Y.
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        # Activar la malla para facilitar la visualización de la gráfica.
        self.ax.grid(True)
        # --- Añadir plano cartesiano central y ejes con flechas ---
        self.ax.set_autoscalex_on(False)
        self.ax.set_autoscaley_on(False)
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['left'].set_position('zero')
        self.ax.annotate('', xy=(10, 0), xytext=(0, 0),
                         arrowprops=dict(facecolor='black', width=1.5, headwidth=8))
        self.ax.annotate('', xy=(0, 10), xytext=(0, 0),
                         arrowprops=dict(facecolor='black', width=1.5, headwidth=8))
        self.ax.annotate('X', xy=(10, 0), xytext=(10.5, 0),
                         textcoords='data', ha='center', va='center')
        self.ax.annotate('Y', xy=(0, 10), xytext=(0, 10.5),
                         textcoords='data', ha='center', va='center')
        self.ax.set_xticks(range(-10, 11))
        self.ax.set_yticks(range(-10, 11))
    def plot_polygon(self, vertices):
        # Limpiar el gráfico anterior para dibujar uno nuevo.
        self.ax.clear()

        self.ax.set_autoscalex_on(False)
        self.ax.set_autoscaley_on(False)

        # Ejes tipo plano cartesiano central:
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_aspect('equal')
        self.ax.grid(True)

        # Dibujar los ejes principales en 0
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['left'].set_position('zero')

        # Flechas para los ejes X y Y
        self.ax.annotate('', xy=(10, 0), xytext=(0, 0),
                         arrowprops=dict(facecolor='black', width=1.5, headwidth=8))
        self.ax.annotate('', xy=(0, 10), xytext=(0, 0),
                         arrowprops=dict(facecolor='black', width=1.5, headwidth=8))

        self.ax.annotate('X', xy=(10, 0), xytext=(10.5, 0),
                         textcoords='data', ha='center', va='center')
        self.ax.annotate('Y', xy=(0, 10), xytext=(0, 10.5),
                         textcoords='data', ha='center', va='center')

        self.ax.set_xticks(range(-10, 11))
        self.ax.set_yticks(range(-10, 11))

        if vertices is not None and len(vertices) > 0:
            puntos = np.array(vertices, dtype=float).tolist()
            polygon = puntos + [puntos[0]]
            xs, ys = zip(*polygon)
            self.ax.plot(xs, ys, 'b-')

        # Reaplicar límites para mantener el centro
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)

        # Redibujar el canvas para mostrar los cambios.
        self.draw()

        
class CanvasMPL3D(FigureCanvas):
    # Lienzo personalizado para gráficos 3D con Matplotlib embebido en Qt.
    def __init__(self):
        self.fig = Figure()
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_zlim(-10, 10)
        self.ax.grid(True)
        # Establecer aspecto igual si es posible
        try:
            self.ax.set_box_aspect([1, 1, 1])
        except Exception:
            pass

    def plot_polyhedron(self, vertices, faces):
        self.ax.clear()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_zlim(-10, 10)
        try:
            self.ax.set_box_aspect([1, 1, 1])
        except Exception:
            pass
        self.ax.grid(True)
        if vertices and faces:
            verts = np.array(vertices, dtype=float)
            for face in faces:
                face_coords = verts[face]
                # Cerrar la cara conectando el último con el primero
                xs, ys, zs = zip(*face_coords, face_coords[0])
                self.ax.plot(xs, ys, zs, 'b-')
        self.draw()