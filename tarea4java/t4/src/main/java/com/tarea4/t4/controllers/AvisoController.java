package com.tarea4.t4.controllers;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.*;
import org.springframework.data.domain.*;
import org.springframework.stereotype.*;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import com.tarea4.t4.models.AvisoAdopcion;
import com.tarea4.t4.repositories.*;

@Controller
public class AvisoController {

    @Autowired
    private AvisoAdopcionRepository avisoRepository;

    @GetMapping("/listado")
    public String listarAvisos(@RequestParam(defaultValue = "1") int pagina, Model model) {
        
        Pageable pageable = PageRequest.of(pagina - 1, 10); 
        Page<AvisoAdopcion> avisosPage = avisoRepository.findAll(pageable);

        // calculamos el promedio de nota para cada aviso antes de pasarlo a la vista
        List<AvisoAdopcion> avisosConPromedio = avisosPage.getContent().stream()
            .peek(aviso -> {
                Double promedio = aviso.calcularPromedioNota();
                aviso.setPromedioNota(promedio);
            })
            .collect(Collectors.toList());


        model.addAttribute("avisos", avisosConPromedio);
        model.addAttribute("pagina", avisosPage.getNumber() + 1);
        model.addAttribute("total_paginas", avisosPage.getTotalPages());

        return "listado";
    }
}
