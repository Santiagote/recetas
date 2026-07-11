import os
import httpx
from dataclasses import asdict
from dominio.modelos.nodo_ast import NodoReceta
from dominio.excepciones import ErrorServicioSemantico

URL_SERVICIO_SEMANTICO = os.environ.get(
    "URL_SERVICIO_SEMANTICO", "http://localhost:8080"
)
TIEMPO_MAXIMO = 10


class ClienteSemantico:
    """Cliente HTTP hacia el microservicio de análisis semántico (Java)."""

    def __init__(self, url_base: str = URL_SERVICIO_SEMANTICO):
        self.url = f"{url_base}/validar"

    def validar(self, ast: NodoReceta) -> list[str]:
        payload = asdict(ast)
        try:
            with httpx.Client(timeout=TIEMPO_MAXIMO) as cliente:
                respuesta = cliente.post(self.url, json=payload)
                respuesta.raise_for_status()
                datos = respuesta.json()
                return datos.get("errores_semanticos", [])
        except httpx.RequestError as e:
            raise ErrorServicioSemantico(
                f"No se pudo contactar al servicio semántico: {e}"
            ) from e
        except httpx.HTTPStatusError as e:
            raise ErrorServicioSemantico(
                f"El servicio semántico respondió con error: {e.response.status_code}"
            ) from e