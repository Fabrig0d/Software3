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
    id_cli INT AUTO_INCREMENT PRIMARY KEY,
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
    username VARCHAR(100)
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
    username VARCHAR(100)
);

-- Tabla para administrador
CREATE TABLE Administrador (
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
    username VARCHAR(100)
);

-- Tabla para tipos de productos (categorías)
CREATE TABLE tipo_producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE
);

-- Tabla para productos
CREATE TABLE productos (
    producto_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion VARCHAR(200),
    presentacion varchar(100),
    precio_dis DECIMAL(8,2),
	precio_pub DECIMAL(8,2),
	stock INT,
    tipo_producto_id INT,
    FOREIGN KEY (tipo_producto_id) REFERENCES tipo_producto(id)
);

CREATE TABLE Pagos (
    pago_id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    fecha_pago DATE,
    monto DECIMAL(10, 2),
    metodo_pago VARCHAR(50),
    estado VARCHAR(20),
   FOREIGN KEY (id_cliente) REFERENCES clientes(id_cli)
);

CREATE TABLE Pedidos (
    pedido_id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    nombre_cli VARCHAR(100),
    apellido_cli VARCHAR(100),
    direccion_pedido Varchar(200),
    fecha_pedido DATE,
    metodo_pago Varchar(40),
    total DECIMAL(10, 2),
    estado VARCHAR(20),
    codigo_orden VARCHAR(100),
	FOREIGN KEY (id_cliente) REFERENCES clientes(id_cli)
);

CREATE TABLE DetallesPedidos (
    detalle_id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    producto_id INT,
	nombre_cli VARCHAR(100),
    apellido_cli VARCHAR(100),
    direccion Varchar(200),
    fecha_pedido DATE,
    cantidad INT,
    metodo_pago Varchar(40),
    precio_unitario DECIMAL(10, 2),
    FOREIGN KEY (pedido_id) REFERENCES Pedidos(pedido_id),
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
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














-- ADMINISTRADOR

DELIMITER //
CREATE PROCEDURE agregar_administrador(
    IN p_nombre VARCHAR(100),
    IN p_apellidos VARCHAR(100),
    IN p_correo VARCHAR(100),
    IN p_telefono_celular VARCHAR(20),
    IN p_dni VARCHAR(15),
    IN p_fecha_nacimiento DATE,
    IN p_direccion VARCHAR(200),
    IN p_sueldo DECIMAL(8,2),
    IN p_rol VARCHAR(100),
    IN p_username VARCHAR(100)
)
BEGIN
    INSERT INTO Administrador (nombre, apellidos, correo, telefono_celular, dni, fecha_nacimiento, direccion, sueldo, rol, username)
    VALUES (p_nombre, p_apellidos, p_correo, p_telefono_celular, p_dni, p_fecha_nacimiento, p_direccion, p_sueldo, p_rol, p_username);
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE buscar_administrador(
    IN p_id INT
)
BEGIN
    SELECT * FROM Administrador WHERE id = p_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE editar_administrador(
    IN p_id INT,
    IN p_nombre VARCHAR(100),
    IN p_apellidos VARCHAR(100),
    IN p_correo VARCHAR(100),
    IN p_telefono_celular VARCHAR(20),
    IN p_dni VARCHAR(15),
    IN p_fecha_nacimiento DATE,
    IN p_direccion VARCHAR(200),
    IN p_sueldo DECIMAL(8,2),
    IN p_rol VARCHAR(100),
    IN p_username VARCHAR(100)
)
BEGIN
    UPDATE Administrador
    SET nombre = p_nombre, apellidos = p_apellidos, correo = p_correo, 
        telefono_celular = p_telefono_celular, dni = p_dni, fecha_nacimiento = p_fecha_nacimiento, 
        direccion = p_direccion, sueldo = p_sueldo, rol = p_rol, username = p_username
    WHERE id = p_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE eliminar_administrador(
    IN p_id INT
)
BEGIN
    DELETE FROM Administrador WHERE id = p_id;
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
    IN p_producto_id INT,
    IN p_nombre VARCHAR(100),
    IN p_descripcion VARCHAR(200),
    IN p_presentacion VARCHAR(100),
    IN p_precio_dis DECIMAL(8,2),
    IN p_precio_pub DECIMAL(8,2),
    IN p_stock INT,
    IN p_tipo_producto_id INT
)
BEGIN
    UPDATE productos
    SET nombre = p_nombre, descripcion = p_descripcion, presentacion = p_presentacion,
        precio_dis = p_precio_dis, precio_pub = p_precio_pub, stock = p_stock, tipo_producto_id = p_tipo_producto_id
    WHERE producto_id = p_producto_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE eliminar_producto(
    IN p_producto_id INT
)
BEGIN
    DELETE FROM productos WHERE producto_id = p_producto_id;
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE buscar_producto(
    IN p_producto_id INT
)
BEGIN
    SELECT * FROM productos WHERE producto_id = p_producto_id;
