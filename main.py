import sys
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox
from gui.ventanas import VentanaTransformaciones
from utils.config import cargar_config

def manejar_errores(exc_type, exc_value, exc_traceback):
    """Muestra los errores en una ventana de diálogo."""
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Error inesperado")
    msg.setText("Ha ocurrido un error en la aplicación.")
    msg.setDetailedText(error_msg)
    msg.exec()

def main():
    # Configurar manejo global de errores
    sys.excepthook = manejar_errores

    # Cargar configuración desde archivo (ej: config.json o .env)
    config = cargar_config("config.json")

    # Crear la aplicación
    app = QApplication(sys.argv)

    # Crear e iniciar la ventana principal
    ventana = VentanaTransformaciones()
    ventana.show()

    # Ejecutar el loop de la app
    sys.exit(app.exec())

if __name__ == "__main__":
    main()