package com.unl.semantico.aplicacion.reglas;

import com.unl.semantico.dominio.modelo.NodoIngrediente;
import com.unl.semantico.dominio.modelo.NodoInstruccion;
import com.unl.semantico.dominio.modelo.NodoReceta;
import com.unl.semantico.infraestructura.CatalogoIngredientes;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class ReglaCantidadValida implements ReglaValidacion {

    private final CatalogoIngredientes catalogo;

    public ReglaCantidadValida(CatalogoIngredientes catalogo) {
        this.catalogo = catalogo;
    }

    @Override
    public List<String> validar(NodoReceta receta) {
        List<String> errores = new ArrayList<>();

        for (NodoInstruccion instruccion : receta.getInstrucciones()) {
            for (NodoIngrediente ingrediente : instruccion.getIngredientes()) {
                validarCantidadIngrediente(ingrediente, errores);
            }
            if (instruccion.getTiempo() != null) {
                validarTiempo(instruccion, errores);
            }
        }
        return errores;
    }

    private void validarCantidadIngrediente(NodoIngrediente ingrediente, List<String> errores) {
        if (ingrediente.getCantidad() == null) {
            return;
        }
        Double valor = catalogo.resolverCantidad(ingrediente.getCantidad());
        if (valor == null) {
            errores.add(String.format(
                    "Cantidad '%s' de '%s' no es interpretable.",
                    ingrediente.getCantidad(), ingrediente.getNombre()));
        } else if (valor <= 0) {
            errores.add(String.format(
                    "Cantidad de '%s' debe ser mayor a cero.", ingrediente.getNombre()));
        }
    }

    private void validarTiempo(NodoInstruccion instruccion, List<String> errores) {
        Double valor = catalogo.resolverCantidad(instruccion.getTiempo());
        if (valor == null) {
            errores.add(String.format(
                    "Cantidad de tiempo '%s' no es interpretable.", instruccion.getTiempo()));
            return;
        }
        if (valor <= 0) {
            errores.add(String.format(
                    "El tiempo en '%s' debe ser mayor a cero.", instruccion.getTipo()));
        }
        if (instruccion.getUnidadTiempo() != null
            && instruccion.getUnidadTiempo().startsWith("hora")
            && valor > 24) {
        errores.add(String.format(
            "Tiempo de %s horas en '%s' es poco razonable.",
            valor, instruccion.getTipo()));
}
    }
}