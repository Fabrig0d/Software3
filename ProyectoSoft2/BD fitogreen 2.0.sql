CREATE DATABASE fitogreen;

USE fitogreen;
-- Tabla para usuarios
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    usuario VARCHAR(100) UNIQUE, 
    contrasena VARCHAR(200), 
    tipo VARCHAR(20) -- Puede ser 'admin', 'empleado', o 'cliente'
);

-- Tabla para clientes
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100), 
    apellidos VARCHAR(100), 
    correo VARCHAR(100) UNIQUE, 
    telefono_celular VARCHAR(20), 
    dni_ruc VARCHAR(15), 
    fecha_nacimiento DATE, 
    departamento VARCHAR(100), 
    provincia VARCHAR(100), 
    distrito VARCHAR(100), 
    direccion VARCHAR(200),
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);

-- Tabla para empleados
CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    nombre VARCHAR(100),  
    apellidos VARCHAR(100), 
    correo VARCHAR(100) UNIQUE, 
    telefono_celular VARCHAR(20), 
    dni VARCHAR(15), 
    fecha_nacimiento DATE, 
    direccion VARCHAR(200), 
    sueldo DECIMAL(8,2), 
    rol VARCHAR(100),
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);

-- Tabla para tipos de productos (categorías)
CREATE TABLE tipo_producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE
);

-- Tabla para productos
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion VARCHAR(200),
    presentacion varchar(100),
    precio_dis DECIMAL(8,2),
	precio_pub DECIMAL(8,2),
	stock INT,
    tipo_producto_id INT,
    FOREIGN KEY (tipo_producto_id) REFERENCES tipo_producto(id)
);


-- PROCEDIMIENTOS ALMACENADOS


DELIMITER //
CREATE PROCEDURE agregar_cliente(
    IN c_nombre VARCHAR(100),
    IN c_apellidos VARCHAR(100),
    IN c_correo VARCHAR(100),
    IN c_telefono_celular VARCHAR(20),
    IN c_dni_ruc VARCHAR(15),
    IN c_fecha_nacimiento DATE,
    IN c_departamento VARCHAR(100),
    IN c_provincia VARCHAR(100),
    IN c_distrito VARCHAR(100),
    IN c_direccion VARCHAR(200)
)
BEGIN
    INSERT INTO clientes (nombre, apellidos, correo, telefono_celular, dni_ruc, fecha_nacimiento, departamento, provincia, distrito, direccion)
    VALUES (c_nombre, c_apellidos, c_correo, c_telefono_celular, c_dni_ruc, c_fecha_nacimiento, c_departamento, c_provincia, c_distrito, c_direccion);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE editar_cliente(
    IN c_id INT,
    IN c_nombre VARCHAR(100),
    IN c_apellidos VARCHAR(100),
    IN c_correo VARCHAR(100),
    IN c_telefono_celular VARCHAR(20),
    IN c_dni_ruc VARCHAR(15),
    IN c_fecha_nacimiento DATE,
    IN c_departamento VARCHAR(100),
    IN c_provincia VARCHAR(100),
    IN c_distrito VARCHAR(100),
    IN c_direccion VARCHAR(200)
)
BEGIN
    UPDATE clientes
    SET nombre = c_nombre, apellidos = c_apellidos, correo = c_correo, telefono_celular = c_telefono_celular, dni_ruc = c_dni_ruc,
        fecha_nacimiento = c_fecha_nacimiento, departamento = c_departamento, provincia = c_provincia, distrito = c_distrito, direccion = c_direccion
    WHERE id = c_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE eliminar_cliente(
    IN c_id INT
)
BEGIN
    DELETE FROM clientes WHERE id = c_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE buscar_cli(
    IN c_id INT
)
BEGIN
    SELECT * FROM clientes WHERE id = c_id;
END //
DELIMITER ;


-- USUARIO

