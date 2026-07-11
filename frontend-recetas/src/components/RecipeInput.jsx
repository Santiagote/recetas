import { useState } from "react";

export default function RecipeInput({ onCompilar, loading }) {
  const [oracion, setOracion] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!oracion.trim()) return;
    onCompilar(oracion.trim());
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <input
        type="text"
        value={oracion}
        onChange={(e) => setOracion(e.target.value)}
        placeholder='Ej: "agregar 2 tazas de harina"'
        className="flex-1 px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
      />
      <button
        type="submit"
        disabled={loading || !oracion.trim()}
        className="px-6 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? "Compilando..." : "Compilar"}
      </button>
    </form>
  );
}
