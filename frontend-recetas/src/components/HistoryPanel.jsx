import { useState, useEffect } from "react";
import { obtenerHistorial } from "../services/api";

export default function HistoryPanel({ onSelect }) {
  const [historial, setHistorial] = useState([]);
  const [abierto, setAbierto] = useState(false);

  useEffect(() => {
    if (abierto) {
      obtenerHistorial()
        .then(setHistorial)
        .catch(() => {});
    }
  }, [abierto]);

  function handleClick(oracion) {
    onSelect(oracion);
    setAbierto(false);
  }

  return (
    <>
      <button
        onClick={() => setAbierto(!abierto)}
        className="fixed bottom-6 right-6 z-40 w-12 h-12 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700 transition-colors flex items-center justify-center text-lg"
        title="Historial"
      >
        {abierto ? "✕" : "⌛"}
      </button>

      {abierto && (
        <div className="fixed inset-0 z-30 bg-black/20" onClick={() => setAbierto(false)} />
      )}

      <div
        className={`fixed bottom-20 right-6 z-40 w-80 max-h-96 bg-white border border-gray-200 rounded-xl shadow-xl overflow-hidden transition-all duration-200 ${abierto ? "opacity-100 scale-100" : "opacity-0 scale-95 pointer-events-none"}`}
      >
        <div className="px-4 py-3 border-b border-gray-100">
          <h3 className="text-sm font-semibold text-gray-700">Historial de compilaciones</h3>
        </div>
        <div className="overflow-y-auto max-h-80">
          {historial.length === 0 ? (
            <p className="text-sm text-gray-400 text-center py-6">Sin compilaciones aún</p>
          ) : (
            <ul className="divide-y divide-gray-50">
              {historial.map((item) => (
                <li key={item.id}>
                  <button
                    onClick={() => handleClick(item.oracion)}
                    className="w-full text-left px-4 py-3 hover:bg-gray-50 transition-colors"
                  >
                    <p className="text-sm text-gray-700 truncate">{item.oracion}</p>
                    <p className="text-xs text-gray-400 mt-0.5">
                      {item.fecha} · {item.nodo}
                    </p>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </>
  );
}
