# Archivo principal de la aplicación: ejecuta la app, maneja errores globales y abre la ventana principal

# Importar sys para acceder a argumentos del sistema y finalizar procesos
import sys
# Importar traceback para capturar y formatear trazas de errores
import traceback
# Importar componentes de PySide6 para construir interfaces gráficas: QApplication y QMessageBox
from PySide6.QtWidgets import QApplication, QMessageBox
# Importar la ventana principal de la aplicación desde el módulo gui.ventanas
from gui.ventanas import VentanaTransformaciones
# Importar función para cargar configuraciones desde archivo
from utils.config import cargar_config

def manejar_errores(exc_type, exc_value, exc_traceback):
    """Muestra los errores en una ventana de diálogo."""
    # Capturar y formatear la traza completa del error
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    # Construir un mensaje de diálogo para mostrar el error
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)  # Icono de error crítico
    msg.setWindowTitle("Error inesperado")  # Título de la ventana de error
    msg.setText("Ha ocurrido un error en la aplicación.")  # Texto principal del mensaje
    msg.setDetailedText(error_msg)  # Texto detallado con la traza del error
    # Mostrar el diálogo de error al usuario
    msg.exec()

def main():
    # Configurar manejo global de errores para que cualquier excepción no atrapada se muestre con manejar_errores
    sys.excepthook = manejar_errores

    # Cargar configuración desde archivo (ej: config.json o .env)
    config = cargar_config("config.json")

    # Crear la aplicación Qt con los argumentos del sistema
    app = QApplication(sys.argv)

    # Crear e iniciar la ventana principal de la aplicación
    ventana = VentanaTransformaciones()
    ventana.show()

    # Ejecutar el loop principal de la aplicación Qt y salir cuando se cierre
    sys.exit(app.exec())

if __name__ == "__main__":
    main()