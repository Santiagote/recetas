package com.unl.semantico.aplicacion;

import com.unl.semantico.dominio.modelo.NodoReceta;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

import com.unl.semantico.aplicacion.reglas.ReglaValidacion;

@Service
public class AnalizadorSemanticoService {

    private final List<ReglaValidacion> reglas;

    // Spring inyecta automaticamente todos los beans que implementan ReglaValidacion
    public AnalizadorSemanticoService(List<ReglaValidacion> reglas) {
        this.reglas = reglas;
    }

    public List<String> analizar(NodoReceta receta) {
        List<String> errores = new ArrayList<>();
        for (ReglaValidacion regla : reglas) {
            errores.addAll(regla.validar(receta));
        }
        return errores;
    }
}