END //
DELIMITER ;













-- PEDIDOS

DELIMITER //
CREATE PROCEDURE agregar_pedido(
    IN p_id_cliente INT,
    IN p_nombre_cli VARCHAR(100),
    IN p_apellido_cli VARCHAR(100),
    IN p_direccion_pedido VARCHAR(200),
    IN p_fecha_pedido DATE,
    IN p_total DECIMAL(10, 2),
    IN p_estado VARCHAR(20)
)
BEGIN
    INSERT INTO Pedidos (id_cliente, nombre_cli, apellido_cli, direccion_pedido, fecha_pedido, total, estado)
    VALUES (p_id_cliente, p_nombre_cli, p_apellido_cli, p_direccion_pedido, p_fecha_pedido, p_total, p_estado);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE buscar_pedido(
    IN p_pedido_id INT
)
BEGIN
    SELECT * FROM Pedidos WHERE pedido_id = p_pedido_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE editar_pedido(
    IN p_pedido_id INT,
    IN p_id_cliente INT,
    IN p_nombre_cli VARCHAR(100),
    IN p_apellido_cli VARCHAR(100),
    IN p_direccion_pedido VARCHAR(200),
    IN p_fecha_pedido DATE,
    IN p_total DECIMAL(10, 2),
    IN p_estado VARCHAR(20)
)
BEGIN
    UPDATE Pedidos
    SET id_cliente = p_id_cliente, nombre_cli = p_nombre_cli, apellido_cli = p_apellido_cli,
        direccion_pedido = p_direccion_pedido, fecha_pedido = p_fecha_pedido,
        total = p_total, estado = p_estado
    WHERE pedido_id = p_pedido_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE eliminar_pedido(
    IN p_pedido_id INT
)
BEGIN
    DELETE FROM Pedidos WHERE pedido_id = p_pedido_id;
END //
DELIMITER ;











-- PAGOS
DELIMITER //
CREATE PROCEDURE agregar_pago(
    IN p_id_cliente INT,
    IN p_fecha_pago DATE,
    IN p_monto DECIMAL(10, 2),
    IN p_metodo_pago VARCHAR(50),
    IN p_estado VARCHAR(20)
)
BEGIN
    INSERT INTO Pagos (id_cliente, fecha_pago, monto, metodo_pago, estado)
    VALUES (p_id_cliente, p_fecha_pago, p_monto, p_metodo_pago, p_estado);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE buscar_pago(
    IN p_pago_id INT
)
BEGIN
    SELECT * FROM Pagos WHERE pago_id = p_pago_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE editar_pago(
    IN p_pago_id INT,
    IN p_id_cliente INT,
    IN p_fecha_pago DATE,
    IN p_monto DECIMAL(10, 2),
    IN p_metodo_pago VARCHAR(50),
    IN p_estado VARCHAR(20)
)
BEGIN
    UPDATE Pagos
    SET id_cliente = p_id_cliente, fecha_pago = p_fecha_pago, monto = p_monto,
        metodo_pago = p_metodo_pago, estado = p_estado
    WHERE pago_id = p_pago_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE eliminar_pago(
    IN p_pago_id INT
)
BEGIN
    DELETE FROM Pagos WHERE pago_id = p_pago_id;
END //
DELIMITER ;











-- DETALLES PEDIDOS


