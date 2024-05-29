CREATE DATABASE fitogreen;

USE fitogreen;

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(8), 
    nombre VARCHAR(100), 
    apellido VARCHAR(100), 
    correo VARCHAR(100) UNIQUE, 
    direccion VARCHAR(200)
);

CREATE TABLE tipoEmpleado (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    nombre VARCHAR(100)
);

CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    dni VARCHAR(8), 
    nombre VARCHAR(100),  
    apellido VARCHAR(100), 
    correo VARCHAR(100) UNIQUE, 
    sueldo DECIMAL(6,2), 
    tipo INT, 
    FOREIGN KEY (tipo) REFERENCES tipoEmpleado(id)
);

CREATE TABLE tipoUsuario (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    descripción VARCHAR(100)
);

CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    correo_cli VARCHAR(100), 
    correo_emp VARCHAR(100), 
    usuario VARCHAR(100), 
    contraseña VARCHAR(200), 
    tipo INT, 
    FOREIGN KEY (correo_cli) REFERENCES clientes(correo), 
    FOREIGN KEY (correo_emp) REFERENCES empleados(correo), 
    FOREIGN KEY (tipo) REFERENCES tipoUsuario(id)
);

CREATE TABLE tipoProducto (
	id INT AUTO_INCREMENT PRIMARY KEY, 
	nombre VARCHAR(100)
);

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    composicion VARCHAR(100),
    presentacion  VARCHAR(100),
    precio_distr DECIMAL(6 , 2 ),
    precio_publico DECIMAL(6 , 2 ),
    stock INT,
    tipo INT,
    FOREIGN KEY (tipo)
        REFERENCES tipoProducto (id)
);


--- PROCEDIMIENTOS ALMACENADOS ---

--- CLIENTES ---

DELIMITER //
CREATE PROCEDURE insertar_cli(
    IN dni_cli VARCHAR(8), 
    IN nombre_cli VARCHAR(100), 
    IN apellido_cli VARCHAR(100), 
    IN correo_cli VARCHAR(100), 
    IN direccion_cli VARCHAR(200)
)
BEGIN
    INSERT INTO clientes (dni, nombre, apellido, correo, direccion)
    VALUES (dni_cli, nombre_cli, apellido_cli, correo_cli, direccion_cli);
END;

DELIMITER //
CREATE PROCEDURE editar_cli(
    IN id_cli INT, 
    IN dni_cli VARCHAR(8), 
    IN nombre_cli VARCHAR(100), 
    IN apellido_cli VARCHAR(100), 
    IN correo_cli VARCHAR(100), 
    IN direccion_cli VARCHAR(200)
)
BEGIN
    UPDATE clientes 
    SET 
        dni = dni_cli, 
        nombre = nombre_cli, 
        apellido = apellido_cli, 
        correo = correo_cli, 
        direccion = direccion_cli 
    WHERE id = id_cli;
END;
 
DELIMITER //
CREATE PROCEDURE listar_cli()
BEGIN
    SELECT * FROM clientes;
END;


DELIMITER //
CREATE PROCEDURE buscar_cli(
    IN dni_cli VARCHAR(8), 
    IN nombre_cli VARCHAR(100), 
    IN apellido_cli VARCHAR(100)
)
BEGIN
    SELECT * FROM clientes 
    WHERE (dni_cli IS NULL OR dni = dni_cli)
    AND (nombre_cli IS NULL OR nombre LIKE CONCAT(nombre_cli, '%'))
    AND (apellido_cli IS NULL OR apellido LIKE CONCAT(apellido_cli, '%'));
END;

--- TIPO DE EMPLEADO ---

DELIMITER //
CREATE PROCEDURE insertar_tipoEmp(
    IN nombre_tipoEmp VARCHAR(100)
)
BEGIN
    INSERT INTO tipoEmpleado (nombre) 
    VALUES (nombre_tipoEmp);
END;



