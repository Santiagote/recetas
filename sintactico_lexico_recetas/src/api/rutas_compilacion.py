import os
from dataclasses import asdict
from flask import Blueprint, request, jsonify
from aplicacion.servicio_compilacion import ServicioCompilacion
from infraestructura.repositorio_historial import guardar_peticion, listar_historial

bp_compilacion = Blueprint("compilacion", __name__)
servicio = ServicioCompilacion()

NODO_ID = os.environ.get("NODO_ID", "desconocido")


@bp_compilacion.route("/compilar", methods=["POST"])
def compilar():
    datos = request.get_json()
    if not datos or "oracion" not in datos:
        return jsonify({"error": "Campo 'oracion' requerido"}), 400

    resultado = servicio.compilar(datos["oracion"])
    guardar_peticion(datos["oracion"], NODO_ID)

    # Respuesta resumida: lo que le importa a un usuario/cliente final
    return jsonify({
        "oracion": resultado.oracion_original,
        "ast": asdict(resultado.ast) if resultado.ast else None,
        "valido": not resultado.errores_sintacticos and not resultado.errores_semanticos,
        "errores": resultado.errores_sintacticos + resultado.errores_semanticos,
        "error": resultado.error,
    })


@bp_compilacion.route("/compilar/detalle", methods=["POST"])
def compilar_detalle():
    """Endpoint de depuración: expone tokens, tiempos e hilos para la tabla de observaciones."""
    datos = request.get_json()
    if not datos or "oracion" not in datos:
        return jsonify({"error": "Campo 'oracion' requerido"}), 400

    resultado = servicio.compilar(datos["oracion"])

    return jsonify({
        "tokens": [
            {
                "nombre": t.nombre, "valor": t.valor, "fuente": t.fuente,
                "tiempo_ms": round(t.tiempo_ms, 4), "hilo": t.hilo,
            }
            for t in resultado.tokens
        ],
        "ast": asdict(resultado.ast) if resultado.ast else None,
        "errores_sintacticos": resultado.errores_sintacticos,
        "errores_semanticos": resultado.errores_semanticos,
        "tiempo_total_segundos": resultado.tiempo_total_segundos,
        "hilos_concurrentes": resultado.hilos_concurrentes,
        "oracion_original": resultado.oracion_original,
        "error": resultado.error,
        "nodo": NODO_ID,
    })


@bp_compilacion.route("/historial", methods=["GET"])
def historial():
    filas = listar_historial()
    return jsonify([
        {"id": f[0], "oracion": f[1], "nodo": f[2], "fecha": f[3]} for f in filas
    ])


@bp_compilacion.route("/", methods=["GET"])
def index():
    return {"api": "Compilador de Recetas de Cocina", "version": "2.0", "nodo": NODO_ID}