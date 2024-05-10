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

# cursor.execute("CREATE DATABASE fitogreen")

# sql = """CREATE TABLE clientes (id INT AUTO_INCREMENT PRIMARY KEY,
#                                 + dni VARCHAR(8),
#                                 + nombre VARCHAR(100), 
#                                 + apellido VARCHAR(100), 
#                                 + correo VARCHAR(100),
#                                 + direccion VARCHAR(200))"""

# sql = """CREATE TABLE tipoEmpleado (id INT AUTO_INCREMENT PRIMARY KEY,
#                                     + nombre VARCHAR(100))"""

# sql = """CREATE TABLE empleados (id INT AUTO_INCREMENT PRIMARY KEY,
#                                  + dni VARCHAR(8),
#                                  + nombre VARCHAR(100), 
#                                  + apellido VARCHAR(100),
#                                  + correo VARCHAR(100),
#                                  + sueldo DECIMAL(6,2),
#                                  + tipo INT,
#                                  + FOREIGN KEY (tipo) REFERENCES tipoEmpleado(id))"""

# sql = """CREATE TABLE tipoUsuario (id INT AUTO_INCREMENT PRIMARY KEY,
#                                    + descripción VARCHAR(100))"""

# sql = """CREATE TABLE usuario (id INT AUTO_INCREMENT PRIMARY KEY,
#                                + correo_cli VARCHAR(100),
#                                + correo_emp VARCHAR(100),
#                                + usuario VARCHAR(100),
#                                + contraseña VARCHAR(200)
#                                + tipo INT,
#                                + FOREIGN KEY (correo_cli) REFERENCES clientes(correo),
#                                + FOREIGN KEY (correo_emp) REFERENCES empleado(correo),
#                                + FOREIGN KEY (tipo) REFERENCES tipoUsuario(id))"""

# sql = """CREATE TABLE tipoProducto (id INT AUTO_INCREMENT PRIMARY KEY,
#                                     + nombre VARCHAR(100))"""

# sql = """CREATE TABLE productos (id INT AUTO_INCREMENT PRIMARY KEY,
#                                  + nombre VARCHAR(100),
#                                  + composicion VARCHAR(100), 
#                                  + precio DECIMAL(6,2),
#                                  + stock INT,
#                                  + tipo INT,
#                                  + FOREIGN KEY (tipo) REFERENCES tipoProducto(id))"""

# sql = """CREATE TABLE tipoMateriaPrima (id INT AUTO_INCREMENT PRIMARY KEY,
#                                         + nombre VARCHAR(100))"""

# sql = """CREATE TABLE materiaPrima (id INT AUTO_INCREMENT PRIMARY KEY,
#                                     + nombre VARCHAR(100),
#                                     + stock VARCHAR(100), 
#                                     + proveedor DECIMAL(6,2),
#                                     + tipo INT,
#                                     + FOREIGN KEY (tipo) REFERENCES tipoMateriaPrima(id))"""



cursor.execute("SHOW TABLES")

for dato in cursor:
    print(dato)

# cursor.execute("SHOW DATABASES")

# for bd in cursor:
#     print(bd)

conn.commit()

conn.close