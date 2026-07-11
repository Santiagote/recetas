package com.unl.semantico.api;

import com.unl.semantico.aplicacion.AnalizadorSemanticoService;
import com.unl.semantico.dominio.modelo.NodoReceta;
import com.unl.semantico.dominio.modelo.ResultadoValidacion;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class SemanticoController {

    private final AnalizadorSemanticoService servicio;

    public SemanticoController(AnalizadorSemanticoService servicio) {
        this.servicio = servicio;
    }

    @PostMapping("/validar")
    public ResultadoValidacion validar(@RequestBody NodoReceta receta) {
        List<String> errores = servicio.analizar(receta);
        return new ResultadoValidacion(errores);
    }

    @GetMapping("/")
    public String index() {
        return "{\"api\":\"Servicio Semantico\",\"version\":\"1.0\"}";
    }
}