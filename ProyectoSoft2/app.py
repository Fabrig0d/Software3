from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
import smtplib
import pymysql
from functools import wraps
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import urllib.parse
from math import ceil

# Cargar variables de entorno
env_path = os.path.join(os.path.dirname(__file__), '../ProyectoSoft2/.env')
load_dotenv(env_path)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Configuración de Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# Configuración de la base de datos
password = os.getenv('DB_PASSWORD')
if password is None:
    raise ValueError("La variable de entorno DB_PASSWORD no está definida en el archivo .env")
encoded_password = urllib.parse.quote_plus(password.encode('utf-8'))

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{encoded_password}@localhost/fitogreen'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20))  # Cambiado a VARCHAR(20) para coincidir con la base de datos

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    correo = db.Column(db.String(100), unique=True)
    telefono_celular = db.Column(db.String(20))
    dni_ruc = db.Column(db.String(15))
    fecha_nacimiento = db.Column(db.Date)
    departamento = db.Column(db.String(100))
    provincia = db.Column(db.String(100))
    distrito = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    username = db.Column(db.String(100))


class Empleado(db.Model):
    __tablename__ = 'empleados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    correo = db.Column(db.String(100), unique=True)
    telefono_celular = db.Column(db.String(20))
    dni = db.Column(db.String(15))
    fecha_nacimiento = db.Column(db.Date)
    direccion = db.Column(db.String(200))
    sueldo = db.Column(db.Numeric(8, 2))  
    username = db.Column(db.String(100))

class Administrador(db.Model):
    __tablename__ = 'Administrador'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    correo = db.Column(db.String(100), unique=True)
    telefono_celular = db.Column(db.String(20))
    dni = db.Column(db.String(15))
    fecha_nacimiento = db.Column(db.Date)
    direccion = db.Column(db.String(200))
    sueldo = db.Column(db.Numeric(8, 2))  
    username = db.Column(db.String(100))

