package com.tarea4.t4.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.tarea4.t4.models.Comuna;

@Repository
public interface ComunaRepository extends JpaRepository<Comuna, Integer> {
}
