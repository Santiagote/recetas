import sqlite3
import os
from datetime import datetime

RUTA_DB = os.environ.get("RUTA_DB", "historial.db")


def _conectar():
    conn = sqlite3.connect(RUTA_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            oracion TEXT,
            nodo TEXT,
            fecha TEXT
        )
    """)
    return conn


def guardar_peticion(oracion: str, nodo: str):
    conn = _conectar()
    conn.execute(
        "INSERT INTO historial (oracion, nodo, fecha) VALUES (?, ?, ?)",
        (oracion, nodo, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def listar_historial():
    conn = _conectar()
    filas = conn.execute(
        "SELECT id, oracion, nodo, fecha FROM historial ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return filas