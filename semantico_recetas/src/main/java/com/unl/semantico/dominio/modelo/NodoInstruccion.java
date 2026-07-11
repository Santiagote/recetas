package com.unl.semantico.dominio.modelo;

import java.util.ArrayList;
import java.util.List;

public class NodoInstruccion {

    private String tipo;
    private List<NodoIngrediente> ingredientes = new ArrayList<>();
    private String tiempo;
    private String unidadTiempo;

    public NodoInstruccion() {
    }

    public String getTipo() {
        return tipo;
    }

    public void setTipo(String tipo) {
        this.tipo = tipo;
    }

    public List<NodoIngrediente> getIngredientes() {
        return ingredientes;
    }

    public void setIngredientes(List<NodoIngrediente> ingredientes) {
        this.ingredientes = ingredientes;
    }

    public String getTiempo() {
        return tiempo;
    }

    public void setTiempo(String tiempo) {
        this.tiempo = tiempo;
    }

    public String getUnidadTiempo() {
        return unidadTiempo;
    }

    public void setUnidadTiempo(String unidadTiempo) {
        this.unidadTiempo = unidadTiempo;
    }
}