from dataclasses import dataclass, field
from typing import Optional
from dominio.modelos.nodo_ast import NodoReceta


@dataclass
class Token:
    nombre: str
    valor: str
    fuente: str
    tiempo_ms: float = 0.0
    hilo: str = ""


@dataclass
class ResultadoCompilacion:
    tokens: list[Token]
    tiempo_total_segundos: float
    hilos_concurrentes: int
    oracion_original: str
    ast: Optional[NodoReceta] = None
    errores_sintacticos: list[str] = field(default_factory=list)
    errores_semanticos: list[str] = field(default_factory=list)
    error: Optional[str] = None