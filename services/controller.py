
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

# Controlador para preparar datos 3D que serán graficados en el CanvasMPL3D

class ControladorGrafico3D:
    @staticmethod
    def preparar(vertices, caras=None, vertices_transformados=None):
        """
        Prepara los datos para graficar en 3D.
        :param vertices: lista de puntos [(x,y,z), ...]
        :param caras: lista de caras, cada cara es una lista de índices de vértices
        :param vertices_transformados: opcional, lista de puntos transformados
        """
        data = {"vertices": vertices}
        if caras is not None:
            data["caras"] = caras
        if vertices_transformados is not None:
            data["transformado"] = vertices_transformados
        return data