
# Controlador para preparar datos que serán graficados en el CanvasMPL

# Esta clase centraliza la preparación de datos para el gráfico
class ControladorGrafico:
    @staticmethod
    def preparar(vertices, vertices_transformados=None):
        # Recibe los vértices originales y opcionalmente los transformados
        # Arma un diccionario con los datos
        data = {"original": vertices}
        # Si hay vértices transformados, también se agregan al diccionario
        if vertices_transformados is not None:
            data["transformado"] = vertices_transformados
        # Devuelve el diccionario listo para usar en la vista (CanvasMPL)
        return data