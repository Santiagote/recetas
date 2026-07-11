package com.unl.semantico.aplicacion.reglas;

import com.unl.semantico.dominio.modelo.NodoIngrediente;
import com.unl.semantico.dominio.modelo.NodoInstruccion;
import com.unl.semantico.dominio.modelo.NodoReceta;
import com.unl.semantico.infraestructura.CatalogoIngredientes;
import com.unl.semantico.infraestructura.CatalogoIngredientes.InfoIngrediente;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class ReglaUnidadCompatible implements ReglaValidacion {

    private final CatalogoIngredientes catalogo;

    public ReglaUnidadCompatible(CatalogoIngredientes catalogo) {
        this.catalogo = catalogo;
    }

    @Override
    public List<String> validar(NodoReceta receta) {
        List<String> errores = new ArrayList<>();

        for (NodoInstruccion instruccion : receta.getInstrucciones()) {
            for (NodoIngrediente ingrediente : instruccion.getIngredientes()) {
                InfoIngrediente info = catalogo.buscar(ingrediente.getNombre());

                if (info == null) {
                    errores.add(String.format(
                            "Ingrediente '%s' no reconocido en el catalogo de recetas.",
                            ingrediente.getNombre()));
                    continue;
                }

                if (ingrediente.getUnidad() != null
                        && !info.unidadesValidas().contains(ingrediente.getUnidad())) {
                    errores.add(String.format(
                            "'%s' no admite la unidad '%s' (tipo '%s' requiere %s).",
                            ingrediente.getNombre(), ingrediente.getUnidad(),
                            info.tipo(), info.unidadesValidas()));
                }
            }
        }
        return errores;
    }
}