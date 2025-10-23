-- crear el usuario cc5002
CREATE USER IF NOT EXISTS 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';

-- darle permisos sobre la base de datos
GRANT ALL PRIVILEGES ON tarea2.* TO 'cc5002'@'localhost';

-- aplicar los cambios
FLUSH PRIVILEGES;

-- eliminar el usuario cc5002
DROP USER 'cc5002'@'localhost';