DELIMITER //
CREATE PROCEDURE editar_tipoEmp(
    IN id_tipoEmp INT, 
    IN nombre_tipoEmp VARCHAR(100)
)
BEGIN
    UPDATE tipoEmpleado 
    SET nombre = nombre_tipoEmp 
    WHERE id = id_tipoEmp;
END;

DELIMITER //
CREATE PROCEDURE listar_tipoEmp()
BEGIN
    SELECT * FROM tipoEmpleado;
END;


DELIMITER //
CREATE PROCEDURE buscar_tipoEmp(
    IN nombre_tipoEmp VARCHAR(100) 
)
BEGIN
    SELECT * FROM tipoEmpleado 
    WHERE (nombre_tipoEmp IS NULL OR nombre LIKE CONCAT(nombre_tipoEmp, '%'));
END;

--- EMPLEADO ---

DELIMITER //
CREATE PROCEDURE insertar_emp(
    IN dni_emp VARCHAR(8), 
    IN nombre_emp VARCHAR(100), 
    IN apellido_emp VARCHAR(100), 
    IN correo_emp VARCHAR(100), 
    IN sueldo_emp DECIMAL(6,2), 
    IN tipo_emp INT
)
BEGIN
    INSERT INTO empleados (dni, nombre, apellido, correo, sueldo, tipo) 
    VALUES (dni_emp, nombre_emp, apellido_emp, correo_emp, sueldo_emp, tipo_emp);
END;

DELIMITER //
CREATE PROCEDURE editar_emp(
    IN id_emp INT, 
    IN dni_emp VARCHAR(8), 
    IN nombre_emp VARCHAR(100), 
    IN apellido_emp VARCHAR(100), 
    IN correo_emp VARCHAR(100), 
    IN sueldo_emp DECIMAL(6,2), 
    IN tipo_emp INT)
BEGIN
    UPDATE empleados 
    SET    
        dni = dni_emp, 
        nombre = nombre_emp, 
        apellido = apellido_emp, 
        correo = correo_emp, 
        sueldo = sueldo_emp, 
        tipo = nuevo_tipo_emp 
    WHERE id = id_emp;
END;


DELIMITER //
CREATE PROCEDURE listar_emp()
BEGIN
    SELECT * FROM empleados;
END;


DELIMITER //
CREATE PROCEDURE buscar_emp()
BEGIN
    SELECT * FROM empleados 
    WHERE (dni_emp IS NULL OR dni = dni_emp) 
    AND (nombre_emp IS NULL OR nombre LIKE CONCAT(nombre_emp, '%')) 
    AND (apellido_emp IS NULL OR apellido LIKE CONCAT(apellido_emp, '%'));
END;


--- TIPO DE USUARIO ---

DELIMITER //
CREATE PROCEDURE insertar_tipoUsu(
    IN nombre_tipoUsu VARCHAR(100)
)
BEGIN
    INSERT INTO tipoUsuario (nombre) 
    VALUES (nombre_tipoUsu);
END;

DELIMITER //
CREATE PROCEDURE editar_tipoUsu(
    IN id_tipoUsu INT, 
    IN nombre_tipoUsu VARCHAR(100) 
)
BEGIN
    UPDATE tipoUsuario
    SET nombre = nombre_tipoUsu 
    WHERE id = id_tipoUsu;
END;


DELIMITER //
CREATE PROCEDURE listar_tipoUsu()
BEGIN
    SELECT * FROM tipoUsuario;
END;

DELIMITER //
CREATE PROCEDURE buscar_tipoUsu(
    IN nombre_tipoUsu VARCHAR(100)
)
BEGIN
    SELECT * FROM tipoUsuario
    WHERE (nombre_tipoUsu IS NULL OR nombre LIKE CONCAT(nombre_tipoUsu, '%'));
END;

--- USUARIO ---

