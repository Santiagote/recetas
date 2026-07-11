export default function Header({ detalle, onToggleDetalle }) {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Compilador de Recetas</h1>
        <p className="text-sm text-gray-500 mt-0.5">
          Analizador léxico, sintáctico y semántico de recetas de cocina
        </p>
      </div>
      <label className="flex items-center gap-2 cursor-pointer select-none">
        <span className="text-sm text-gray-600">Modo detalle</span>
        <div className="relative">
          <input
            type="checkbox"
            checked={detalle}
            onChange={onToggleDetalle}
            className="sr-only peer"
          />
          <div className="w-10 h-5 bg-gray-300 rounded-full peer-checked:bg-blue-600 transition-colors" />
          <div className="absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow peer-checked:translate-x-5 transition-transform" />
        </div>
      </label>
    </header>
  );
}