DELIMITER //
CREATE PROCEDURE agregar_usuario(
    IN u_usuario VARCHAR(100),
    IN u_contrasena VARCHAR(200),
    IN u_tipo VARCHAR(30)
)
BEGIN
    INSERT INTO usuario (usuario, contrasena, tipo)
    VALUES (u_usuario, u_contrasena, u_tipo);
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE editar_usuario(
    IN u_id INT,
    IN u_usuario VARCHAR(100),
    IN u_contrasena VARCHAR(200),
    IN u_tipo VARCHAR(30)
)
BEGIN
    UPDATE usuario
    SET usuario = u_usuario, contrasena = u_contrasena, tipo = u_tipo
    WHERE id = u_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE eliminar_usuario(
    IN u_id INT
)
BEGIN
    DELETE FROM usuario WHERE id = u_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE buscar_usu(
    IN u_id INT
)
BEGIN
    SELECT * FROM usuario WHERE id = u_id;
END //
DELIMITER ;


-- EMPLEADO


DELIMITER //
CREATE PROCEDURE agregar_empleado(
    IN e_nombre VARCHAR(100),
    IN e_apellidos VARCHAR(100),
    IN e_correo VARCHAR(100),
    IN e_telefono_celular VARCHAR(20),
    IN e_dni VARCHAR(15),
    IN e_fecha_nacimiento DATE,
    IN e_direccion VARCHAR(200),
    IN e_sueldo DECIMAL(8,2),
    IN e_rol VARCHAR(100),
    IN e_usuario_id INT
)
BEGIN
    INSERT INTO empleados (nombre, apellidos, correo, telefono_celular, dni, fecha_nacimiento, direccion, sueldo, rol, usuario_id)
    VALUES (e_nombre, e_apellidos, e_correo, e_telefono_celular, e_dni, e_fecha_nacimiento, e_direccion, e_sueldo, e_rol, e_usuario_id);
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE editar_empleado(
    IN e_id INT,
    IN e_nombre VARCHAR(100),
    IN e_apellidos VARCHAR(100),
    IN e_correo VARCHAR(100),
    IN e_telefono_celular VARCHAR(20),
    IN e_dni VARCHAR(15),
    IN e_fecha_nacimiento DATE,
    IN e_direccion VARCHAR(200),
    IN e_sueldo DECIMAL(8,2),
    IN e_rol VARCHAR(100),
    IN e_usuario_id INT
)
BEGIN
    UPDATE empleados
    SET nombre = e_nombre, apellidos = e_apellidos, correo = e_correo, telefono_celular = e_telefono_celular, dni = e_dni,
        fecha_nacimiento = e_fecha_nacimiento, direccion = e_direccion, sueldo = e_sueldo, rol = e_rol, usuario_id = e_usuario_id
    WHERE id = e_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE eliminar_empleado(
    IN e_id INT
)
BEGIN
    DELETE FROM empleados WHERE id = e_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE buscar_emp(
    IN e_id INT
)
BEGIN
    SELECT * FROM empleados WHERE id = e_id;
END //
DELIMITER ;

-- TIPO DE PRODUCTO


DELIMITER //
CREATE PROCEDURE agregar_tipo_producto(
    IN tp_nombre VARCHAR(100)
)
BEGIN
    INSERT INTO tipo_producto (nombre)
    VALUES (tp_nombre);
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE editar_tipo_producto(
    IN tp_id INT,
    IN tp_nombre VARCHAR(100)
)
BEGIN
    UPDATE tipo_producto
    SET nombre = tp_nombre
    WHERE id = tp_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE eliminar_tipo_producto(
    IN tp_id INT
)
BEGIN
    DELETE FROM tipo_producto WHERE id = tp_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE buscar_tp(
    IN tp_id INT
)
BEGIN
    SELECT * FROM tipo_producto WHERE id = tp_id;
END //
DELIMITER ;


-- PRODUCTOS