class TipoProducto(db.Model):
    __tablename__ = 'tipo_producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    presentacion = db.Column(db.String(100), nullable=True)
    precio_dis = db.Column(db.Numeric(8, 2), nullable=False)
    precio_pub = db.Column(db.Numeric(8, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    tipo_producto_id = db.Column(db.Integer, db.ForeignKey('tipo_producto.id'), nullable=False)
    tipo_producto = db.relationship('TipoProducto', backref=db.backref('productos', lazy=True))

# Carrito de compra (almacenado en memoria, en una aplicación real podría ser una base de datos)
cart = []

@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', products=productos, cart=session.get('cart', []))

@app.route('/carrito')
def carrito():
    cart_items = session.get('cart', [])
    return render_template('carrito.html', cart_items=cart_items)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form['producto_id'])
    product = Producto.query.get(product_id)
    if product:
        cart_item = {'id': product.id, 'name': product.nombre, 'price': product.precio_pub, 'quantity': 1}
        cart = session.get('cart', [])
        cart.append(cart_item)
        session['cart'] = cart
        return redirect(url_for('mostrar_catalogo'))
    else:
        return "Producto no encontrado"

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    return redirect(url_for('carrito'))

@app.route('/borrar_carrito', methods=['POST'])
def borrar_carrito():
    session.pop('cart', None)
    return redirect(url_for('carrito'))

@app.route('/pagar', methods=['POST'])
def pagar():
    # Aquí puedes agregar la lógica para procesar el pago
    return '¡Gracias por su compra!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Contraseña ingresada por el usuario: {password}")
        user = Usuario.query.filter_by(usuario=username).first()  
        if user and check_password_hash(user.contrasena, password):
            session['logged_in'] = True
            session['username'] = username
            session['tipo'] = user.tipo  # Almacenar el tipo de usuario en la sesión
            if user.tipo == 'cliente':
                return redirect(url_for('home_cliente'))
            elif user.tipo == 'empleado':
                return redirect(url_for('home_empleado'))
            elif user.tipo == 'admin':
                return redirect(url_for('home_admin'))
        else:
            flash('Usuario o contraseña incorrectos.', 'error')
    return render_template('login.html')

@app.route('/ruta_protegida')
def ruta_protegida():
    if 'logged_in' in session and session['logged_in'] and session['tipo'] == 'cliente':
        # El usuario está autenticado y es un cliente
        return render_template('ruta_protegida.html')
    else:
        flash('No tienes permiso para acceder a esta página', 'error')
        return redirect(url_for('login'))

@app.route('/home_cliente')
def home_cliente():
    if 'logged_in' in session and session['logged_in'] and session['tipo'] == 'cliente':
        return render_template('home_cliente.html', username=session['username'])
    else:
        flash('Acceso denegado. Debes ser un cliente.', 'error')
        return redirect(url_for('login'))


@app.route('/home_empleado')
def home_empleado():
    if 'logged_in' in session and session['logged_in'] and session['tipo'] == 'empleado':
        return render_template('home_empleado.html', username=session['username'])
    else:
        flash('Acceso denegado. Debes ser un empleado.', 'error')
        return redirect(url_for('login'))
    
@app.route('/home_admin')
def home_admin():
    if 'logged_in' in session and session['logged_in'] and session['tipo'] == 'admin':
        return render_template('home_admin.html', username=session['username'])
    else:
        flash('Acceso denegado. Debes ser un administrador.', 'error')
        return redirect(url_for('login'))

@app.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form['nombre']
    email = request.form['email']
    asunto = request.form['asunto']
    mensaje = request.form['mensaje']
    msg = Message(asunto, sender=app.config['MAIL_DEFAULT_SENDER'], recipients=['fabriziovh01@example.com'])
    msg.body = f"Nombre: {nombre}\nCorreo: {email}\n\nMensaje:\n{mensaje}"
    try:
        mail.send(msg)
        flash('¡Tu mensaje ha sido enviado correctamente!')
    except smtplib.SMTPException as e:
        flash('Error al enviar el mensaje: ' + str(e))
    return redirect(url_for('home_cliente'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('tipo', None)
    return redirect(url_for('login'))

@app.route('/catalogo')
def mostrar_catalogo():
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Número de productos por página
    tipo_producto_id = request.args.get('tipo_producto_id', type=int)

    if tipo_producto_id:
        productos = Producto.query.filter_by(tipo_producto_id=tipo_producto_id).paginate(page=page, per_page=per_page)
    else:
        productos = Producto.query.paginate(page=page, per_page=per_page)

    total_pages = ceil(productos.total / per_page)
    tipos_producto = TipoProducto.query.all()  # Obtener todos los tipos de productos
    return render_template('catalogo.html', productos=productos.items, total_pages=total_pages, current_page=page, tipos_producto=tipos_producto)

@app.route('/catalogo_in')
def catalogo_index():
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Número de productos por página
    tipo_producto_id = request.args.get('tipo_producto_id', type=int)

    if tipo_producto_id:
        productos = Producto.query.filter_by(tipo_producto_id=tipo_producto_id).paginate(page=page, per_page=per_page)
    else:
        productos = Producto.query.paginate(page=page, per_page=per_page)

    total_pages = ceil(productos.total / per_page)
    tipos_producto = TipoProducto.query.all()  # Obtener todos los tipos de productos
    return render_template('catalogo_in.html', productos=productos.items, total_pages=total_pages, current_page=page, tipos_producto=tipos_producto)

@app.route('/catalogo_e')
def catalogo_empleado():
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Número de productos por página
    tipo_producto_id = request.args.get('tipo_producto_id', type=int)

    if tipo_producto_id:
        productos = Producto.query.filter_by(tipo_producto_id=tipo_producto_id).paginate(page=page, per_page=per_page)
    else:
        productos = Producto.query.paginate(page=page, per_page=per_page)

    total_pages = ceil(productos.total / per_page)
    tipos_producto = TipoProducto.query.all()  # Obtener todos los tipos de productos
    return render_template('catalogo_e.html', productos=productos.items, total_pages=total_pages, current_page=page, tipos_producto=tipos_producto)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and session['logged_in'] and session['tipo'] == 'admin':
            return f(*args, **kwargs)
        else:
            flash('Acceso denegado. Debes ser un administrador.', 'error')
            return redirect(url_for('login'))
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Aquí iría tu lógica para verificar si el usuario es un administrador
        # Puedes implementar tu propia lógica de autenticación aquí
        # Por ejemplo, verificar si el usuario está autenticado y si es un administrador
        # Si no es un administrador, puedes redirigirlo a alguna otra página
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register_usuarios', methods=['GET', 'POST'])
@admin_required
def register():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        username = request.form.get('username')
        password = request.form.get('password')
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        correo = request.form.get('correo')
        telefono_celular = request.form.get('telefono_celular')
        dni = request.form.get('dni')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        direccion = request.form.get('direccion')

        if tipo == 'cliente':
            departamento = request.form.get('departamento')
            provincia = request.form.get('provincia')
            distrito = request.form.get('distrito')
            if all([username, password, nombre, apellidos, correo, telefono_celular, dni, fecha_nacimiento, direccion, departamento, provincia, distrito]):
                agregar_cliente(username, password, nombre, apellidos, correo, telefono_celular, dni, fecha_nacimiento, direccion, departamento, provincia, distrito)
                flash('Cliente registrado exitosamente', 'success')
                return redirect(url_for('login'))
            else:
                flash('Por favor complete todos los campos', 'error')

        elif tipo == 'empleado':
            sueldo = request.form.get('sueldo')
            if all([username, password, nombre, apellidos, correo, telefono_celular, dni, fecha_nacimiento, direccion, sueldo]):
                agregar_empleado(username, password, nombre, apellidos, correo, telefono_celular, dni, fecha_nacimiento, direccion, sueldo)
                flash('Empleado registrado exitosamente', 'success')
                return redirect(url_for('login'))
            else:
                flash('Por favor complete todos los campos', 'error')
        
        elif tipo == 'administrador':
            sueldo = request.form.get('sueldo')
            if all([username, password, nombre, apellidos, correo, telefono_celular, dni, fecha_nacimiento, direccion, sueldo]):
                agregar_administrador(username, password, nombre, apellidos, correo, telefono_celular, dni, fecha_nacimiento, direccion, sueldo)
                flash('Administrador registrado exitosamente', 'success')
                return redirect(url_for('login'))
            else:
                flash('Por favor complete todos los campos', 'error')
    
    return render_template('register_usuarios.html')

def agregar_administrador(username, password, nombre, apellidos, correo, telefono_celular, dni, fecha_nacimiento, direccion,sueldo):
    nuevo_administrador = Administrador(
        username=username,
        password=password,  # Recuerda hashear la contraseña
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        telefono_celular=telefono_celular,
        dni=dni,
        fecha_nacimiento=fecha_nacimiento,
        direccion=direccion,
        sueldo=sueldo
    )
    db.session.add(nuevo_administrador)
    db.session.commit()
    return nuevo_administrador

def agregar_cliente(username, password, nombre, apellidos, correo, telefono_celular, dni, fecha_nacimiento,departamento,provincia,distrito,direccion):
    nuevo_cliente = Cliente(
        username=username,
        password=password,  # Recuerda hashear la contraseña
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        telefono_celular=telefono_celular,
        dni_ruc=dni,
        fecha_nacimiento=fecha_nacimiento,
        departamento=departamento,
        provincia=provincia,
        distrito=distrito,
        direccion=direccion
    )
    db.session.add(nuevo_cliente)
    db.session.commit()
    return nuevo_cliente

def agregar_empleado(username, password, nombre, apellidos, correo, telefono_celular, dni, fecha_nacimiento, direccion,sueldo):
    nuevo_empleado = Empleado(
        username=username,
        password=password,  # Recuerda hashear la contraseña
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        telefono_celular=telefono_celular,
        dni=dni,
        fecha_nacimiento=fecha_nacimiento,
        direccion=direccion,
        sueldo=sueldo
    )
    db.session.add(nuevo_empleado)
    db.session.commit()
    return nuevo_empleado


def agregar_usuario_con_sp(username, password, tipo):
    hashed_password = generate_password_hash(password)
    connection = db.engine.raw_connection()
    try:
        cursor = connection.cursor()
        cursor.callproc('agregar_usuario', [username, hashed_password, tipo])
        connection.commit()
    finally:
        cursor.close()
        connection.close()

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        correo = request.form['correo']
        telefono_celular = request.form['telefono_celular']
        dni_ruc = request.form['dni_ruc']
        fecha_nacimiento = request.form['fecha_nacimiento']
        departamento = request.form['departamento']
        provincia = request.form['provincia']
        distrito = request.form['distrito']
        direccion = request.form['direccion']
        username = request.form['username']
        password = request.form['password']
        
        # Usar procedimiento almacenado para agregar el usuario
        agregar_usuario_con_sp(username, password, 'cliente')
        
        # Recuperar el usuario recién creado para obtener su id
        user = Usuario.query.filter_by(usuario=username).first()
        
        if user:
            # Crear nuevo cliente y asociarlo con su propio id
            nuevo_cliente = Cliente(
                id=user.id,  # Asociar el cliente con su propio id
                nombre=nombre,
                apellidos=apellidos,
                correo=correo,
                telefono_celular=telefono_celular,
                dni_ruc=dni_ruc,
                fecha_nacimiento=fecha_nacimiento,
                departamento=departamento,
                provincia=provincia,
                distrito=distrito,
                direccion=direccion,
                username=username
            )
            db.session.add(nuevo_cliente)
            db.session.commit()
            
            flash('Usuario registrado exitosamente.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error al crear el cliente. Usuario no encontrado.', 'error')
    
    return render_template('registro.html')

@app.route('/datos_c')
def datos_c():
    if 'logged_in' in session and session['logged_in'] and session.get('tipo') == 'cliente':
        username = session.get('username')
        cliente = Cliente.query.filter_by(username=username).first()
        if cliente:
            return render_template('datos_c.html', cliente=cliente)
        else:
            flash('No se encontraron datos del cliente.', 'error')
    return redirect(url_for('login'))

@app.route('/contacto')
def contacto():
    if 'logged_in' in session and session['logged_in'] and session['tipo'] == 'cliente':
        return render_template('contacto.html', username=session['username'])
    else:
        flash('Acceso denegado. Debes ser un cliente.', 'error')
        return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)

