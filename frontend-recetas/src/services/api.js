const API_BASE = "http://localhost:5000";

export async function compilar(oracion) {
  const res = await fetch(`${API_BASE}/compilar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ oracion }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || `Error ${res.status}`);
  }
  return res.json();
}

export async function compilarDetalle(oracion) {
  const res = await fetch(`${API_BASE}/compilar/detalle`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ oracion }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || `Error ${res.status}`);
  }
  return res.json();
}

export async function obtenerHistorial() {
  const res = await fetch(`${API_BASE}/historial`);
  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
}
