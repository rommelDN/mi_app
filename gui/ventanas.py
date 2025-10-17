# ==============================
# IMPORTS
# ==============================
import sys
import numpy as np

# PySide6
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QSplitter,
    QRadioButton,
    QButtonGroup,
    QMessageBox,
)
from PySide6.QtCore import Qt

# Local imports
from gui.canvasmpl import CanvasMPL, CanvasMPL3D
from services.rotacion_general import rotacion_general, rotacion_general_3d
from services.reflexion import reflexion
from services.homotencia import homotencia, homotencia_3d


# ==============================
# CLASE PRINCIPAL
# ==============================
class VentanaTransformaciones(QMainWindow):
    """Ventana principal de la aplicación con interfaz y lógica de interacción."""

    def __init__(self):
        """Constructor de la ventana principal: inicializa y organiza la interfaz."""
        super().__init__()

        # -----------------------------
        # CONFIGURACIÓN DE LA VENTANA
        # -----------------------------
        self.setWindowTitle(
            "UPC - PROYECTO DE TRANSFORMACIONES LINEALES"
        )  # Título de la ventana
        self.showMaximized()  # Abrir maximizada

        # Splitter principal (divide en panel izquierdo y derecho)
        splitter = QSplitter(Qt.Horizontal)

        # -----------------------------
        # PANEL IZQUIERDO (Inputs y controles)
        # -----------------------------
        panel_izq = QWidget()
        layout_izq = QVBoxLayout()
        layout_izq.setContentsMargins(20, 20, 20, 20)
        
        label_menu = QLabel("MENU")
        label_menu.setAlignment(Qt.AlignCenter)  # Centrar el texto
        layout_izq.addWidget(label_menu)
        
        separador0 = QFrame()
        separador0.setFrameShape(QFrame.HLine)  # Línea horizontal
        separador0.setFrameShadow(QFrame.Sunken)  # Efecto de sombra
        separador0.setLineWidth(1)  # Grosor de la línea
        separador0.setStyleSheet("background-color: #c0c0c0; margin: 10px 0px;")  # Color y márgenes
        layout_izq.addWidget(separador0)
        
        # --- Selección de figuras 2D ---
        layout_izq.addWidget(QLabel("Escoger Figura:"))
        self.btn_triangulo = QRadioButton("Triángulo")
        self.btn_cuadrado = QRadioButton("Cuadrado")
        self.btn_hexagono = QRadioButton("Hexágono")
        for btn in (self.btn_triangulo, self.btn_cuadrado, self.btn_hexagono):
            btn.setAutoExclusive(False)
            btn.toggled.connect(lambda checked, b=btn: self.toggle_radio(b, checked))
            layout_izq.addWidget(btn)
        self.grupo_figuras = QButtonGroup()
        self.grupo_figuras.addButton(self.btn_triangulo, 3)
        self.grupo_figuras.addButton(self.btn_cuadrado, 4)
        self.grupo_figuras.addButton(self.btn_hexagono, 6)
        self.grupo_figuras.setExclusive(False)
        self.grupo_figuras.buttonToggled.connect(self.dibujar_figura)
        
        # --- BARRA DE SEPARACIÓN ---
        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)  # Línea horizontal
        separador.setFrameShadow(QFrame.Sunken)  # Efecto de sombra
        separador.setLineWidth(1)  # Grosor de la línea
        separador.setStyleSheet("background-color: #c0c0c0; margin: 10px 0px;")  # Color y márgenes
        layout_izq.addWidget(separador)
        
        # --- Selección de figuras 3D ---
        layout_izq.addWidget(QLabel("Escoger Figura 3D:"))
        self.btn_cubo = QRadioButton("Cubo")
        self.btn_cubo.setAutoExclusive(False)
        self.btn_cubo.toggled.connect(
            lambda checked: self.toggle_radio(self.btn_cubo, checked)
        )
        layout_izq.addWidget(self.btn_cubo)
        self.grupo_figuras3D = QButtonGroup()
        self.grupo_figuras3D.addButton(self.btn_cubo, 1)
        self.grupo_figuras3D.setExclusive(False)
        self.grupo_figuras3D.buttonToggled.connect(self.dibujar_figura3D)
        
        separador1 = QFrame()
        separador1.setFrameShape(QFrame.HLine)  # Línea horizontal
        separador1.setFrameShadow(QFrame.Sunken)  # Efecto de sombra
        separador1.setLineWidth(1)  # Grosor de la línea
        separador1.setStyleSheet("background-color: #c0c0c0; margin: 10px 0px;")  # Color y márgenes
        layout_izq.addWidget(separador1)
        
        # --- Opciones de rotación 2D ---
        layout_izq.addWidget(QLabel("Fijar Vértice de Rotación:"))
        self.btn_fijar1 = QRadioButton("Centro")
        self.btn_fijar2 = QRadioButton("Escoger")
        for btn in (self.btn_fijar1, self.btn_fijar2):
            btn.setAutoExclusive(False)
            btn.toggled.connect(lambda checked, b=btn: self.toggle_radio(b, checked))
            layout_izq.addWidget(btn)
        self.grupo_fijar = QButtonGroup()
        self.grupo_fijar.addButton(self.btn_fijar1, 5)
        self.grupo_fijar.addButton(self.btn_fijar2, 6)
        self.grupo_fijar.setExclusive(False)
        self.grupo_fijar.buttonToggled.connect(self.actualizar_fijar)
        self.input_punto = QLineEdit()
        
        separador2 = QFrame()
        separador2.setFrameShape(QFrame.HLine)  # Línea horizontal
        separador2.setFrameShadow(QFrame.Sunken)  # Efecto de sombra
        separador2.setLineWidth(1)  # Grosor de la línea
        separador2.setStyleSheet("background-color: #c0c0c0; margin: 10px 0px;")  # Color y márgenes
        layout_izq.addWidget(separador2)
        
        self.input_punto.setPlaceholderText("Punto(0,0)")
        self.input_punto.hide()
        layout_izq.addWidget(self.input_punto)
        layout_izq.addWidget(QLabel("Rotar en el eje X:"))
        self.input_x = QLineEdit()
        self.input_x.setPlaceholderText("Grados(0°)")
        layout_izq.addWidget(self.input_x)
        
        separador3 = QFrame()
        separador3.setFrameShape(QFrame.HLine)  # Línea horizontal
        separador3.setFrameShadow(QFrame.Sunken)  # Efecto de sombra
        separador3.setLineWidth(1)  # Grosor de la línea
        separador3.setStyleSheet("background-color: #c0c0c0; margin: 10px 0px;")  # Color y márgenes
        layout_izq.addWidget(separador3)
        
        # --- Reflexión ---
        layout_izq.addWidget(QLabel("Aplicar Reflexión a la Figura:"))
        self.btn_reflexion = QRadioButton("Reflexión")
        self.btn_reflexion.setAutoExclusive(False)
        self.btn_reflexion.toggled.connect(
            lambda checked: self.toggle_radio(self.btn_reflexion, checked)
        )
        layout_izq.addWidget(self.btn_reflexion)
        self.grupo_reflexion = QButtonGroup()
        self.grupo_reflexion.addButton(self.btn_reflexion, 7)
        self.grupo_reflexion.setExclusive(False)
        
        separador4 = QFrame()
        separador4.setFrameShape(QFrame.HLine)  # Línea horizontal
        separador4.setFrameShadow(QFrame.Sunken)  # Efecto de sombra
        separador4.setLineWidth(1)  # Grosor de la línea
        separador4.setStyleSheet("background-color: #c0c0c0; margin: 10px 0px;")  # Color y márgenes
        layout_izq.addWidget(separador4)
        
        # --- Homotecia ---
        layout_izq.addWidget(QLabel("Aplicar Homotecia a la Figura 2D:"))
        self.input_homot_k = QLineEdit()
        self.input_homot_k.setPlaceholderText("Factor k (ej. 2.0)")
        layout_izq.addWidget(self.input_homot_k)
        self.input_homot_centro = QLineEdit()
        self.input_homot_centro.setPlaceholderText("Centro (x,y) opcional")
        layout_izq.addWidget(self.input_homot_centro)
        self.btn_homotencia = QRadioButton("Homotecia")
        self.btn_homotencia.setAutoExclusive(False)
        self.btn_homotencia.toggled.connect(
            lambda checked: self.toggle_radio(self.btn_homotencia, checked)
        )
        layout_izq.addWidget(self.btn_homotencia)
        self.grupo_homotencia = QButtonGroup()
        self.grupo_homotencia.addButton(self.btn_homotencia, 8)
        self.grupo_homotencia.setExclusive(False)
        
        separador5 = QFrame()
        separador5.setFrameShape(QFrame.HLine)  # Línea horizontal
        separador5.setFrameShadow(QFrame.Sunken)  # Efecto de sombra
        separador5.setLineWidth(1)  # Grosor de la línea
        separador5.setStyleSheet("background-color: #c0c0c0; margin: 10px 0px;")  # Color y márgenes
        layout_izq.addWidget(separador5)
        
        # --- Rotación 3D ---
        layout_izq.addWidget(QLabel("Rotar figura 3D (en grados):"))
        self.input_rx = QLineEdit()
        self.input_rx.setPlaceholderText("Ángulo eje X")
        self.input_ry = QLineEdit()
        self.input_ry.setPlaceholderText("Ángulo eje Y")
        self.input_rz = QLineEdit()
        self.input_rz.setPlaceholderText("Ángulo eje Z")
        for input_widget in (self.input_rx, self.input_ry, self.input_rz):
            layout_izq.addWidget(input_widget)
            
        separador6 = QFrame()
        separador6.setFrameShape(QFrame.HLine)  # Línea horizontal
        separador6.setFrameShadow(QFrame.Sunken)  # Efecto de sombra
        separador6.setLineWidth(1)  # Grosor de la línea
        separador6.setStyleSheet("background-color: #c0c0c0; margin: 10px 0px;")  # Color y márgenes
        layout_izq.addWidget(separador6)

        layout_izq.addWidget(QLabel("Aplicar Homotecia a la Figura 3D:"))
        self.input_homot_k_3D = QLineEdit()
        self.input_homot_k_3D.setPlaceholderText("Factor k (ej. 2.0)")
        layout_izq.addWidget(self.input_homot_k_3D)
        self.input_homot_centro_3D = QLineEdit()
        self.input_homot_centro_3D.setPlaceholderText("Centro (x,y) opcional")
        layout_izq.addWidget(self.input_homot_centro_3D)
        self.btn_homotencia_3D = QRadioButton("Homotecia 3D")
        self.btn_homotencia_3D.setAutoExclusive(False)
        self.btn_homotencia_3D.toggled.connect(
            lambda checked: self.toggle_radio(self.btn_homotencia_3D, checked)
        )
        layout_izq.addWidget(self.btn_homotencia_3D)
        self.grupo_homotencia_3D = QButtonGroup()
        self.grupo_homotencia_3D.addButton(self.btn_homotencia_3D, 8)
        self.grupo_homotencia_3D.setExclusive(False)
        
        
        
        # --- Botón aplicar ---
        self.btn_aplicar = QPushButton("Aplicar transformación")
        self.btn_aplicar.clicked.connect(self.aplicar_trasformacion)
        layout_izq.addWidget(self.btn_aplicar)

        layout_izq.addStretch()
        panel_izq.setLayout(layout_izq)

        # -----------------------------
        # PANEL DERECHO (Canvas 2D y 3D)
        # -----------------------------
        self.canvas = CanvasMPL()
        self.canvas3d = CanvasMPL3D()
        splitter_der = QSplitter(Qt.Vertical)
        splitter_der.addWidget(self.canvas)
        splitter_der.addWidget(self.canvas3d)

        # Añadir paneles al splitter principal
        splitter.addWidget(panel_izq)
        splitter.addWidget(splitter_der)
        splitter.setSizes([300, 900])
        self.setCentralWidget(splitter)

        # -----------------------------
        # ESTADO INICIAL
        # -----------------------------
        self.vertices_actuales = []

    def dibujar_figura(self, button, checked):
        if not checked:
            # Limpiar el canvas si se desmarca la figura
            self.canvas.plot_polygon([])
            self.vertices_actuales = []
            return

        if not self.canvas.isVisible():
            QMessageBox.warning(
                self,
                "Advertencia",
                "La pestaña de 2D está minimizada, por favor expándala.",
            )
            button.setChecked(False)
            return

        if button.text() == "Triángulo":
            vertices = [(1, 1), (4, 1), (2.5, 4)]
        elif button.text() == "Cuadrado":
            vertices = [(1, 1), (4, 1), (4, 4), (1, 4)]
        elif button.text() == "Hexágono":
            # Un hexágono regular centrado en (2.5,2.5) con radio 2
            vertices = []
            centro = (2.5, 2.5)
            radio = 2
            for i in range(6):
                ang = 2 * np.pi * i / 6
                x = centro[0] + radio * np.cos(ang)
                y = centro[1] + radio * np.sin(ang)
                vertices.append((x, y))
        else:
            vertices = []

        if vertices:
            # Importar controlador
            from services.controller import ControladorGrafico

            datos = ControladorGrafico.preparar(vertices)
            self.canvas.plot_polygon(datos["original"])
            self.vertices_actuales = vertices
            

    def dibujar_figura3D(self, button, checked):
        if not checked:
            # Limpiar el canvas 3D si se desmarca la figura
            self.canvas3d.plot_polyhedron([], [])
            button.setChecked(False)
            return
        if not self.canvas3d.isVisible():
            QMessageBox.warning(
                self,
                "Advertencia",
                "La pestaña de 3D está minimizada, por favor expándala.",
            )
            button.setChecked(False)
            return
        if button.text() == "Cubo":
            # Vértices de un cubo centrado en el origen con lado 4
            vertices = [
                (-2, -2, -2),
                (2, -2, -2),
                (2, 2, -2),
                (-2, 2, -2),
                (-2, -2, 2),
                (2, -2, 2),
                (2, 2, 2),
                (-2, 2, 2),
            ]
            # Caras definidas por índices de vértices
            caras = [
                [0, 1, 2, 3],
                [4, 5, 6, 7],
                [0, 1, 5, 4],
                [2, 3, 7, 6],
                [1, 2, 6, 5],
                [0, 3, 7, 4],
            ]
        else:
            vertices, caras = [], []
        if vertices:
            self.canvas3d.plot_polyhedron(vertices, caras)
            self.canvas3d.vertices = vertices
            

    def actualizar_fijar(self, button, checked):
        # Mostrar self.input_punto solo si está seleccionado btn_fijar2 ("Escoger")
        if checked:
            if button == self.btn_fijar2:
                self.input_punto.show()
            elif button == self.btn_fijar1:
                self.input_punto.hide()

    def aplicar_trasformacion(self):
        """Aplica la transformación seleccionada (rotación, reflexión, homotecia o rotación 3D)."""

        # -----------------------------
        # Verificar si hay figura 2D o 3D
        # -----------------------------
        has_2d = bool(self.vertices_actuales)
        has_3d = bool(getattr(self.canvas3d, "vertices", None))
        if not has_2d and not has_3d:
            return

        # -----------------------------
        # MANEJO DE FIGURAS 2D
        # -----------------------------
        if has_2d:
            # --- ROTACIÓN 2D ---
            angulo_texto = self.input_x.text().strip()
            aplicar_rotacion = False
            angulo_radianes, centro = None, None

            # Si hay un ángulo ingresado, convertirlo a radianes
            if angulo_texto:
                try:
                    angulo_grados = float(angulo_texto)
                    angulo_radianes = np.deg2rad(angulo_grados)
                    aplicar_rotacion = True
                except ValueError:
                    return
            elif self.btn_fijar2.isChecked():
                # Si se escogió un punto pero no se ingresó ángulo, no se aplica rotación
                return

            if aplicar_rotacion:
                # Determinar centro de rotación
                if self.btn_fijar1.isChecked():
                    # Centroide de la figura
                    xs = [v[0] for v in self.vertices_actuales]
                    ys = [v[1] for v in self.vertices_actuales]
                    centro = (sum(xs) / len(xs), sum(ys) / len(ys))
                elif self.btn_fijar2.isChecked():
                    # Punto ingresado manualmente
                    try:
                        x_str, y_str = self.input_punto.text().split(",")
                        centro = (float(x_str.strip()), float(y_str.strip()))
                    except Exception:
                        return
                else:
                    return

                # Aplicar rotación
                puntos = np.array(self.vertices_actuales, dtype=float)
                centro_np = np.array(centro, dtype=float)
                vertices_rotados = rotacion_general(puntos, angulo_radianes, centro_np)
                self.vertices_actuales = vertices_rotados.tolist()
                self.canvas.plot_polygon(self.vertices_actuales)
                return

            # --- REFLEXIÓN ---
            if self.btn_reflexion.isChecked():
                puntos = np.array(self.vertices_actuales, dtype=float)
                matriz_reflexion = np.array(
                    [[1, 0], [0, -1]]
                )  # Reflexión respecto al eje X
                vertices_reflejados = reflexion(matriz_reflexion, puntos)
                self.vertices_actuales = vertices_reflejados.tolist()
                self.canvas.plot_polygon(self.vertices_actuales)
                return

            # --- HOMOTECIA ---
            if self.btn_homotencia.isChecked():
                puntos = np.array(self.vertices_actuales, dtype=float)
                try:
                    k = float(self.input_homot_k.text().strip())
                except ValueError:
                    return

                # Centro por defecto (origen)
                centro = (0.0, 0.0)
                if self.input_homot_centro.text().strip():
                    try:
                        x_str, y_str = self.input_homot_centro.text().split(",")
                        centro = (float(x_str.strip()), float(y_str.strip()))
                    except Exception:
                        return

                centro_np = np.array(centro, dtype=float)
                vertices_homot = homotencia(puntos, k, centro_np)
                self.vertices_actuales = vertices_homot.tolist()
                self.canvas.plot_polygon(self.vertices_actuales)
                return

        # -----------------------------
        # MANEJO DE FIGURAS 3D
        # -----------------------------
        if has_3d:
            # --- ROTACIÓN 3D ---
            aplicar_rotacion_3D = False
            try:
                # Verificar si hay ángulos ingresados
                ang_x_text = self.input_rx.text().strip()
                ang_y_text = self.input_ry.text().strip()
                ang_z_text = self.input_rz.text().strip()

                # Si al menos un campo tiene valor, aplicar rotación
                if ang_x_text or ang_y_text or ang_z_text:
                    aplicar_rotacion_3D = True
                    ang_x = float(ang_x_text) if ang_x_text else 0.0
                    ang_y = float(ang_y_text) if ang_y_text else 0.0
                    ang_z = float(ang_z_text) if ang_z_text else 0.0
            except ValueError:
                QMessageBox.warning(self, "Error", "Ángulos de rotación 3D inválidos.")
                return

            if aplicar_rotacion_3D:
                # Convertir vértices actuales en array numpy
                puntos3d = np.array(self.canvas3d.vertices, dtype=float)
                if puntos3d.size == 0:
                    return

                # Aplicar rotaciones en cada eje
                if ang_x != 0:
                    puntos3d = rotacion_general_3d(puntos3d, np.deg2rad(ang_x), "x")
                if ang_y != 0:
                    puntos3d = rotacion_general_3d(puntos3d, np.deg2rad(ang_y), "y")
                if ang_z != 0:
                    puntos3d = rotacion_general_3d(puntos3d, np.deg2rad(ang_z), "z")

                # Caras fijas del cubo
                caras = [
                    [0, 1, 2, 3],
                    [4, 5, 6, 7],
                    [0, 1, 5, 4],
                    [2, 3, 7, 6],
                    [1, 2, 6, 5],
                    [0, 3, 7, 4],
                ]

                # Guardar y redibujar
                self.canvas3d.vertices = puntos3d.tolist()
                self.canvas3d.plot_polyhedron(self.canvas3d.vertices, caras)
                return

            # --- HOMOTECIA 3D ---
            if self.btn_homotencia_3D.isChecked():
                puntos3d = np.array(self.canvas3d.vertices, dtype=float)
                if puntos3d.size == 0:
                    return

                try:
                    k = float(self.input_homot_k_3D.text().strip())
                except ValueError:
                    QMessageBox.warning(self, "Error", "Factor de homotecia 3D inválido.")
                    return

                # Centro por defecto (origen)
                centro = (0.0, 0.0, 0.0)
                if self.input_homot_centro_3D.text().strip():
                    try:
                        # Para 3D, el centro puede tener 2 o 3 coordenadas
                        centro_texto = self.input_homot_centro_3D.text().strip()
                        coordenadas = centro_texto.split(",")
                        if len(coordenadas) == 2:
                            centro = (
                                float(coordenadas[0].strip()),
                                float(coordenadas[1].strip()),
                                0.0,
                            )
                        elif len(coordenadas) == 3:
                            centro = (
                                float(coordenadas[0].strip()),
                                float(coordenadas[1].strip()),
                                float(coordenadas[2].strip()),
                            )
                        else:
                            raise ValueError("El centro debe tener 2 o 3 coordenadas")
                    except Exception as e:
                        QMessageBox.warning(
                            self, "Error", f"Formato de centro 3D inválido: {e}"
                        )
                        return

                # Aplicar homotecia 3D
                centro_np = np.array(centro, dtype=float)
                vertices_homot = centro_np + k * (puntos3d - centro_np)

                # Caras fijas del cubo
                caras = [
                    [0, 1, 2, 3],
                    [4, 5, 6, 7],
                    [0, 1, 5, 4],
                    [2, 3, 7, 6],
                    [1, 2, 6, 5],
                    [0, 3, 7, 4],
                ]

                # Guardar y redibujar
                self.canvas3d.vertices = vertices_homot.tolist()
                self.canvas3d.plot_polyhedron(self.canvas3d.vertices, caras)
                return

    def toggle_radio(self, button, checked):
        if checked:
            # Si se activa un botón, se mantiene activado
            button.setChecked(True)
        else:
            # Si se desactiva un botón, se limpia y se desmarca
            button.setChecked(False)


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
