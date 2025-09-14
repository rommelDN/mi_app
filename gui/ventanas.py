import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QSplitter,QRadioButton,QButtonGroup
)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Este archivo contiene la interfaz gráfica principal de la aplicación.
# - sys: se usa para ejecutar la aplicación Qt y manejar argumentos de línea de comandos.
# - PySide6.QtWidgets: proporciona los widgets necesarios para construir la interfaz (ventanas, layouts, botones, inputs, etc.).
# - PySide6.QtCore.Qt: se usa para definir orientaciones y comportamientos específicos como la orientación del splitter.
# - matplotlib.backends.backend_qtagg.FigureCanvasQTAgg: permite incrustar gráficos de Matplotlib dentro de widgets Qt.
# - matplotlib.figure.Figure: se utiliza para crear las figuras que se graficarán en el canvas.

# Definición de la clase principal de la ventana de la aplicación,
# que hereda de QMainWindow para aprovechar sus funcionalidades.
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
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        # Activar la malla para facilitar la visualización de la gráfica.
        self.ax.grid(True)
    def plot_polygon(self, vertices):
        # Limpiar el gráfico anterior para dibujar uno nuevo.
        self.ax.clear()
        if vertices:
            # Cerrar el polígono conectando el último vértice con el primero.
            polygon = vertices + [vertices[0]]
            # Separar las coordenadas X e Y para graficar.
            xs, ys = zip(*polygon)
            # Dibujar el polígono con línea azul.
            self.ax.plot(xs, ys, 'b-')
        # Mantener la relación de aspecto cuadrada.
        self.ax.set_aspect('equal')
        # Reactivar la malla tras limpiar el gráfico.
        self.ax.grid(True)
        # Reestablecer los límites de los ejes.
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        # Redibujar el canvas para mostrar los cambios.
        self.draw()

class VentanaTransformaciones(QMainWindow):
    # Ventana principal de la aplicación que contiene la interfaz y la lógica de interacción.
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

        # Botones de radio para escoger cantidad de vértices (3, 4 o 5).
        self.btn_vertices1 = QRadioButton("3")
        self.btn_vertices2 = QRadioButton("4")
        self.btn_vertices3 = QRadioButton("5")

        # Agrupamos los botones para que solo uno pueda estar seleccionado a la vez.
        self.grupo_vertices = QButtonGroup()
        self.grupo_vertices.addButton(self.btn_vertices1, 3)
        self.grupo_vertices.addButton(self.btn_vertices2, 4)
        self.grupo_vertices.addButton(self.btn_vertices3, 5)

        # Añadimos los botones al layout izquierdo.
        layout_izq.addWidget(self.btn_vertices1)
        layout_izq.addWidget(self.btn_vertices2)
        layout_izq.addWidget(self.btn_vertices3)

        # Etiqueta para el ingreso de los vértices.
        layout_izq.addWidget(QLabel("Ingresar Vértices:"))
        # Crear inputs de vértices (máximo 5, pero inicialmente ocultos).
        self.inputs_vertices = []
        for i in range(5):
            input_v = QLineEdit()
            input_v.setPlaceholderText(f"Vértice {i+1} (x,y)")
            input_v.hide()  # Ocultar por defecto hasta que se seleccione la cantidad.
            self.inputs_vertices.append(input_v)
            layout_izq.addWidget(input_v)
        
        # Conectar evento para actualizar los inputs visibles según la cantidad de vértices seleccionada.
        self.grupo_vertices.buttonToggled.connect(self.actualizar_vertices)
        
        # Opciones para fijar el vértice de rotación.
        layout_izq.addWidget(QLabel("Fijar Vertice de Rotacion:"))
        self.btn_fijar1 = QRadioButton("Centro")
        self.btn_fijar2 = QRadioButton("Escoger")
        self.grupo_fijar = QButtonGroup()
        self.grupo_fijar.addButton(self.btn_fijar1, 5)
        self.grupo_fijar.addButton(self.btn_fijar2, 6)
        layout_izq.addWidget(self.btn_fijar1)
        layout_izq.addWidget(self.btn_fijar2)

        # Input para escoger punto de rotación, oculto por defecto.
        self.input_punto = QLineEdit()
        self.input_punto.setPlaceholderText("Punto(0,0)")
        self.input_punto.hide()
        layout_izq.addWidget(self.input_punto)

        # Conectar evento para mostrar u ocultar el input según la opción de fijar vértice seleccionada.
        self.grupo_fijar.buttonToggled.connect(self.actualizar_fijar)

        # Inputs para rotar en los ejes X, Y y Z.
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
        # Conectar el clic del botón a la función que procesa y envía los vértices.
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
        # Método que muestra u oculta los inputs de vértices según la cantidad seleccionada.
        if checked:
            # Obtener la cantidad de vértices seleccionada a partir del id del botón.
            cantidad = self.grupo_vertices.id(button)
            # Mostrar solo los inputs necesarios y ocultar el resto.
            for i, input_v in enumerate(self.inputs_vertices):
                if i < cantidad:
                    input_v.show()
                else:
                    input_v.hide()
    def actualizar_fijar(self, button, checked):
        # Método que muestra u oculta el input para escoger punto de rotación.
        if not checked:
            # Solo actuar cuando el botón se activa.
            return
        if button.text() == "Centro":
            # Si se selecciona "Centro", ocultar el input de punto personalizado.
            pass
            self.input_punto.hide()
        elif button.text() == "Escoger":
            # Si se selecciona "Escoger", mostrar el input para ingresar el punto.
            self.input_punto.show()
        else:
            # Por defecto, ocultar el input.
            self.input_punto.hide()
    
    def enviar_vertices(self):
        # Método que recoge los vértices ingresados, valida y envía para graficar.
        # Número de vértices seleccionados (por defecto 0).
        num_vertices = 0
        # Revisar qué botón de cantidad de vértices está seleccionado.
        for btn in self.grupo_vertices.buttons():
            if btn.isChecked():
                num_vertices = self.grupo_vertices.id(btn)

        # Recolectar los vértices escritos en los inputs.
        vertices = []
        for i in range(num_vertices):
            texto = self.inputs_vertices[i].text()
            if texto:
                try:
                    # Espera formato: "x,y" (sin paréntesis o con ellos).
                    x, y = map(float, texto.strip("() ").split(","))
                    vertices.append((x, y))
                except Exception:
                    # Imprimir mensaje de error si el formato no es válido.
                    print(f"Formato inválido en vértice {i+1}: {texto}")

        # Si la cantidad de vértices es correcta y todos están bien formateados.
        if num_vertices > 0 and len(vertices) == num_vertices:
            # Importar el controlador que procesa los datos para graficar.
            from services.controller import ControladorGrafico  

            # Preparar los datos para graficar (por ahora solo originales).
            datos = ControladorGrafico.preparar(vertices)

            # Dibujar el polígono original en el canvas.
            self.canvas.plot_polygon(datos["original"])

            # Mensaje de confirmación en consola.
            print("Vértices enviados y graficados:", vertices)
        else:
            # Mensaje de error si no se enviaron correctamente los vértices.
            print("Error: No se enviaron los vértices")


# Bloque principal que se ejecuta cuando se corre el script directamente.
if __name__ == "__main__":
    # Crear la aplicación Qt.
    app = QApplication(sys.argv)
    # Instanciar la ventana principal de la aplicación.
    ventana = VentanaTransformaciones()
    # Mostrar la ventana en pantalla.
    ventana.show()
    # Ejecutar el loop principal de eventos de la aplicación.
    sys.exit(app.exec())