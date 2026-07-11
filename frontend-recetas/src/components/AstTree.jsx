import { useState } from "react";

const COLORES_INSTRUCCION = {
  INSTRUCCION_AGREGAR: { bg: "bg-blue-100", text: "text-blue-800", dot: "bg-blue-500" },
  INSTRUCCION_MEZCLAR: { bg: "bg-purple-100", text: "text-purple-800", dot: "bg-purple-500" },
  INSTRUCCION_HORNEAR: { bg: "bg-orange-100", text: "text-orange-800", dot: "bg-orange-500" },
  INSTRUCCION_REPOSAR: { bg: "bg-teal-100", text: "text-teal-800", dot: "bg-teal-500" },
  INSTRUCCION_CORTAR:  { bg: "bg-red-100",   text: "text-red-800",   dot: "bg-red-500" },
};

const ETIQUETA_INSTRUCCION = {
  INSTRUCCION_AGREGAR: "Agregar",
  INSTRUCCION_MEZCLAR: "Mezclar",
  INSTRUCCION_HORNEAR: "Hornear",
  INSTRUCCION_REPOSAR: "Reposar",
  INSTRUCCION_CORTAR:  "Cortar",
};

function IconoChevron({ abierto }) {
  return (
    <span className={`inline-block transition-transform duration-200 ${abierto ? "rotate-0" : "-rotate-90"}`}>
      ▼
    </span>
  );
}

function LineaConectora({ esUltimo }) {
  return (
    <span className="inline-flex flex-col items-center mr-2 select-none text-gray-400">
      <span className="text-sm leading-none">{esUltimo ? "└──" : "├──"}</span>
    </span>
  );
}

function BadgeArbol({ children, colorClasses, size = "sm" }) {
  const sizeClass = size === "xs" ? "text-xs px-1.5 py-0.5" : "text-sm px-2.5 py-1";
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-md font-medium ${sizeClass} ${colorClasses}`}>
      {children}
    </span>
  );
}

function NodoHoja({ etiqueta, valor }) {
  return (
    <div className="flex items-center gap-2 py-0.5">
      <span className="text-xs text-gray-400 font-mono">{etiqueta}:</span>
      <span className="text-sm text-gray-700 font-mono">{valor}</span>
    </div>
  );
}

function NodoIngrediente({ ingrediente, nivel }) {
  const [abierto, setAbierto] = useState(true);
  const tieneHijos = ingrediente.cantidad || ingrediente.unidad;

  return (
    <div>
      <button
        onClick={() => setAbierto(!abierto)}
        className="flex items-center gap-2 w-full text-left py-0.5"
      >
        <span className="text-xs text-gray-400 w-4">{tieneHijos ? <IconoChevron abierto={abierto} /> : " "}</span>
        <BadgeArbol colorClasses="bg-green-100 text-green-700" size="xs">
          {tieneHijos && <span className="text-[10px]">{abierto ? "－" : "＋"}</span>}
          🥄 {ingrediente.nombre}
        </BadgeArbol>
      </button>
      {abierto && tieneHijos && (
        <div className="ml-6 pl-3 border-l-2 border-green-200 space-y-0.5 mt-0.5">
          {ingrediente.cantidad && <NodoHoja etiqueta="cantidad" valor={ingrediente.cantidad} />}
          {ingrediente.unidad && <NodoHoja etiqueta="unidad" valor={ingrediente.unidad} />}
        </div>
      )}
    </div>
  );
}

function NodoInstruccion({ instruccion, esUltimo, nivel }) {
  const [abierto, setAbierto] = useState(true);
  const colores = COLORES_INSTRUCCION[instruccion.tipo] || { bg: "bg-gray-100", text: "text-gray-800", dot: "bg-gray-500" };
  const etiqueta = ETIQUETA_INSTRUCCION[instruccion.tipo] || instruccion.tipo;
  const tieneTiempo = instruccion.tiempo || instruccion.unidad_tiempo;
  const tieneIngredientes = instruccion.ingredientes && instruccion.ingredientes.length > 0;
  const expandible = tieneTiempo || tieneIngredientes;

  return (
    <div className="relative">
      <div className="flex items-start gap-1">
        {nivel > 0 && (
          <div className="flex flex-col items-center pt-2">
            <div className={`w-4 h-0.5 ${esUltimo ? "bg-blue-300" : "bg-blue-300"}`} />
          </div>
        )}
        <div className="flex-1 min-w-0">
          <button
            onClick={() => expandible && setAbierto(!abierto)}
            className={`flex items-center gap-2 w-full text-left py-1.5 px-3 rounded-lg transition-colors ${colores.bg} ${expandible ? "cursor-pointer hover:brightness-95" : "cursor-default"}`}
          >
            {expandible && (
              <span className={`transition-transform duration-200 text-xs ${abierto ? "rotate-0" : "-rotate-90"}`}>▼</span>
            )}
            {!expandible && <span className="w-3" />}
            <span className={`w-2 h-2 rounded-full ${colores.dot}`} />
            <span className={`font-semibold text-sm ${colores.text}`}>{etiqueta}</span>
            {instruccion.tiempo && (
              <span className="text-sm text-gray-500 ml-1">
                ⏱ {instruccion.tiempo}{instruccion.unidad_tiempo ? ` ${instruccion.unidad_tiempo.replace("UNIDAD_TIEMPO_", "").toLowerCase()}` : ""}
              </span>
            )}
          </button>

          {abierto && tieneIngredientes && (
            <div className="ml-4 pl-4 border-l-2 border-blue-200 mt-1 space-y-1">
              {instruccion.ingredientes.map((ing, i) => (
                <NodoIngrediente key={i} ingrediente={ing} nivel={nivel + 1} />
              ))}
            </div>
          )}

          {abierto && tieneTiempo && !tieneIngredientes && (
            <div className="ml-4 pl-4 border-l-2 border-blue-200 mt-1">
              {instruccion.tiempo && <NodoHoja etiqueta="tiempo" valor={`${instruccion.tiempo}${instruccion.unidad_tiempo ? ` ${instruccion.unidad_tiempo}` : ""}`} />}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function AstTree({ ast }) {
  const [abierto, setAbierto] = useState(true);

  if (!ast) return null;

  return (
    <div>
      <h3 className="text-sm font-semibold text-gray-700 mb-2">AST</h3>
      <div className="bg-white border border-gray-200 rounded-xl shadow-sm p-4 font-mono text-sm overflow-x-auto">
        <button
          onClick={() => setAbierto(!abierto)}
          className="flex items-center gap-2 w-full text-left px-3 py-2 bg-gray-800 text-white rounded-lg mb-2"
        >
          <span className={`transition-transform duration-200 text-xs ${abierto ? "rotate-0" : "-rotate-90"}`}>▼</span>
          <span className="w-2 h-2 rounded-full bg-white" />
          <span className="font-semibold">NodoReceta</span>
          {ast.instrucciones && <span className="text-gray-400 text-xs ml-1">({ast.instrucciones.length} instrucciones)</span>}
        </button>

        {abierto && (
          <div className="ml-4 pl-4 border-l-2 border-gray-300 space-y-2">
            {ast.instrucciones && ast.instrucciones.length > 0 ? (
              ast.instrucciones.map((inst, i) => (
                <NodoInstruccion
                  key={i}
                  instruccion={inst}
                  esUltimo={i === ast.instrucciones.length - 1}
                  nivel={1}
                />
              ))
            ) : (
              <p className="text-gray-400 text-sm ml-2">(sin instrucciones)</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
