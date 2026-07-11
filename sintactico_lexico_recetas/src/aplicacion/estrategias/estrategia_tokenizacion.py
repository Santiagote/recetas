from abc import ABC, abstractmethod
from dominio.modelos.token import Token


class EstrategiaTokenizacion(ABC):
    @abstractmethod
    def tokenizar(self, texto: str) -> list[Token]:
        pass