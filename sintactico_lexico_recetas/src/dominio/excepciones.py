class ErrorSintactico(Exception):
    """Error detectado durante el análisis sintáctico (parser)."""
    pass


class ErrorSemantico(Exception):
    """Error detectado durante el análisis semántico."""
    pass


class ErrorServicioSemantico(Exception):
    """Error de comunicación con el microservicio semántico en Java."""
    pass


class ErrorClienteOllama(Exception):
    """Error de comunicación con el servidor local de Ollama."""
    pass