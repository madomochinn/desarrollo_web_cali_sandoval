package com.tarea4.t4.models;

import jakarta.persistence.*;
import java.util.List;

@Entity
@Table(name = "region")
public class Region {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "nombre", nullable = false)
    private String nombre;

    @OneToMany(mappedBy = "region")
    private List<Comuna> comunas;

    // --- CONSTRUCTORES ---
    public Region() {}
    
    // --- GETTERS Y SETTERS ---
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public List<Comuna> getComunas() { return comunas; }
    public void setComunas(List<Comuna> comunas) { this.comunas = comunas; }
}
