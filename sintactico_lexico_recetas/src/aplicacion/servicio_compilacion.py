from dominio.modelos.token import ResultadoCompilacion
from aplicacion.tonkenizador import Tokenizador
from aplicacion.analizador_sintactico import AnalizadorSintactico
from infraestructura.cliente_semantico import ClienteSemantico
from infraestructura.generador_mensajes_error import GeneradorMensajesError
from dominio.excepciones import ErrorServicioSemantico


class ServicioCompilacion:
    def __init__(self, tokenizador: Tokenizador = None,
                 cliente_semantico: ClienteSemantico = None,
                 generador_errores: GeneradorMensajesError = None):
        self.tokenizador = tokenizador or Tokenizador()
        self.cliente_semantico = cliente_semantico or ClienteSemantico()
        self.generador_errores = generador_errores or GeneradorMensajesError()

    def compilar(self, oracion: str) -> ResultadoCompilacion:
        try:
            resultado_lexico = self.tokenizador.tokenizar(oracion)
            parser = AnalizadorSintactico(resultado_lexico['tokens'])
            ast, errores_sintacticos = parser.parsear()

            errores_semanticos = []
            if not errores_sintacticos:
                try:
                    errores_semanticos = self.cliente_semantico.validar(ast)
                except ErrorServicioSemantico as e:
                    errores_semanticos = [str(e)]

            errores_sintacticos = [
                self.generador_errores.humanizar(e) for e in errores_sintacticos
            ]
            errores_semanticos = [
                self.generador_errores.humanizar(e) for e in errores_semanticos
            ]

            return ResultadoCompilacion(
                tokens=resultado_lexico['tokens'],
                tiempo_total_segundos=resultado_lexico['tiempo_total_segundos'],
                hilos_concurrentes=resultado_lexico['hilos_concurrentes'],
                oracion_original=resultado_lexico['oracion_original'],
                ast=ast,
                errores_sintacticos=errores_sintacticos,
                errores_semanticos=errores_semanticos,
            )
        except Exception as e:
            return ResultadoCompilacion(
                tokens=[], tiempo_total_segundos=0.0, hilos_concurrentes=0,
                oracion_original=oracion, error=str(e),
            )