DELIMITER //
CREATE PROCEDURE insertar_cliUsu(
    IN correo_cliUsu VARCHAR(100), 
    IN usuario_usu VARCHAR(100), 
    IN contraseña_usu VARCHAR(200),
    IN tipo_usu INT
)
BEGIN
    INSERT INTO usuario (correo_cli, usuario, contraseña, tipo) 
    VALUES (correo_cliUsu, usuario_usu, contraseña_usu, tipo_usu);
END;

DELIMITER //
CREATE PROCEDURE insertar_empUsu(
    IN correo_empUsu VARCHAR(100), 
    IN usuario_usu VARCHAR(100), 
    IN contraseña_usu VARCHAR(200),
    IN tipo_usu INT
)
BEGIN
    INSERT INTO usuario (correo_emp, usuario, contraseña, tipo) 
    VALUES (correo_empUsu, usuario_usu, contraseña_usu, tipo_usu);
END;

DELIMITER //
CREATE PROCEDURE editar_cliUsu(
    IN id_usu INT,
    IN correo_cliUsu VARCHAR(100), 
    IN usuario_usu VARCHAR(100), 
    IN contraseña_usu VARCHAR(200),
    IN tipo_usu INT
)
BEGIN
    UPDATE usuario 
    SET    
        correo_cli = correo_cliUsu, 
        usuario = usuario_usu,
        contraseña = contraseña_usu, 
        tipo = tipo_usu
    WHERE id = id_usu;
END;

DELIMITER //
CREATE PROCEDURE editar_empUsu(
    IN id_usu INT,
    IN correo_empUsu VARCHAR(100), 
    IN usuario_usu VARCHAR(100), 
    IN contraseña_usu VARCHAR(200),
    IN tipo_usu INT
)
BEGIN
    UPDATE usuario 
    SET    
        correo_emp = correo_empUsu,  
        usuario = usuario_usu,
        contraseña = contraseña_usu, 
        tipo = tipo_usu
    WHERE id = id_usu;
END;

DELIMITER //
CREATE PROCEDURE listar_cliUsu(
    IN correo_cliUsu VARCHAR(100)
)
BEGIN
    SELECT * FROM usuario
    WHERE correo_cliUsu IS NOT NULL;
END;

DELIMITER //
CREATE PROCEDURE listar_empUsu(
    IN correo_empUsu VARCHAR(100)
)
BEGIN
    SELECT * FROM usuario
    WHERE correo_empUsu IS NOT NULL;
END;

DELIMITER //
CREATE PROCEDURE buscar_usu(
    IN usuario_usu VARCHAR(100)
)
BEGIN
    SELECT * FROM usuario 
    WHERE (usuario_usu IS NULL OR usuario LIKE CONCAT(usuario_usu, '%'));
END;

--- TIPO DE PRODUCTO ---

DELIMITER //
CREATE PROCEDURE insertar_tipoProd(
    IN nombre_tipoProd VARCHAR(100)
)
BEGIN
    INSERT INTO tipoProducto (nombre) 
    VALUES (nombre_tipoProd);
END;

DELIMITER //
CREATE PROCEDURE editar_tipoProd(
    IN id_tipoProd INT, 
    IN nombre_tipoProd VARCHAR(100)
)
BEGIN
    UPDATE tipoProducto
    SET nombre = nombre_tipoProd 
    WHERE id = id_tipoProd;
END;

DELIMITER //
CREATE PROCEDURE listar_tipoProd()
BEGIN
    SELECT * FROM tipoProducto;
END;

DELIMITER //
CREATE PROCEDURE buscar_tipoProd(
    IN nombre_tipoProd VARCHAR(100)
)
BEGIN
    SELECT * FROM tipoProducto
    WHERE (nombre_tipoProd IS NULL OR nombre LIKE CONCAT(nombre_tipoProd, '%'));
END;

--- PRODUCTO ---

