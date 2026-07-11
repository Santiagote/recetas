from dominio.modelos.token import Token
from dominio.modelos.nodo_ast import NodoReceta, NodoInstruccion, NodoIngrediente
from dominio.excepciones import ErrorSintactico


class AnalizadorSintactico:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def _actual(self) -> Token | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _avanzar(self) -> Token:
        tok = self._actual()
        self.pos += 1
        return tok

    def _match(self, *nombres: str) -> bool:
        tok = self._actual()
        return tok is not None and tok.nombre in nombres

    def _siguiente_es_ingrediente(self) -> bool:
        """Mira el token despues de CONECTOR_Y para decidir si es otro
        ingrediente (misma instruccion) o el inicio de una nueva instruccion."""
        siguiente = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
        if siguiente is None:
            return False
        return not siguiente.nombre.startswith("INSTRUCCION_")

    def parsear(self) -> tuple[NodoReceta, list[str]]:
        instrucciones = []
        errores = []
        while self._actual() is not None:
            if self._match("CONECTOR_Y"):
                self._avanzar()
                continue
            try:
                instrucciones.append(self._instruccion())
            except ErrorSintactico as e:
                errores.append(str(e))
                self._avanzar()
        return NodoReceta(instrucciones=instrucciones), errores

    def _instruccion(self) -> NodoInstruccion:
        tok = self._actual()
        if tok is None or not tok.nombre.startswith("INSTRUCCION_"):
            encontrado = tok.nombre if tok else "FIN_DE_ENTRADA"
            raise ErrorSintactico(f"Se esperaba una instruccion, se encontro '{encontrado}'.")
        self._avanzar()
        tipo = tok.nombre

        if tipo == "INSTRUCCION_AGREGAR":
            ingredientes = [self._ingrediente()]
            while self._match("CONECTOR_Y") and self._siguiente_es_ingrediente():
                self._avanzar()
                ingredientes.append(self._ingrediente())
            return NodoInstruccion(tipo=tipo, ingredientes=ingredientes)

        if tipo in ("INSTRUCCION_HORNEAR", "INSTRUCCION_REPOSAR"):
            if self._match("CONECTOR_POR"):
                self._avanzar()
            cantidad, unidad = self._tiempo()
            return NodoInstruccion(tipo=tipo, tiempo=cantidad, unidad_tiempo=unidad)

        if tipo == "INSTRUCCION_MEZCLAR":
            cantidad = unidad = None
            if self._match("CONECTOR_POR"):
                self._avanzar()
                cantidad, unidad = self._tiempo()
            return NodoInstruccion(tipo=tipo, tiempo=cantidad, unidad_tiempo=unidad)

        if tipo == "INSTRUCCION_CORTAR":
            ingredientes = [self._ingrediente()] if self._match("INGREDIENTE") else []
            return NodoInstruccion(tipo=tipo, ingredientes=ingredientes)

        raise ErrorSintactico(f"Instruccion no soportada por la gramatica: '{tipo}'.")

    def _ingrediente(self) -> NodoIngrediente:
        cantidad = unidad = None
        if self._match("CANTIDAD", "NUMERO"):
            cantidad = self._avanzar().valor
        if self._match("CONECTOR_DE"):
            self._avanzar()
        if self._match("UNIDAD_VOLUMEN", "UNIDAD_MASA", "UNIDAD_UNIDAD"):
            unidad = self._avanzar().nombre
            if self._match("CONECTOR_DE"):
                self._avanzar()
        if not self._match("INGREDIENTE"):
            tok = self._actual()
            encontrado = tok.nombre if tok else "FIN_DE_ENTRADA"
            raise ErrorSintactico(f"Se esperaba INGREDIENTE, se encontro '{encontrado}'.")
        nombre = self._avanzar().valor
        return NodoIngrediente(nombre=nombre, cantidad=cantidad, unidad=unidad)

    def _tiempo(self) -> tuple[str, str]:
        if not self._match("CANTIDAD", "NUMERO"):
            tok = self._actual()
            encontrado = tok.nombre if tok else "FIN_DE_ENTRADA"
            raise ErrorSintactico(f"Se esperaba una cantidad de tiempo, se encontro '{encontrado}'.")
        cantidad = self._avanzar().valor
        if not self._match("UNIDAD_TIEMPO"):
            tok = self._actual()
            encontrado = tok.nombre if tok else "FIN_DE_ENTRADA"
            raise ErrorSintactico(f"Se esperaba UNIDAD_TIEMPO, se encontro '{encontrado}'.")
        unidad = self._avanzar().valor
        return cantidad, unidad