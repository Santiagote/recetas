package com.unl.semantico.dominio.modelo;

import java.util.List;

public class ResultadoValidacion {

    private List<String> erroresSemanticos;
    private boolean esValido;

    public ResultadoValidacion(List<String> erroresSemanticos) {
        this.erroresSemanticos = erroresSemanticos;
        this.esValido = erroresSemanticos.isEmpty();
    }

    public List<String> getErroresSemanticos() {
        return erroresSemanticos;
    }

    public boolean isEsValido() {
        return esValido;
    }
}