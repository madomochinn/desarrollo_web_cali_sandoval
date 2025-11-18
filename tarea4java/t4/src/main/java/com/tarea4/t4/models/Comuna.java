package com.tarea4.t4.models;

import jakarta.persistence.*;
import java.util.List;

@Entity
@Table(name = "comuna")
public class Comuna {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "nombre", nullable = false)
    private String nombre;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "region_id", nullable = false)
    private Region region;

    @OneToMany(mappedBy = "comuna")
    private List<AvisoAdopcion> avisos;

    // --- CONSTRUCTORES ---
    public Comuna() {}
    
    // --- GETTERS Y SETTERS ---
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public Region getRegion() { return region; }
    public void setRegion(Region region) { this.region = region; }

    public List<AvisoAdopcion> getAvisos() { return avisos; }
    public void setAvisos(List<AvisoAdopcion> avisos) { this.avisos = avisos; }
}
