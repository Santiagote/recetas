package com.unl.semantico.aplicacion.reglas;

import com.unl.semantico.dominio.modelo.NodoReceta;

import java.util.List;

public interface ReglaValidacion {
    List<String> validar(NodoReceta receta);
}