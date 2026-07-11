import AstTree from "./AstTree";
import TokenTable from "./TokenTable";
import ErrorList from "./ErrorList";

function Badge({ label, color }) {
  return (
    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-semibold ${color}`}>
      {label}
    </span>
  );
}

export default function ResultPanel({ resultado, detalle }) {
  if (!resultado) return null;

  const { ast, valido, errores, error, tokens, errores_sintacticos, errores_semanticos, oracion_original, tiempo_total_segundos, hilos_concurrentes, nodo } = resultado;

  const sintacticos = errores_sintacticos || [];
  const semanticos = errores_semanticos || [];
  const todosErrores = errores || [];

  return (
    <div className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">
          {error}
        </div>
      )}

      {!error && (
        <>
          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-500">
              {oracion_original && (
                <span className="text-gray-400">Receta: </span>
              )}
              <span className="font-medium text-gray-700">{oracion_original}</span>
            </span>
            {valido !== undefined && (
              valido
                ? <Badge label="Válido" color="bg-green-100 text-green-700" />
                : <Badge label="Inválido" color="bg-red-100 text-red-700" />
            )}
          </div>

          {detalle && (tiempo_total_segundos !== undefined) && (
            <div className="flex gap-4 text-sm text-gray-500">
              <span>Tiempo: <strong>{tiempo_total_segundos.toFixed(3)}s</strong></span>
              <span>Hilos: <strong>{hilos_concurrentes}</strong></span>
              {nodo && <span>Nodo: <strong>{nodo}</strong></span>}
            </div>
          )}

          {todosErrores.length > 0 && <ErrorList errores={todosErrores} />}

          {sintacticos.length > 0 && <ErrorList errores={sintacticos} />}
          {semanticos.length > 0 && <ErrorList errores={semanticos} />}

          {detalle && <TokenTable tokens={tokens} />}

          {ast && <AstTree ast={ast} />}
        </>
      )}
    </div>
  );
}