DELIMITER //
CREATE PROCEDURE insertar_prod(
    IN nombre_prod VARCHAR(100), 
    IN composicion_prod VARCHAR(100), 
    IN presentacion_prod VARCHAR(100),
    IN precio_distr_prod DECIMAL(6,2), 
    IN precio_publico_prod DECIMAL(6,2),
    IN stock_prod INT, 
    IN tipo_prod INT
)
BEGIN
    INSERT INTO productos (nombre, composicion, presentacion, precio_distr, precio_publico, stock, tipo) 
    VALUES (nombre_prod, composicion_prod, presentacion_prod, precio_distr_prod, precio_publico_prod, stock_prod, tipo_prod);
END;

DELIMITER //
CREATE PROCEDURE editar_prod(
    IN id_prod INT, 
    IN nombre_prod VARCHAR(100), 
    IN composicion_prod VARCHAR(100), 
    IN precio_prod DECIMAL(6,2), 
    IN stock_prod INT, 
    IN tipo_prod INT
)
BEGIN
    UPDATE productos
    SET     
        nombre = nombre_prod, 
        composicion = composicion_prod, 
        precio = precio_prod, 
        stock = stock_prod, 
        tipo = tipo_prod 
    WHERE id = id_prod;
END;

DELIMITER //
CREATE PROCEDURE listar_prod()
BEGIN
    SELECT * FROM productos;
END;

DELIMITER //
CREATE PROCEDURE listar_prodxtipo(
    IN tipo_prod INT
)
BEGIN
    SELECT * FROM productos
    WHERE tipo = tipo_prod;
END;

DELIMITER //
CREATE PROCEDURE buscar_prod(
    IN nombre_prod VARCHAR(100), 
    IN composicion_prod VARCHAR(100)
)
BEGIN
    SELECT * FROM productos 
    WHERE (nombre_prod IS NULL OR nombre LIKE CONCAT(nombre_prod, '%')) 
    AND (composicion_prod IS NULL OR composicion LIKE CONCAT(composicion_prod, '%'));
END;

DELIMITER //
CREATE PROCEDURE buscar_prodxMayorOmenorQue(
    IN precio_prod DECIMAL(6,2), 
    IN busqueda VARCHAR(10) 
)
BEGIN
    IF busqueda = 'mayor' THEN
        SELECT * FROM productos 
        WHERE precio > precio_prod;
    ELSEIF busqueda = 'menor' THEN
        SELECT * FROM productos 
        WHERE precio < precio_prod;
    END IF;
END;

CALL insertar_tipoProd('Algas Marinas y Fitohormonas');
CALL insertar_tipoProd('Fungicidas Biológicos');
CALL insertar_tipoProd('Aminoácidos');
CALL insertar_tipoProd('Ácidos Húmicos');
CALL insertar_tipoProd('Nutrientes Específicos');	

-- FITO ALGAS: Algas Marinas + Fitohormonas
CALL insertar_prod('FITO ALGAS', 'Algas Marinas + Fitohormonas', '12 litros', 30.00, 50.00, 100, 1);
CALL insertar_prod('FITO ALGAS', 'Algas Marinas + Fitohormonas', '20 litros', 25.00, 40.00, 150, 1);
CALL insertar_prod('FITO ALGAS', 'Algas Marinas + Fitohormonas', '200 litros', 20.00, 35.00, 200, 1);

-- ALGAS SHEER: Algas marinas
CALL insertar_prod('ALGAS SHEER', 'Algas marinas', '12 litros', 20.00, 35.00, 80, 1);
CALL insertar_prod('ALGAS SHEER', 'Algas marinas', '20 litros', 15.00, 30.00, 120, 1);
CALL insertar_prod('ALGAS SHEER', 'Algas marinas', '200 litros', 10.00, 20.00, 50, 1);

-- HONGO STOP: Fungicida Biológico
CALL insertar_prod('HONGO STOP', 'Fungicida Biológico', '12 litros', 55.00, 65.00, 90, 2);
CALL insertar_prod('HONGO STOP', 'Fungicida Biológico', '20 litros', 45.00, 60.00, 110, 2);
CALL insertar_prod('HONGO STOP', 'Fungicida Biológico', '200 litros', 40.00, 55.00, 150, 2);

