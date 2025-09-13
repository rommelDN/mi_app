import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QSplitter,QRadioButton,QButtonGroup
)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Definición de la clase principal de la ventana de la aplicación,
# que hereda de QMainWindow para aprovechar sus funcionalidades.
class CanvasMPL(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect('equal')
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        # Activar malla
        self.ax.grid(True)
    def plot_polygon(self, vertices):
        self.ax.clear()
        if vertices:
            polygon = vertices + [vertices[0]]
            xs, ys = zip(*polygon)
            self.ax.plot(xs, ys, 'b-')
        self.ax.set_aspect('equal')
        # Activar malla
        self.ax.grid(True)
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.draw()

class VentanaTransformaciones(QMainWindow):
    def __init__(self):
        super().__init__()
        # Configuración del título de la ventana principal.
        self.setWindowTitle("Proyecto Transformaciones Lineales")
        # Maximiza la ventana para que ocupe toda la pantalla al iniciar.
        self.showMaximized()

        # --- CONTENEDOR PRINCIPAL ---
        # Crea un splitter horizontal que divide el área en dos paneles (izquierda y derecha).
        splitter = QSplitter(Qt.Horizontal)

        # -----------------------------
        # IZQUIERDA → Inputs
        # -----------------------------
        # Panel izquierdo que contendrá los inputs para los parámetros de la transformación.
        panel_izq = QWidget()
        # Layout vertical para organizar los widgets uno debajo del otro.
        layout_izq = QVBoxLayout()
        # Establece márgenes internos para el layout (espacio entre borde y contenido).
        layout_izq.setContentsMargins(20, 20, 20, 20)

        # Etiqueta descriptiva para los parámetros de transformación.
        layout_izq.addWidget(QLabel("Parámetros de transformación:"))
        layout_izq.addWidget(QLabel("Escoger cantidad de vértices:"))

        # Botón para escoger cantidad de vértices.
        self.btn_vertices1 = QRadioButton("3")
        self.btn_vertices2 = QRadioButton("4")
        self.btn_vertices3 = QRadioButton("5")

        # Agrupamos los botones
        self.grupo_vertices = QButtonGroup()
        self.grupo_vertices.addButton(self.btn_vertices1, 3)
        self.grupo_vertices.addButton(self.btn_vertices2, 4)
        self.grupo_vertices.addButton(self.btn_vertices3, 5)

        layout_izq.addWidget(self.btn_vertices1)
        layout_izq.addWidget(self.btn_vertices2)
        layout_izq.addWidget(self.btn_vertices3)


        layout_izq.addWidget(QLabel("Ingresar Vértices:"))
        # Crear inputs de vértices (máximo 5, pero inicialmente ocultos)
        self.inputs_vertices = []
        for i in range(5):
            input_v = QLineEdit()
            input_v.setPlaceholderText(f"Vértice {i+1} (x,y)")
            input_v.hide()  # Ocultar por defecto
            self.inputs_vertices.append(input_v)
            layout_izq.addWidget(input_v)
        
        # Conectar evento
        self.grupo_vertices.buttonToggled.connect(self.actualizar_vertices)
        
        layout_izq.addWidget(QLabel("Fijar Vertice de Rotacion:"))
        self.btn_fijar1 = QRadioButton("Centro")
        self.btn_fijar2 = QRadioButton("Escoger")
        self.grupo_fijar = QButtonGroup()
        self.grupo_fijar.addButton(self.btn_fijar1, 5)
        self.grupo_fijar.addButton(self.btn_fijar2, 6)
        layout_izq.addWidget(self.btn_fijar1)
        layout_izq.addWidget(self.btn_fijar2)

        # Input para escoger punto, oculto por defecto
        self.input_punto = QLineEdit()
        self.input_punto.setPlaceholderText("Punto(0,0)")
        self.input_punto.hide()
        layout_izq.addWidget(self.input_punto)

        # Conectar evento de grupo_fijar
        self.grupo_fijar.buttonToggled.connect(self.actualizar_fijar)


        layout_izq.addWidget(QLabel("Rotar en el eje X:"))
        self.input_x = QLineEdit()
        self.input_x.setPlaceholderText("Grados(0°)")
        layout_izq.addWidget(self.input_x)


        layout_izq.addWidget(QLabel("Rotar en el eje Y:"))
        self.input_y = QLineEdit()
        self.input_y.setPlaceholderText("Grados(0°)")
        layout_izq.addWidget(self.input_y)


        layout_izq.addWidget(QLabel("Rotar en el eje Z:"))
        self.input_z = QLineEdit()
        self.input_z.setPlaceholderText("Grados(0°)")
        layout_izq.addWidget(self.input_z)
        

        # Botón para aplicar la transformación con los valores ingresados.
        self.btn_aplicar = QPushButton("Aplicar transformación")
        self.btn_aplicar.clicked.connect(self.enviar_vertices)
        layout_izq.addWidget(self.btn_aplicar)

        # Añade un espacio flexible para empujar los widgets hacia arriba.
        layout_izq.addStretch()
        # Asigna el layout al panel izquierdo.
        panel_izq.setLayout(layout_izq)


        # -----------------------------
        # DERECHA → Canvas
        # -----------------------------
        # Panel derecho que actuará como canvas o área de dibujo para mostrar resultados.
        self.canvas = CanvasMPL()

        # Añade ambos paneles al splitter para que se puedan redimensionar.
        splitter.addWidget(panel_izq)
        splitter.addWidget(self.canvas)

        # Define el tamaño inicial relativo de cada panel dentro del splitter.
        splitter.setSizes([300, 900])

        # Establece el splitter como el widget central de la ventana principal.
        self.setCentralWidget(splitter)

    def actualizar_vertices(self, button, checked):
        if checked:
            cantidad = self.grupo_vertices.id(button)
            for i, input_v in enumerate(self.inputs_vertices):
                if i < cantidad:
                    input_v.show()
                else:
                    input_v.hide()
    def actualizar_fijar(self, button, checked):
        if not checked:
            # Solo actuar cuando el botón se activa
            return
        if button.text() == "Centro":
            pass
            self.input_punto.hide()
        elif button.text() == "Escoger":
            self.input_punto.show()
        else:
            self.input_punto.hide()
    
    def enviar_vertices(self):
        # Número de vértices seleccionados
        num_vertices = 0
        for btn in self.grupo_vertices.buttons():
            if btn.isChecked():
                num_vertices = self.grupo_vertices.id(btn)

        # Recolectar los vértices escritos
        vertices = []
        for i in range(num_vertices):
            texto = self.inputs_vertices[i].text()
            if texto:
                try:
                    # Espera formato: "x,y"
                    x, y = map(float, texto.strip("() ").split(","))
                    vertices.append((x, y))
                except Exception:
                    print(f"Formato inválido en vértice {i+1}: {texto}")

        # Enviar al controlador y graficar
        if num_vertices > 0 and len(vertices) == num_vertices:
            from services.controller import ControladorGrafico  

            # Por ahora solo graficamos los originales
            datos = ControladorGrafico.preparar(vertices)

            # Dibujar el polígono original
            self.canvas.plot_polygon(datos["original"])

            print("Vértices enviados y graficados:", vertices)
        else:
            print("Error: No se enviaron los vértices")


# Bloque principal que se ejecuta cuando se corre el script directamente.
if __name__ == "__main__":
    # Crea la aplicación Qt.
    app = QApplication(sys.argv)
    # Instancia la ventana principal de la aplicación.
    ventana = VentanaTransformaciones()
    # Muestra la ventana en pantalla.
    ventana.show()
    # Ejecuta el loop principal de eventos de la aplicación.
    sys.exit(app.exec())