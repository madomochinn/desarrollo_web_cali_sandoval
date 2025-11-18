package com.tarea4.t4.models;

import jakarta.persistence.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "aviso_adopcion") // Nombre de la tabla en tarea2.sql
public class AvisoAdopcion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    // Campos principales basados en listado.html y tarea2.sql
    @Column(name = "fecha_ingreso")
    private LocalDate fechaIngreso;

    @Column(name = "sector")
    private String sector;

    @Column(name = "cantidad")
    private Integer cantidad;

    @Column(name = "tipo")
    private String tipo;

    @Column(name = "edad")
    private Integer edad;

    // Columna para 'a' (años) o 'm' (meses)
    @Column(name = "unidad_medida") 
    private String unidadMedida; 

    // Relación Many-to-One a la entidad Comuna (asumiendo que existe)
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "comuna_id") // La columna con la FK a comuna
    private Comuna comuna;
    
    @OneToMany(mappedBy = "aviso", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
    private List<Nota> notas = new ArrayList<>(); // Inicializar para evitar NullPointerException

    @Transient 
    private Double promedioNota;

    // --- CONSTRUCTORES ---
    public AvisoAdopcion() {
    }
    
    // --- MÉTODOS DE CÁLCULO ---

    public Double calcularPromedioNota() {
        if (notas == null || notas.isEmpty()) {
            return 0.0;
        }
        double suma = notas.stream().mapToInt(Nota::getNota).sum();
        return suma / notas.size();
    }
    
    // --- GETTERS Y SETTERS ---

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public LocalDate getFechaIngreso() { return fechaIngreso; }
    public void setFechaIngreso(LocalDate fechaIngreso) { this.fechaIngreso = fechaIngreso; }

    public String getSector() { return sector; }
    public void setSector(String sector) { this.sector = sector; }

    public Integer getCantidad() { return cantidad; }
    public void setCantidad(Integer cantidad) { this.cantidad = cantidad; }

    public String getTipo() { return tipo; }
    public void setTipo(String tipo) { this.tipo = tipo; }

    public Integer getEdad() { return edad; }
    public void setEdad(Integer edad) { this.edad = edad; }

    public String getUnidadMedida() { return unidadMedida; }
    public void setUnidadMedida(String unidadMedida) { this.unidadMedida = unidadMedida; }
    
    public String getComuna() { 
        return (this.comuna != null) ? this.comuna.getNombre() : "N/A";
    }
    public void setComuna(Comuna comuna) { this.comuna = comuna; }
    public Comuna getComunaEntity() { return this.comuna; }

    public Double getPromedioNota() { return promedioNota; }
    public void setPromedioNota(Double promedioNota) { this.promedioNota = promedioNota; }
    
    public List<Nota> getNotas() { return notas; }
    public void setNotas(List<Nota> notas) { this.notas = notas; }
}
