-- Tabla LOGIN
CREATE TABLE LOGIN (
    ID_login SERIAL PRIMARY KEY,
    Correo_electronico VARCHAR(25),
    Contraseña VARCHAR(25)
);


-- Tabla CATEGORIA
CREATE TABLE CATEGORIA (
    ID_categoria SERIAL PRIMARY KEY,
    Nombre VARCHAR(30),
    Descripcion VARCHAR(100)
);


CREATE TABLE CLIENTE (
    ID_cliente SERIAL PRIMARY KEY,       -- Identificador único para cada cliente
    Nombre VARCHAR(50) NOT NULL,         -- Nombre del cliente (obligatorio)
    Apellido VARCHAR(50) NOT NULL,       -- Apellido del cliente (obligatorio)
    RFC VARCHAR(13) NOT NULL,            -- RFC del cliente (obligatorio)
    Direccion VARCHAR(100) NOT NULL,     -- Dirección del cliente (obligatorio)
    Telefono VARCHAR(15) NOT NULL,       -- Teléfono del cliente (obligatorio)
    ID_servicio INT,                     -- ID del servicio (opcional)
    ID_equipo INT,                       -- ID del equipo (opcional)
    ID_categoria INT NOT NULL,           -- Relación con la tabla CATEGORIA (obligatorio)
    CONSTRAINT fk_categoria FOREIGN KEY (ID_categoria) REFERENCES CATEGORIA(ID_categoria) -- Clave foránea
);


-- Tabla SERVICIO
CREATE TABLE SERVICIO (
    ID_servicio SERIAL PRIMARY KEY,
    Descripcion VARCHAR(100),
    Tipo VARCHAR(20),
    Recepcion DATE,
    Entrega DATE,
    Solucion VARCHAR(100),
    Abono FLOAT,
    Servicio FLOAT,
    Total FLOAT,
    ID_cliente INT,
	ID_equipo INT,
    FOREIGN KEY (ID_cliente) REFERENCES CLIENTE(ID_cliente)
);


-- Tabla TECNICO
CREATE TABLE TECNICO(
    ID_tecnico SERIAL PRIMARY KEY,
    Nombre_completo VARCHAR(50),
    Telefono VARCHAR(15)
);


-- Tabla REPUESTO
CREATE TABLE REPUESTO (
    ID_repuesto SERIAL PRIMARY KEY,
    Nombre VARCHAR(50),
    Descripcion VARCHAR(100),
    Marca VARCHAR(20),
    Categoria VARCHAR(50),
    Compra  VARCHAR(30),
    Venta VARCHAR(30),
    Stock VARCHAR(10),
    ID_categoria INT,
    FOREIGN KEY (ID_categoria) REFERENCES CATEGORIA(ID_categoria)
);

-- Tabla EQUIPO
CREATE TABLE EQUIPO (
    ID_equipo SERIAL PRIMARY KEY,
    Num_serie VARCHAR(50),
    IMEI VARCHAR(50),
    Marca VARCHAR(20),
    Modelo VARCHAR(50),
    Estado VARCHAR(20),
    ID_categoria INT,
    ID_tecnico INT,
	ID_repuesto INT,
	ID_cliente INT,
    FOREIGN KEY (ID_categoria) REFERENCES CATEGORIA(ID_categoria),
    FOREIGN KEY (ID_tecnico) REFERENCES TECNICO(ID_tecnico),
	FOREIGN KEY (ID_repuesto) REFERENCES REPUESTO(ID_repuesto),
	FOREIGN KEY (ID_cliente) REFERENCES CLIENTE(ID_cliente)
);

ALTER TABLE CLIENTE 
ADD FOREIGN KEY (ID_servicio) REFERENCES SERVICIO(ID_servicio),
ADD FOREIGN KEY (ID_equipo) REFERENCES EQUIPO(ID_equipo);

ALTER TABLE SERVICIO 
ADD FOREIGN KEY (ID_equipo) REFERENCES EQUIPO(ID_equipo)
