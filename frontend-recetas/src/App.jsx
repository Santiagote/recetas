import { useState, useCallback } from "react";
import Header from "./components/Header";
import RecipeInput from "./components/RecipeInput";
import ResultPanel from "./components/ResultPanel";
import LoadingSpinner from "./components/LoadingSpinner";
import HistoryPanel from "./components/HistoryPanel";
import { compilar, compilarDetalle } from "./services/api";

function App() {
  const [detalle, setDetalle] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCompilar = useCallback(async (oracion) => {
    setLoading(true);
    setError(null);
    setResultado(null);
    try {
      const fn = detalle ? compilarDetalle : compilar;
      const res = await fn(oracion);
      setResultado(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [detalle]);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header detalle={detalle} onToggleDetalle={() => setDetalle((d) => !d)} />

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 py-8 space-y-6">
        <RecipeInput onCompilar={handleCompilar} loading={loading} />

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">
            {error}
          </div>
        )}

        {loading && <LoadingSpinner />}

        {resultado && <ResultPanel resultado={resultado} detalle={detalle} />}

        {!loading && !resultado && !error && (
          <div className="text-center py-16">
            <p className="text-gray-400 text-sm">
              Escribe una receta y presiona "Compilar" para ver el análisis
            </p>
          </div>
        )}
      </main>

      <HistoryPanel onSelect={handleCompilar} />
    </div>
  );
}

export default App;
