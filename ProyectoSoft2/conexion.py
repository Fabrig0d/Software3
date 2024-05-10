import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    # port = "3306,"
    database = "fitogreen"
)

# print(conn)

cursor = conn.cursor()

#-----------------------------------------------------------------------------------
#
# CREACION BASE DE DATOS
# cursor.execute("CREATE DATABASE fitogreen")

# MOSTRAR BASES DE DATOS CREADAS
# cursor.execute("SHOW DATABASES")
# for bd in cursor:
#     print(bd)

#-----------------------------------------------------------------
#
# CREACION DE TABLAS
# sql = """CREATE TABLE clientes (id INT AUTO_INCREMENT PRIMARY KEY, dni VARCHAR(8), nombre VARCHAR(100), apellido VARCHAR(100), correo VARCHAR(100) UNIQUE, direccion VARCHAR(200))"""
# sql = """CREATE TABLE tipoEmpleado (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100))"""
# sql = """CREATE TABLE empleados (id INT AUTO_INCREMENT PRIMARY KEY, dni VARCHAR(8), nombre VARCHAR(100),  apellido VARCHAR(100), correo VARCHAR(100) UNIQUE, sueldo DECIMAL(6,2), tipo INT, FOREIGN KEY (tipo) REFERENCES tipoEmpleado(id))"""
# sql = """CREATE TABLE tipoUsuario (id INT AUTO_INCREMENT PRIMARY KEY, descripción VARCHAR(100))"""
# sql = """CREATE TABLE usuario (id INT AUTO_INCREMENT PRIMARY KEY, correo_cli VARCHAR(100), correo_emp VARCHAR(100), usuario VARCHAR(100), contraseña VARCHAR(200), tipo INT, FOREIGN KEY (correo_cli) REFERENCES clientes(correo), FOREIGN KEY (correo_emp) REFERENCES empleados(correo), FOREIGN KEY (tipo) REFERENCES tipoUsuario(id))"""
# sql = """CREATE TABLE tipoProducto (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100))"""
# sql = """CREATE TABLE productos (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100), composicion VARCHAR(100),  precio DECIMAL(6,2), stock INT, tipo INT, FOREIGN KEY (tipo) REFERENCES tipoProducto(id))"""
# cursor.execute(sql)

# MOSTRAR TABLAS
# cursor.execute("SHOW TABLES")
# for dato in cursor:
#     print(dato)

#--------------------------------------------------------------------
#
# PROCEDIMIENTOS ALMACENADOS
# sqlsp = """
# CREATE PROCEDURE insertar_emp(IN dni_emp VARCHAR(8), IN nombre_emp VARCHAR(100), IN apellido_emp VARCHAR(100), IN correo_emp VARCHAR(100), IN sueldo_emp DECIMAL(6,2), IN tipo_emp INT)
# INSERT INTO empleados (dni, nombre, apellido, correo, sueldo, tipo) VALUES (dni_emp, nombre_emp, apellido_emp, correo_emp, sueldo_emp, tipo_emp);
# """

# sqlsp = """
# CREATE PROCEDURE editar_emp(IN id_emp INT, IN dni_emp VARCHAR(8), IN nombre_emp VARCHAR(100), IN apellido_emp VARCHAR(100), IN correo_emp VARCHAR(100), IN sueldo_emp DECIMAL(6,2), IN tipo_emp INT)
# UPDATE empleados SET dni = dni_emp, nombre = nombre_emp, apellido = apellido_emp, correo = correo_emp, sueldo = sueldo_emp, tipo = nuevo_tipo_emp WHERE id = id_emp;
# """

# sqlsp = """
# CREATE PROCEDURE listar_emp()
# SELECT * FROM empleados;
# """

# sqlsp = """
# CREATE PROCEDURE buscar_emp()
# SELECT * FROM empleados WHERE (dni_emp IS NULL OR dni = dni_emp) AND (nombre_emp IS NULL OR nombre LIKE CONCAT(nombre_emp, '%')) AND (apellido_emp IS NULL OR apellido LIKE CONCAT(apellido_emp, '%'))
# """


# cursor.execute(sqlsp)
# conn.commit()

# MOSTRAR PROCEDIMIENTOS ALMACENADOS
# showSP = """
#     SELECT SPECIFIC_NAME
#     FROM information_schema.ROUTINES
#     WHERE ROUTINE_TYPE = 'PROCEDURE'
#     AND ROUTINE_SCHEMA = 'fitogreen';
# """
# cursor.execute(showSP)
# for sp in cursor:
#      print(sp[0])

#-----------------------------------------------
# INSERTAR DATOS EN TABLAS
# sql = """INSERT INTO clientes (dni, nombre, apellido, correo, direccion) VALUES (%s, %s, %s, %s, %s)"""
# valores = [
#     (12345678, abcdefg, abcdefg, abcdefg, abcdefg),
#     (12345678, abcdefg, abcdefg, abcdefg, abcdefg),
# ]

# sql = """INSERT INTO tipoEmpleados (nombre) VALUES (%s)"""
# valores = [ 
#     "Asesor de Ventas",
#     "Administrador",
# ]

# sql = """CALL insertar_emp(%s, %s, %s, %s, %s)"""
# valores = [
#     ("12345678", "abcdefg", "abcdefg", "abcdefg", 1, 5000.50),
#     ("12345678", "abcdefg", "abcdefg", "abcdefg", 2, 5000.50),
# ]

# cursor.executemany(sql, valores)
# conn.commit()
# print(cursor.rowcount, "registros insertados")


conn.close