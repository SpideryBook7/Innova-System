DROP TABLE IF EXISTS reservaciones;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE reservaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    correo TEXT NOT NULL,
    telefono TEXT NOT NULL,
    Fecha TEXT NOT NULL,
    nombre_cabana TEXT NOT NULL,
    fecha_de_salida TEXT NOT NULL,
    precio REAL NOT NULL
);

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
