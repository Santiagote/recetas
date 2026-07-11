from infraestructura.cliente_ollama import ClienteOllama
from dominio.excepciones import ErrorClienteOllama

PROMPT_SISTEMA_ERRORES = """Eres un asistente que reformula mensajes de error tecnicos
de un compilador de recetas en explicaciones claras y breves para un usuario no tecnico.
No agregues informacion que no este en el mensaje original. Responde en una sola oracion,
en español, sin tecnicismos como "token" o "AST". No uses JSON, responde solo con texto plano."""


class GeneradorMensajesError:
    def __init__(self):
        self.cliente = ClienteOllama()

    def humanizar(self, mensaje_tecnico: str) -> str:
        try:
            return self.cliente.consultar(PROMPT_SISTEMA_ERRORES, mensaje_tecnico)
        except ErrorClienteOllama:
            return mensaje_tecnico