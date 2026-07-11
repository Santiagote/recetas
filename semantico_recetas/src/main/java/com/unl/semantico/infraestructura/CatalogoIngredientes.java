package com.unl.semantico.infraestructura;

import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;

@Component
public class CatalogoIngredientes {

    public record InfoIngrediente(String tipo, List<String> unidadesValidas) {
    }

    private static final Map<String, InfoIngrediente> INGREDIENTES = Map.of(
            "harina", new InfoIngrediente("solido", List.of("UNIDAD_MASA")),
            "azucar", new InfoIngrediente("solido", List.of("UNIDAD_MASA")),
            "sal", new InfoIngrediente("solido", List.of("UNIDAD_MASA")),
            "leche", new InfoIngrediente("liquido", List.of("UNIDAD_VOLUMEN")),
            "aceite", new InfoIngrediente("liquido", List.of("UNIDAD_VOLUMEN")),
            "huevo", new InfoIngrediente("unidad", List.of("UNIDAD_UNIDAD"))
    );

    private static final Map<String, Double> CANTIDAD_A_NUMERO = Map.of(
            "un", 1.0,
            "una", 1.0,
            "dos", 2.0,
            "tres", 3.0,
            "media", 0.5,
            "par", 2.0
    );

    public InfoIngrediente buscar(String nombreIngrediente) {
        return INGREDIENTES.get(nombreIngrediente);
    }

    public Double resolverCantidad(String cantidad) {
        if (cantidad == null) {
            return null;
        }
        if (cantidad.chars().allMatch(Character::isDigit) && !cantidad.isEmpty()) {
            return Double.parseDouble(cantidad);
        }
        return CANTIDAD_A_NUMERO.get(cantidad);
    }
}