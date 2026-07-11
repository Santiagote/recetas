import time
import threading
from dominio.modelos.token import Token
from aplicacion.estrategias.estrategia_tokenizacion import EstrategiaTokenizacion

TABLA_TOKENS = {
    "agregar": "INSTRUCCION_AGREGAR", "añadir": "INSTRUCCION_AGREGAR",
    "echar": "INSTRUCCION_AGREGAR", "poner": "INSTRUCCION_AGREGAR",
    "mezclar": "INSTRUCCION_MEZCLAR", "revolver": "INSTRUCCION_MEZCLAR",
    "batir": "INSTRUCCION_MEZCLAR", "remover": "INSTRUCCION_MEZCLAR",
    "hornear": "INSTRUCCION_HORNEAR",
    "reposar": "INSTRUCCION_REPOSAR", "enfriar": "INSTRUCCION_REPOSAR",
    "cortar": "INSTRUCCION_CORTAR", "picar": "INSTRUCCION_CORTAR", "rebanar": "INSTRUCCION_CORTAR",
    "un": "CANTIDAD", "una": "CANTIDAD", "dos": "CANTIDAD", "tres": "CANTIDAD",
    "media": "CANTIDAD", "par": "CANTIDAD", "cero": "CANTIDAD",
    "taza": "UNIDAD_VOLUMEN", "tazas": "UNIDAD_VOLUMEN", "litro": "UNIDAD_VOLUMEN",
    "litros": "UNIDAD_VOLUMEN", "ml": "UNIDAD_VOLUMEN", "cucharada": "UNIDAD_VOLUMEN",
    "cucharadas": "UNIDAD_VOLUMEN",
    "kilo": "UNIDAD_MASA", "kilos": "UNIDAD_MASA", "gramo": "UNIDAD_MASA",
    "gramos": "UNIDAD_MASA", "libra": "UNIDAD_MASA", "libras": "UNIDAD_MASA",
    "onza": "UNIDAD_MASA", "onzas": "UNIDAD_MASA",
    "minuto": "UNIDAD_TIEMPO", "minutos": "UNIDAD_TIEMPO", "hora": "UNIDAD_TIEMPO",
    "horas": "UNIDAD_TIEMPO", "segundo": "UNIDAD_TIEMPO", "segundos": "UNIDAD_TIEMPO",
    "unidad": "UNIDAD_UNIDAD", "unidades": "UNIDAD_UNIDAD", "pieza": "UNIDAD_UNIDAD",
    "piezas": "UNIDAD_UNIDAD",
    "harina": "INGREDIENTE", "azucar": "INGREDIENTE", "huevo": "INGREDIENTE",
    "huevos": "INGREDIENTE", "leche": "INGREDIENTE", "sal": "INGREDIENTE",
    "aceite": "INGREDIENTE",
    "y": "CONECTOR_Y", "e": "CONECTOR_Y",
    "por": "CONECTOR_POR",
    "de": "CONECTOR_DE", "del": "CONECTOR_DE",
}


class EstrategiaDiccionario(EstrategiaTokenizacion):
    """Clasifica palabras de lenguaje natural usando una tabla de busqueda
    determinista (sin IA). Esta es la logica real de tokenizacion."""

    def tokenizar(self, texto: str) -> list[Token]:
        return [t for t, _ in self.tokenizar_con_posiciones(texto)]

    def tokenizar_con_posiciones(self, texto: str) -> list[tuple[Token, int]]:
        nombre_hilo = threading.current_thread().name
        resultados = []
        cursor = 0
        for palabra in texto.split():
            palabra_normalizada = palabra.lower().strip(".,;:")
            inicio = time.perf_counter()
            nombre_token = TABLA_TOKENS.get(palabra_normalizada, "TEXTO_NO_RECONOCIDO")
            tiempo_ms = (time.perf_counter() - inicio) * 1000
            token = Token(
                nombre=nombre_token,
                valor=palabra,
                fuente='DICCIONARIO',
                tiempo_ms=tiempo_ms,
                hilo=nombre_hilo,
            )
            pos = texto.find(palabra, cursor)
            resultados.append((token, pos))
            cursor = pos + len(palabra)
        return resultados