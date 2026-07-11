package com.unl.semantico.dominio.modelo;

import java.util.ArrayList;
import java.util.List;

public class NodoReceta {

    private List<NodoInstruccion> instrucciones = new ArrayList<>();

    public NodoReceta() {
    }

    public List<NodoInstruccion> getInstrucciones() {
        return instrucciones;
    }

    public void setInstrucciones(List<NodoInstruccion> instrucciones) {
        this.instrucciones = instrucciones;
    }
}