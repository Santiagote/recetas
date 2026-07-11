package com.unl.semantico.aplicacion.reglas;

import com.unl.semantico.dominio.modelo.NodoIngrediente;
import com.unl.semantico.dominio.modelo.NodoInstruccion;
import com.unl.semantico.dominio.modelo.NodoReceta;
import com.unl.semantico.infraestructura.CatalogoIngredientes;
import com.unl.semantico.infraestructura.CatalogoIngredientes.InfoIngrediente;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

@Component
public class ReglaInstruccionCompatible implements ReglaValidacion {

    private static final Set<String> INSTRUCCIONES_SOLO_SOLIDOS = Set.of("INSTRUCCION_CORTAR");

    private final CatalogoIngredientes catalogo;

    public ReglaInstruccionCompatible(CatalogoIngredientes catalogo) {
        this.catalogo = catalogo;
    }

    @Override
    public List<String> validar(NodoReceta receta) {
        List<String> errores = new ArrayList<>();

        for (NodoInstruccion instruccion : receta.getInstrucciones()) {
            if (!INSTRUCCIONES_SOLO_SOLIDOS.contains(instruccion.getTipo())) {
                continue;
            }
            for (NodoIngrediente ingrediente : instruccion.getIngredientes()) {
                InfoIngrediente info = catalogo.buscar(ingrediente.getNombre());
                if (info != null && "liquido".equals(info.tipo())) {
                    errores.add(String.format(
                            "No se puede aplicar '%s' sobre '%s' (es liquido).",
                            instruccion.getTipo(), ingrediente.getNombre()));
                }
            }
        }
        return errores;
    }
}