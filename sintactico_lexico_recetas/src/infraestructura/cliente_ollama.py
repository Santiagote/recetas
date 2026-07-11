import httpx
from dominio.excepciones import ErrorClienteOllama

MODELO_POR_DEFECTO = "llama3.2:3b"
URL_BASE = "http://localhost:11434"
TIEMPO_MAXIMO = 15


class ClienteOllama:
    def __init__(self, modelo: str = MODELO_POR_DEFECTO):
        self.modelo = modelo
        self.url = f"{URL_BASE}/api/chat"

    def consultar(self, sistema: str, usuario: str, formato_json: bool = False) -> str:
        payload = {
            "model": self.modelo,
            "messages": [
                {"role": "system", "content": sistema},
                {"role": "user", "content": usuario},
            ],
            "stream": False,
            "options": {"temperature": 0},
        }
        if formato_json:
            payload["format"] = "json"

        try:
            with httpx.Client(timeout=TIEMPO_MAXIMO) as cliente:
                respuesta = cliente.post(self.url, json=payload)
                respuesta.raise_for_status()
                return respuesta.json()["message"]["content"].strip()
        except httpx.ConnectError as e:
            raise ErrorClienteOllama(
                "No se pudo conectar con Ollama. ¿Está corriendo en localhost:11434?"
            ) from e
        except httpx.TimeoutException as e:
            raise ErrorClienteOllama(
                f"Ollama no respondió en {TIEMPO_MAXIMO}s (timeout)."
            ) from e
        except httpx.HTTPStatusError as e:
            raise ErrorClienteOllama(
                f"Ollama respondió con error {e.response.status_code}. "
                f"¿Existe el modelo '{self.modelo}'?"
            ) from e