export default function ErrorList({ errores }) {
  if (!errores || errores.length === 0) return null;

  return (
    <div>
      <h3 className="text-sm font-semibold text-red-700 mb-2">
        Errores ({errores.length})
      </h3>
      <ul className="space-y-1">
        {errores.map((err, i) => (
          <li
            key={i}
            className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-md px-3 py-2"
          >
            {err}
          </li>
        ))}
      </ul>
    </div>
  );
}