DELIMITER //
CREATE PROCEDURE agregar_detalle_pedido(
    IN p_pedido_id INT,
    IN p_producto_id INT,
    IN p_nombre_cli VARCHAR(100),
    IN p_apellido_cli VARCHAR(100),
    IN p_direccion VARCHAR(200),
    IN p_fecha_pedido DATE,
    IN p_cantidad INT,
    IN p_metodo_pago VARCHAR(40),
    IN p_precio_unitario DECIMAL(10, 2)
)
BEGIN
    INSERT INTO DetallesPedidos (pedido_id, producto_id, nombre_cli, apellido_cli, direccion, fecha_pedido, cantidad, metodo_pago, precio_unitario)
    VALUES (p_pedido_id, p_producto_id, p_nombre_cli, p_apellido_cli, p_direccion, p_fecha_pedido, p_cantidad, p_metodo_pago, p_precio_unitario);
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE buscar_detalle_pedido(
    IN p_detalle_id INT
)
BEGIN
    SELECT * FROM DetallesPedidos WHERE detalle_id = p_detalle_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE editar_detalle_pedido(
    IN p_detalle_id INT,
    IN p_pedido_id INT,
    IN p_producto_id INT,
    IN p_nombre_cli VARCHAR(100),
    IN p_apellido_cli VARCHAR(100),
    IN p_direccion VARCHAR(200),
    IN p_fecha_pedido DATE,
    IN p_cantidad INT,
    IN p_metodo_pago VARCHAR(40),
    IN p_precio_unitario DECIMAL(10, 2)
)
BEGIN
    UPDATE DetallesPedidos
    SET pedido_id = p_pedido_id, producto_id = p_producto_id, nombre_cli = p_nombre_cli,
        apellido_cli = p_apellido_cli, direccion = p_direccion, fecha_pedido = p_fecha_pedido,
        cantidad = p_cantidad, metodo_pago = p_metodo_pago, precio_unitario = p_precio_unitario
    WHERE detalle_id = p_detalle_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE eliminar_detalle_pedido(
    IN p_detalle_id INT
)
BEGIN
    DELETE FROM DetallesPedidos WHERE detalle_id = p_detalle_id;
END //
DELIMITER ;
































describe productos;


-- TIPO DE PRODUCTOS

CALL agregar_tipo_producto('Algas Marinas y Fitohormonas');
CALL agregar_tipo_producto('Fungicidas Biológicos');
CALL agregar_tipo_producto('Aminoácidos');
CALL agregar_tipo_producto('Ácidos Húmicos');
CALL agregar_tipo_producto('Nutrientes Específicos');	

-- PRODUCTOS

-- FITO ALGAS: Algas Marinas + Fitohormonas
CALL agregar_producto('FITO ALGAS', 'Algas Marinas + Fitohormonas', '1 litro', 30.00, 50.00, 20, 1);
CALL agregar_producto('FITO ALGAS', 'Algas Marinas + Fitohormonas', '12 litros', 30.00, 50.00, 100, 1);
CALL agregar_producto('FITO ALGAS', 'Algas Marinas + Fitohormonas', '20 litros', 25.00, 40.00, 150, 1);
CALL agregar_producto('FITO ALGAS', 'Algas Marinas + Fitohormonas', '200 litros', 20.00, 35.00, 200, 1);

-- ALGAS SHEER: Algas marinas
CALL agregar_producto('ALGAS SHEER', 'Algas marinas', '1 litro', 20.00, 35.00, 10, 1);
CALL agregar_producto('ALGAS SHEER', 'Algas marinas', '12 litros', 20.00, 35.00, 80, 1);
CALL agregar_producto('ALGAS SHEER', 'Algas marinas', '20 litros', 15.00, 30.00, 120, 1);
CALL agregar_producto('ALGAS SHEER', 'Algas marinas', '200 litros', 10.00, 20.00, 50, 1);

