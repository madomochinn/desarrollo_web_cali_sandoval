package com.tarea4.t4.controllers;

import java.util.*;

import org.springframework.beans.factory.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.tarea4.t4.models.*;
import com.tarea4.t4.repositories.*;
import jakarta.transaction.*;

@RestController
@RequestMapping("/api/avisos")
public class EvaluacionRestController {

    @Autowired
    private AvisoAdopcionRepository avisoRepository; 
    
    @Autowired
    private NotaRepository notaRepository;

    static class NotaRequest {
        private Integer nota;
        
        public Integer getNota() { return nota; }
        public void setNota(Integer nota) { this.nota = nota; }
    }


    @PostMapping("/{avisoId}/evaluar")
    @Transactional
    public ResponseEntity<Map<String, Object>> evaluarAviso(
            @PathVariable Integer avisoId, 
            @RequestBody NotaRequest request) {

        Integer nota = request.getNota();

        // validamos la nota (seguridad en el servidor)
        if (nota == null || nota < 1 || nota > 7) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("error", "La nota debe ser un número entero entre 1 y 7.");
            return ResponseEntity.badRequest().body(errorResponse);
        }

        return avisoRepository.findById(avisoId)
            .map(aviso -> {
                // creamos y guardamos la nueva nota
                Nota nuevaNota = new Nota(aviso, nota);
                notaRepository.save(nuevaNota); 

                // recalculamos la nota promedio para el aviso
                aviso.getNotas().add(nuevaNota); 
                
                Double nuevoPromedio = aviso.calcularPromedioNota(); 

                // devolvemos el nuevo promedio al cliente
                Map<String, Object> response = new HashMap<>();
                response.put("promedio", nuevoPromedio);
                
                return ResponseEntity.ok(response);
            })
            .orElse(ResponseEntity.notFound().build()); 
    }
}
