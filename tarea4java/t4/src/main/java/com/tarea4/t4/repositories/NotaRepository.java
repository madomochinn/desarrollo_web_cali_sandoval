package com.tarea4.t4.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.tarea4.t4.models.*;

@Repository
public interface NotaRepository extends JpaRepository<Nota, Integer> {
}
