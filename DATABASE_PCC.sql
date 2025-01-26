-- Tabla LOGIN
CREATE TABLE LOGIN (
    ID_login SERIAL PRIMARY KEY,
    Correo_electronico VARCHAR(50) NOT NULL,
    Contraseña VARCHAR(25)
);


-- Tabla CATEGORIA
CREATE TABLE CATEGORIA (
    ID_categoria SERIAL PRIMARY KEY,
    Nombre VARCHAR(50) UNIQUE NOT NULL,
    Descripcion VARCHAR(200) NOT NULL
);


CREATE TABLE CLIENTE (
    ID_cliente SERIAL PRIMARY KEY,       -- Identificador único para cada cliente
    Nombre VARCHAR(50) NOT NULL,         -- Nombre del cliente (obligatorio)
    Apellido VARCHAR(50) NOT NULL,       -- Apellido del cliente (obligatorio)
    RFC VARCHAR(13),                     -- RFC del cliente (obligatorio)
    Direccion VARCHAR(200) NOT NULL,     -- Dirección del cliente (obligatorio)
    Telefono VARCHAR(15) UNIQUE NOT NULL -- Teléfono del cliente (obligatorio)
);


-- Tabla SERVICIO
CREATE TABLE SERVICIO (
    ID_servicio SERIAL PRIMARY KEY,
    Descripcion VARCHAR(200) NOT NULL,
    Tipo VARCHAR(50) NOT NULL,
	Estado VARCHAR(50),
    Recepcion DATE NOT NULL,
    Entrega DATE NOT NULL,
    Solucion VARCHAR(500),
    Abono FLOAT,
    Servicio FLOAT,
    Total FLOAT,
    ID_cliente INT,
	ID_equipo INT,
    ID_tecnico INT
);


-- Tabla TECNICO
CREATE TABLE TECNICO(
    ID_tecnico SERIAL PRIMARY KEY,
    Nombre_completo VARCHAR(100) NOT NULL,
    Telefono VARCHAR(15) UNIQUE NOT NULL
);


-- Tabla REPUESTO
CREATE TABLE REPUESTO (
    ID_repuesto SERIAL PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Descripcion VARCHAR(200) NOT NULL,
    Marca VARCHAR(50) NOT NULL,
	Ubicacion VARCHAR(50),
    Compra  float NOT NULL,
    Venta float NOT NULL,
    Stock int NOT NULL,
    ID_categoria INT
);

-- Tabla EQUIPO
CREATE TABLE EQUIPO (
    ID_equipo SERIAL PRIMARY KEY,
	Equipo VARCHAR(50) NOT NULL,
    Num_serie_IMEI VARCHAR(50) UNIQUE NOT NULL,
    Marca VARCHAR(50) NOT NULL,
    Modelo VARCHAR(50) NOT NULL,
	Detalles VARCHAR(200) NOT NULL,
    ID_categoria INT,
	ID_cliente INT
);

ALTER TABLE EQUIPO 
ADD CONSTRAINT fk_categoria FOREIGN KEY (ID_categoria) REFERENCES CATEGORIA(ID_categoria) ON UPDATE CASCADE ON DELETE CASCADE,
ADD CONSTRAINT fk_cliente FOREIGN KEY (ID_cliente) REFERENCES CLIENTE(ID_cliente) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE SERVICIO 
ADD CONSTRAINT fk_cliente FOREIGN KEY (ID_cliente) REFERENCES CLIENTE(ID_cliente) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE SERVICIO 
ADD CONSTRAINT fk_equipo FOREIGN KEY (ID_equipo) REFERENCES EQUIPO(ID_equipo) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE SERVICIO 
ADD CONSTRAINT fk_tecnico FOREIGN KEY (ID_tecnico) REFERENCES TECNICO(ID_tecnico) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE REPUESTO
ADD CONSTRAINT fk_categoria FOREIGN KEY (ID_categoria) REFERENCES CATEGORIA(ID_categoria) ON UPDATE CASCADE ON DELETE CASCADE; 