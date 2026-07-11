import re
import time
import threading
from dominio.modelos.token import Token
from aplicacion.estrategias.estrategia_tokenizacion import EstrategiaTokenizacion


class EstrategiaAutomata(EstrategiaTokenizacion):
    def __init__(self):
        self.patrones = [
            (r'\d+', 'NUMERO'),
        ]

    def tokenizar(self, texto: str) -> list[Token]:
        return [t for t, _, _ in self.tokenizar_con_posiciones(texto)]

    def tokenizar_con_posiciones(self, texto: str) -> list[tuple[Token, int, int]]:
        resultados = []
        nombre_hilo = threading.current_thread().name
        for patron, nombre_token in self.patrones:
            inicio = time.perf_counter()
            for match in re.finditer(patron, texto):
                token = Token(
                    nombre=nombre_token,
                    valor=match.group(),
                    fuente='AFD',
                    tiempo_ms=(time.perf_counter() - inicio) * 1000,
                    hilo=nombre_hilo,
                )
                resultados.append((token, match.start(), match.end()))
        resultados.sort(key=lambda x: x[1])
        return resultados