-- FITO AMINO: Aminoácidos
CALL insertar_prod('FITO AMINO', 'Aminoácidos', '12 litros', 35.00, 60.00, 70, 3);
CALL insertar_prod('FITO AMINO', 'Aminoácidos', '20 litros', 30.00, 50.00, 100, 3);
CALL insertar_prod('FITO AMINO', 'Aminoácidos', '200 litros', 25.00, 50.00, 130, 3);

-- FITO HUMIC 20: Ácidos Húmicos (Leonardita)
CALL insertar_prod('FITO HUMIC 20', 'Ácidos Húmicos (Leonardita)', '12 litros', 15.00, 20.00, 60, 4);
CALL insertar_prod('FITO HUMIC 20', 'Ácidos Húmicos (Leonardita)', '20 litros', 11.00, 15.00, 80, 4);
CALL insertar_prod('FITO HUMIC 20', 'Ácidos Húmicos (Leonardita)', '200 litros', 8.00, 15.00, 100, 4);

-- Nutrientes Específicos (Potasio, Fósforo, Boro, Calcio, Magnesio)
CALL insertar_prod('FITO K – 50', 'Potasio', '12 litros', 18.00, 28.00, 50, 5);
CALL insertar_prod('FITO K – 50', 'Potasio', '20 litros', 16.00, 25.00, 70, 5);
CALL insertar_prod('FITO K – 50', 'Potasio', '200 litros', 13.00, 20.00, 90, 5);

CALL insertar_prod('FITO POWER', 'Fósforo', '12 litros', 18.00, 28.00, 40, 5);
CALL insertar_prod('FITO POWER', 'Fósforo', '20 litros', 16.00, 25.00, 60, 5);
CALL insertar_prod('FITO POWER', 'Fósforo', '200 litros', 13.00, 20.00, 80, 5);

CALL insertar_prod('FITO BORO', 'Boro', '12 litros', 18.00, 28.00, 30, 5);
CALL insertar_prod('FITO BORO', 'Boro', '20 litros', 16.00, 25.00, 50, 5);
CALL insertar_prod('FITO BORO', 'Boro', '200 litros', 13.00, 20.00, 70, 5);

CALL insertar_prod('FITO Ca/B/Zn', 'Calcio, Boro, Zinc', '12 litros', 18.00, 28.00, 80, 5);
CALL insertar_prod('FITO Ca/B/Zn', 'Calcio, Boro, Zinc', '20 litros', 16.00, 25.00, 100, 5);
CALL insertar_prod('FITO Ca/B/Zn', 'Calcio, Boro, Zinc', '200 litros', 13.00, 20.00, 120, 5);

CALL insertar_prod('FITO MAGNESIO', 'Magnesio', '12 litros', 18.00, 28.00, 60, 5);


CALL listar_tipoProd();
DESC productos;
CALL listar_prod();
CALL listar_cli();

-- Insertar 10 registros adicionales de clientes utilizando el procedimiento almacenado
CALL insertar_cli('11111111', 'Ana', 'López', 'ana@example.com', 'Calle Ancha 111');
CALL insertar_cli('22222222', 'Pedro', 'Sánchez', 'pedro@example.com', 'Avenida del Sol 222');
CALL insertar_cli('33333333', 'Laura', 'García', 'laura@example.com', 'Plaza Central 333');
CALL insertar_cli('44444444', 'Miguel', 'Rodríguez', 'miguel@example.com', 'Calle Estrecha 444');
CALL insertar_cli('55555555', 'Sofía', 'Fernández', 'sofia@example.com', 'Avenida del Río 555');

-- Usuarios
CALL insertar_cliUsu ('ana@example.com', 'anita1','anapsw1','1')

