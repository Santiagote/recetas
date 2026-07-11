export default function TokenTable({ tokens }) {
  if (!tokens || tokens.length === 0) return null;

  return (
    <div>
      <h3 className="text-sm font-semibold text-gray-700 mb-2">
        Tokens ({tokens.length})
      </h3>
      <div className="overflow-x-auto border border-gray-200 rounded-lg">
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="text-left px-3 py-2 text-gray-500 font-medium">Nombre</th>
              <th className="text-left px-3 py-2 text-gray-500 font-medium">Valor</th>
              <th className="text-left px-3 py-2 text-gray-500 font-medium">Fuente</th>
              <th className="text-right px-3 py-2 text-gray-500 font-medium">Tiempo (ms)</th>
              <th className="text-right px-3 py-2 text-gray-500 font-medium">Hilo</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {tokens.map((t, i) => (
              <tr key={i} className="hover:bg-gray-50">
                <td className="px-3 py-2 font-mono text-blue-600">{t.nombre}</td>
                <td className="px-3 py-2 font-mono">{t.valor}</td>
                <td className="px-3 py-2">
                  <span className={`inline-block px-1.5 py-0.5 rounded text-xs font-medium ${t.fuente === "llm" ? "bg-purple-100 text-purple-700" : "bg-green-100 text-green-700"}`}>
                    {t.fuente}
                  </span>
                </td>
                <td className="px-3 py-2 text-right font-mono text-gray-500">{t.tiempo_ms}</td>
                <td className="px-3 py-2 text-right font-mono text-gray-500">{t.hilo}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