DELIMITER //
CREATE PROCEDURE agregar_producto(
    IN p_nombre VARCHAR(100),
    IN p_descripcion VARCHAR(200),
    IN p_presentacion varchar(100),
    IN p_preciodis DECIMAL(8,2),
    IN p_preciopub DECIMAL(8,2),
    IN p_stock INT,
    IN p_tipo_producto_id INT
)
BEGIN
    INSERT INTO productos (nombre, descripcion, presentacion, precio_dis, precio_pub,stock, tipo_producto_id)
    VALUES (p_nombre, p_descripcion, p_presentacion, p_preciodis ,p_preciopub,p_stock, p_tipo_producto_id);
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE editar_producto(
    IN p_id INT,
    IN p_nombre VARCHAR(100),
    IN p_descripcion VARCHAR(200),
    IN p_presentacion varchar(100),
	IN p_preciodis DECIMAL(8,2),
	IN p_preciopub DECIMAL(8,2),
    IN p_stock INT,
    IN p_tipo_producto_id INT
)
BEGIN
    UPDATE productos
    SET nombre = p_nombre, descripcion = p_descripcion, presentacion = p_presentacion, precio_dis = p_preciodis, precio_pub = p_preciopub , stock = p_stock,  tipo_producto_id = p_tipo_producto_id
    WHERE id = p_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE eliminar_producto(
    IN p_id INT
)
BEGIN
    DELETE FROM productos WHERE id = p_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE buscar_producto(
    IN p_id INT
)
BEGIN
    SELECT * FROM productos WHERE id = p_id;
END //
DELIMITER ;



-- Agregar usuarios
CALL agregar_usuario('joselp','psw1','cliente');
CALL agregar_usuario('maria01', 'password123', 'cliente');
CALL agregar_usuario('juanito95', 'abc123', 'empleado');
CALL agregar_usuario('admin123', 'adminpass', 'admin');
CALL agregar_usuario('luisa89', 'lalala123', 'cliente');
CALL agregar_usuario('pedrito22', 'password456', 'empleado');
CALL agregar_usuario('ana555', 'ana123', 'cliente');

-- Agregar clientes
CALL agregar_cliente ('Jose','Lopez Borja','josesitolb@gmail.com','987654321','1234567','1990-05-25','Lima','Lima','SJL','jr macumba 221');
CALL agregar_cliente('María', 'García Pérez', 'maria.garcia@example.com', '987654321', '12345678', '1992-08-10', 'Lima', 'Lima', 'Miraflores', 'Av. Larco 123');
CALL agregar_cliente('Juan', 'Pérez Rodríguez', 'juanito.perez@example.com', '999888777', '87654321', '1985-03-20', 'Lima', 'Lima', 'San Isidro', 'Av. Arequipa 456');
CALL agregar_cliente('Luisa', 'Martínez González', 'luisa.martinez@example.com', '987123456', '56789012', '1995-11-15', 'Lima', 'Lima', 'Surco', 'Calle Las Flores 789');
CALL agregar_cliente('Pedro', 'Vargas López', 'pedro.vargas@example.com', '955772233', '11223344', '1988-07-03', 'Lima', 'Lima', 'Barranco', 'Av. Grau 321');
CALL agregar_cliente('Ana', 'Sánchez Ramírez', 'ana.sanchez@example.com', '998877665', '99887766', '1990-04-27', 'Lima', 'Lima', 'San Borja', 'Jr. Los Pinos 456');

-- TIPO DE PRODUCTOS

CALL agregar_tipo_producto('Algas Marinas y Fitohormonas');
CALL agregar_tipo_producto('Fungicidas Biológicos');
CALL agregar_tipo_producto('Aminoácidos');
CALL agregar_tipo_producto('Ácidos Húmicos');
CALL agregar_tipo_producto('Nutrientes Específicos');	

-- PRODUCTOS