-- HONGO STOP: Fungicida Biológico
CALL agregar_producto('HONGO STOP', 'Fungicida Biológico', '1 litro', 55.00, 65.00, 30, 2);
CALL agregar_producto('HONGO STOP', 'Fungicida Biológico', '12 litros', 55.00, 65.00, 90, 2);
CALL agregar_producto('HONGO STOP', 'Fungicida Biológico', '20 litros', 45.00, 60.00, 110, 2);
CALL agregar_producto('HONGO STOP', 'Fungicida Biológico', '200 litros', 40.00, 55.00, 150, 2);

-- FITO AMINO: Aminoácidos
CALL agregar_producto('FITO AMINO', 'Aminoácidos', '1 litro', 35.00, 60.00, 25, 3);
CALL agregar_producto('FITO AMINO', 'Aminoácidos', '12 litros', 35.00, 60.00, 70, 3);
CALL agregar_producto('FITO AMINO', 'Aminoácidos', '20 litros', 30.00, 50.00, 100, 3);
CALL agregar_producto('FITO AMINO', 'Aminoácidos', '200 litros', 25.00, 50.00, 130, 3);

-- FITO HUMIC 20: Ácidos Húmicos (Leonardita)
CALL agregar_producto('FITO HUMIC 20', 'Ácidos Húmicos (Leonardita)', '1 litro', 15.00, 20.00, 15, 4);
CALL agregar_producto('FITO HUMIC 20', 'Ácidos Húmicos (Leonardita)', '12 litros', 15.00, 20.00, 60, 4);
CALL agregar_producto('FITO HUMIC 20', 'Ácidos Húmicos (Leonardita)', '20 litros', 11.00, 15.00, 80, 4);
CALL agregar_producto('FITO HUMIC 20', 'Ácidos Húmicos (Leonardita)', '200 litros', 8.00, 15.00, 100, 4);

-- Nutrientes Específicos (Potasio, Fósforo, Boro, Calcio, Magnesio)

CALL agregar_producto('FITO K – 50', 'Potasio', '1 litro', 18.00, 28.00, 10, 5);
CALL agregar_producto('FITO K – 50', 'Potasio', '1 litro', 18.00, 28.00, 10, 5);
CALL agregar_producto('FITO K – 50', 'Potasio', '12 litros', 18.00, 28.00, 50, 5);
CALL agregar_producto('FITO K – 50', 'Potasio', '20 litros', 16.00, 25.00, 70, 5);
CALL agregar_producto('FITO K – 50', 'Potasio', '200 litros', 13.00, 20.00, 90, 5);

CALL agregar_producto('FITO POWER', 'Fósforo', '1 litro', 18.00, 28.00, 10, 5);
CALL agregar_producto('FITO POWER', 'Fósforo', '12 litros', 18.00, 28.00, 40, 5);
CALL agregar_producto('FITO POWER', 'Fósforo', '20 litros', 16.00, 25.00, 60, 5);
CALL agregar_producto('FITO POWER', 'Fósforo', '200 litros', 13.00, 20.00, 80, 5);

CALL agregar_producto('FITO BORO', 'Boro', '1 litro', 18.00, 28.00, 10, 5);
CALL agregar_producto('FITO BORO', 'Boro', '12 litros', 18.00, 28.00, 30, 5);
CALL agregar_producto('FITO BORO', 'Boro', '20 litros', 16.00, 25.00, 50, 5);
CALL agregar_producto('FITO BORO', 'Boro', '200 litros', 13.00, 20.00, 70, 5);

CALL agregar_producto('FITO Ca/B/Zn', 'Calcio, Boro, Zinc', '1 litro', 18.00, 28.00, 15, 5);
CALL agregar_producto('FITO Ca/B/Zn', 'Calcio, Boro, Zinc', '12 litros', 18.00, 28.00, 80, 5);
CALL agregar_producto('FITO Ca/B/Zn', 'Calcio, Boro, Zinc', '20 litros', 16.00, 25.00, 100, 5);
CALL agregar_producto('FITO Ca/B/Zn', 'Calcio, Boro, Zinc', '200 litros', 13.00, 20.00, 120, 5);

CALL agregar_producto('FITO MAGNESIO', 'Magnesio', '1 litro', 18.00, 28.00, 12, 5);
CALL agregar_producto('FITO MAGNESIO', 'Magnesio', '12 litros', 18.00, 28.00, 60, 5);




