from dataclasses import dataclass, field
from typing import Optional


@dataclass
class NodoIngrediente:
    nombre: str
    cantidad: Optional[str] = None
    unidad: Optional[str] = None


@dataclass
class NodoInstruccion:
    tipo: str
    ingredientes: list[NodoIngrediente] = field(default_factory=list)
    tiempo: Optional[str] = None
    unidad_tiempo: Optional[str] = None


@dataclass
class NodoReceta:
    instrucciones: list[NodoInstruccion] = field(default_factory=list)