-- FITO ALGAS: Algas Marinas + Fitohormonas
CALL agregar_producto('FITO ALGAS', 'Algas Marinas + Fitohormonas', '12 litros', 30.00, 50.00, 100, 1);
CALL agregar_producto('FITO ALGAS', 'Algas Marinas + Fitohormonas', '20 litros', 25.00, 40.00, 150, 1);
CALL agregar_producto('FITO ALGAS', 'Algas Marinas + Fitohormonas', '200 litros', 20.00, 35.00, 200, 1);

-- ALGAS SHEER: Algas marinas
CALL agregar_producto('ALGAS SHEER', 'Algas marinas', '12 litros', 20.00, 35.00, 80, 1);
CALL agregar_producto('ALGAS SHEER', 'Algas marinas', '20 litros', 15.00, 30.00, 120, 1);
CALL agregar_producto('ALGAS SHEER', 'Algas marinas', '200 litros', 10.00, 20.00, 50, 1);

-- HONGO STOP: Fungicida Biológico
CALL agregar_producto('HONGO STOP', 'Fungicida Biológico', '12 litros', 55.00, 65.00, 90, 2);
CALL agregar_producto('HONGO STOP', 'Fungicida Biológico', '20 litros', 45.00, 60.00, 110, 2);
CALL agregar_producto('HONGO STOP', 'Fungicida Biológico', '200 litros', 40.00, 55.00, 150, 2);

-- FITO AMINO: Aminoácidos
CALL agregar_producto('FITO AMINO', 'Aminoácidos', '12 litros', 35.00, 60.00, 70, 3);
CALL agregar_producto('FITO AMINO', 'Aminoácidos', '20 litros', 30.00, 50.00, 100, 3);
CALL agregar_producto('FITO AMINO', 'Aminoácidos', '200 litros', 25.00, 50.00, 130, 3);

-- FITO HUMIC 20: Ácidos Húmicos (Leonardita)
CALL agregar_producto('FITO HUMIC 20', 'Ácidos Húmicos (Leonardita)', '12 litros', 15.00, 20.00, 60, 4);
CALL agregar_producto('FITO HUMIC 20', 'Ácidos Húmicos (Leonardita)', '20 litros', 11.00, 15.00, 80, 4);
CALL agregar_producto('FITO HUMIC 20', 'Ácidos Húmicos (Leonardita)', '200 litros', 8.00, 15.00, 100, 4);

-- Nutrientes Específicos (Potasio, Fósforo, Boro, Calcio, Magnesio)
CALL agregar_producto('FITO K – 50', 'Potasio', '12 litros', 18.00, 28.00, 50, 5);
CALL agregar_producto('FITO K – 50', 'Potasio', '20 litros', 16.00, 25.00, 70, 5);
CALL agregar_producto('FITO K – 50', 'Potasio', '200 litros', 13.00, 20.00, 90, 5);

CALL agregar_producto('FITO POWER', 'Fósforo', '12 litros', 18.00, 28.00, 40, 5);
CALL agregar_producto('FITO POWER', 'Fósforo', '20 litros', 16.00, 25.00, 60, 5);
CALL agregar_producto('FITO POWER', 'Fósforo', '200 litros', 13.00, 20.00, 80, 5);

CALL agregar_producto('FITO BORO', 'Boro', '12 litros', 18.00, 28.00, 30, 5);
CALL agregar_producto('FITO BORO', 'Boro', '20 litros', 16.00, 25.00, 50, 5);
CALL agregar_producto('FITO BORO', 'Boro', '200 litros', 13.00, 20.00, 70, 5);

CALL agregar_producto('FITO Ca/B/Zn', 'Calcio, Boro, Zinc', '12 litros', 18.00, 28.00, 80, 5);
CALL agregar_producto('FITO Ca/B/Zn', 'Calcio, Boro, Zinc', '20 litros', 16.00, 25.00, 100, 5);
CALL agregar_producto('FITO Ca/B/Zn', 'Calcio, Boro, Zinc', '200 litros', 13.00, 20.00, 120, 5);

CALL agregar_producto('FITO MAGNESIO', 'Magnesio', '12 litros', 18.00, 28.00, 60, 5);

