from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
import smtplib
import mysql.connector
import difflib
from datetime import date
from functools import wraps
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import random
import string
import urllib.parse
from math import ceil
from sqlalchemy import exc, extract, func, or_



# Cargar variables de entorno
env_path = os.path.join(os.path.dirname(__file__), '../ProyectoSoft2/.env')
load_dotenv(env_path)

app = Flask(__name__)

unanswered_questions_count = 0

faq_responses = {
    "horarios": "Nuestros horarios de atención son de lunes a viernes de 9am a 6pm.",
    "contacto": "Puedes contactarnos al correo contacto@asesoria.com o al teléfono 123-456-7890.",
    "servicios": "Ofrecemos servicios de asesoría en línea, soporte técnico y más.",
    "envios": "Los envíos dependen de la distancia y el precio del delivery.",
    "recepcion": "La recepción de productos se realiza en nuestro local principal.",
    "pagos": "Aceptamos pagos en efectivo, tarjeta de crédito y transferencia bancaria.",
    "compras": "Puedes realizar compras directamente desde nuestra tienda en línea."
}

initial_options = ["envios", "recepcion", "pagos", "compras"]

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Configuración de Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'Fabriziovh01@gmail.com'
app.config['MAIL_PASSWORD'] = '925024936fabri'
app.config['MAIL_DEFAULT_SENDER'] = 'Fabriziovh01@gmail.com'

mail = Mail(app)


UPLOAD_FOLDER = '/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuración de la base de datos
password = os.getenv('DB_PASSWORD')
if password is None:
    raise ValueError("La variable de entorno DB_PASSWORD no está definida en el archivo .env")
encoded_password = urllib.parse.quote_plus(password.encode('utf-8'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{encoded_password}@localhost/fitogreen'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'secret_key' : os.getenv('SECRET_KEY'),
}

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20))  # Puede ser 'admin', 'empleado', o 'cliente'

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cli = db.Column(db.Integer, primary_key=True)
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
    rol = db.Column(db.String(100))
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
    nombre = db.Column(db.String(100), unique=True)

class Producto(db.Model):
    __tablename__ = 'productos'
    producto_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(200))
    presentacion = db.Column(db.String(100))
    precio_dis = db.Column(db.Numeric(8, 2))
    precio_pub = db.Column(db.Numeric(8, 2))
    stock = db.Column(db.Integer)
    imagen = db.Column(db.String(500))
    tipo_producto_id = db.Column(db.Integer, db.ForeignKey('tipo_producto.id'))
    tipo_producto = db.relationship('TipoProducto', backref=db.backref('productos', lazy=True))

class Pagos(db.Model):
    __tablename__ = 'Pagos'
    pago_id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cli'))
    fecha_pago = db.Column(db.Date)
    monto = db.Column(db.Numeric(10, 2))
    metodo_pago = db.Column(db.String(50))
    estado = db.Column(db.String(20))

class Pedidos(db.Model):
    __tablename__ = 'Pedidos'
    pedido_id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cli'))
    nombre_cli = db.Column(db.String(100))
    apellido_cli = db.Column(db.String(100))
    direccion_pedido = db.Column(db.String(200))
    fecha_pedido = db.Column(db.Date)
    metodo_pago = db.Column(db.String(45))
    total = db.Column(db.Numeric(10, 2))
    estado = db.Column(db.String(20))
    codigo_orden = db.Column(db.String(100))

class DetallesPedidos(db.Model):
    __tablename__ = 'DetallesPedidos'
    detalle_id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('Pedidos.pedido_id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.producto_id'))
    nombre_cli = db.Column(db.String(100))
    apellido_cli = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    fecha_pedido = db.Column(db.Date)
    cantidad = db.Column(db.Integer)
    metodo_pago = db.Column(db.String(40))
    precio_unitario = db.Column(db.Numeric(10, 2))

    pedido = db.relationship('Pedidos', backref=db.backref('detalles_pedidos', lazy=True))
    producto = db.relationship('Producto', backref=db.backref('detalles_pedidos', lazy=True))

class MensajeContacto(db.Model):
    __tablename__ = 'MensajeContacto'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(100))
    asunto = db.Column(db.String(200))
    mensaje = db.Column(db.Text)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)
    imagen = db.Column(db.String(255))
    estado = db.Column(db.String(20), nullable=False, default='Pendiente')

    def __repr__(self):
        return f"<MensajeContacto {self.id}: {self.nombre} - {self.email}>"

# Carrito de compra (almacenado en memoria, en una aplicación real podría ser una base de datos)
cart = []


@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', products=productos, cart=session.get('cart', []))

@app.route('/carrito')
def carrito():
    cart_items = session.get('cart', [])
    print("Carrito en sesión:", cart_items)  # Verifica qué hay en el carrito

    # Convertir 'price' y 'quantity' a números adecuados
    for item in cart_items:
        item['price'] = float(item['price']) if isinstance(item['price'], str) else item['price']
        item['quantity'] = int(item['quantity']) if isinstance(item['quantity'], str) else item['quantity']
        item['precio_dis'] = float(item.get('precio_dis', 0))

    # Calcular el subtotal considerando la presentación seleccionada y la cantidad de litros
    for item in cart_items:
        if 'presentacion' in item:
            if item['presentacion'] == "12 litros":
                item['subtotal'] = item['precio_dis'] * 12 * item['quantity']
            elif item['presentacion'] == "20 litros":
                item['subtotal'] = item['precio_dis'] * 20 * item['quantity']
            elif item['presentacion'] == "200 litros":
                item['subtotal'] = item['precio_dis'] * 200 * item['quantity']
            else:
                item['subtotal'] = item['price'] * item['quantity']  # Si no es una presentación especial, usar el precio normal
        else:
            item['subtotal'] = item['price'] * item['quantity']  # Si no hay presentación, usar el precio normal

    total = sum(item['subtotal'] for item in cart_items)
    return render_template('carrito.html', cart_items=cart_items, total=total)

@app.route('/update_quantity/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    new_quantity = int(request.form['quantity'])
    cart = session.get('cart', [])
    for item in cart:
        if item['producto_id'] == product_id:
            item['quantity'] = new_quantity  # Actualizar la cantidad
            session['cart'] = cart
            return redirect(url_for('carrito'))
    return "Producto no encontrado en el carrito"

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'producto_id' not in request.form or not request.form['producto_id']:
        return "ID de producto no válido"

    try:
        producto_id = int(request.form['producto_id'])
    except ValueError:
        return "ID de producto no válido"

    product = Producto.query.get(producto_id)
    if product:
        cart = session.get('cart', [])
        # Verificar si el producto ya está en el carrito
        for item in cart:
            if item['producto_id'] == producto_id:
                item['quantity'] += 1  # Incrementar la cantidad
                session['cart'] = cart
                return redirect(url_for('mostrar_catalogo'))

        # Determinar el precio unitario a utilizar
        if product.presentacion in ["12 litros", "20 litros", "200 litros"]:
            precio_unitario = product.precio_dis
        else:
            precio_unitario = product.precio_pub

        # Agregar el producto al carrito
        cart_item = {
            'producto_id': product.producto_id,
            'name': product.nombre,
            'price': str(precio_unitario),  # Convertir a string para consistencia si es necesario
            'quantity': 1,
            'precio_dis': product.precio_dis if product.precio_dis else None,
            'presentacion': product.presentacion
        }
        cart.append(cart_item)
        session['cart'] = cart
        print("Carrito actualizado:", session['cart']) 
        return redirect(url_for('mostrar_catalogo'))
    else:
        return "Producto no encontrado"
    

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['producto_id'] != product_id]
    session['cart'] = cart
    return redirect(url_for('carrito'))

@app.route('/borrar_carrito', methods=['POST'])
def borrar_carrito():
    session.pop('cart', None)
    return redirect(url_for('carrito'))
@app.route('/carrito_rapido', methods=['GET'])
def carrito_rapido():
    cart_items = session.get('cart', [])
    total = sum(item['subtotal'] for item in cart_items)
    return render_template('carrito_rapido.html', cart_items=cart_items, total=total)


@app.route('/pago', methods=['POST'])
def pago():
    username = session.get('username')
    if username:
        try:
            cliente = Cliente.query.filter_by(username=username).first()
            if not cliente:
                flash('Cliente no encontrado.', 'error')
                return redirect(url_for('carrito'))

            cart_items = session.get('cart', [])
            if not cart_items:
                flash('El carrito está vacío.', 'error')
                return redirect(url_for('carrito'))

            # Calcular el total del pedido
            for item in cart_items:
                item['price'] = float(item['price']) if isinstance(item['price'], (int, float, str)) else 0.0
                item['quantity'] = int(item['quantity']) if isinstance(item['quantity'], (int, str)) else 0
                item['precio_dis'] = float(item.get('precio_dis', 0))
                if item['presentacion'] in ["12 litros", "20 litros", "200 litros"]:
                    presentacion_factor = int(item['presentacion'].split()[0])
                    item['price'] = item['precio_dis'] * presentacion_factor
                item['subtotal'] = item['price'] * item['quantity']
            total = sum(item['subtotal'] for item in cart_items)

            # Crear un nuevo pedido
            nuevo_pedido = Pedidos(
                id_cliente=cliente.id_cli,
                nombre_cli=cliente.nombre,
                apellido_cli=cliente.apellidos,
                direccion_pedido=cliente.direccion,
                fecha_pedido=date.today(),
                metodo_pago=request.form['metodo_pago'],
                total=total,
                estado='Pendiente'
            )

            db.session.add(nuevo_pedido)
            db.session.commit()

            pedido_id = nuevo_pedido.pedido_id

            # Agregar detalles del pedido a DetallesPedidos
            for item in cart_items:
                detalle_pedido = DetallesPedidos(
                    pedido_id=pedido_id,
                    producto_id=item['producto_id'],
                    nombre_cli=cliente.nombre,
                    apellido_cli=cliente.apellidos,
                    direccion=cliente.direccion,
                    fecha_pedido=date.today(),
                    cantidad=item['quantity'],
                    metodo_pago=request.form['metodo_pago'],
                    precio_unitario=item['price']
                )
                db.session.add(detalle_pedido)

            db.session.commit()

            # Limpiar el carrito después de completar la compra
            session.pop('cart', None)

            return redirect(url_for('orden_confirmada', pedido_id=pedido_id))

        except exc.SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Error al procesar el pedido: {str(e)}', 'error')
            return redirect(url_for('pagar'))
    else:
        flash('Por favor, inicia sesión para realizar un pedido.', 'error')
        return redirect(url_for('login'))
    

def obtener_detalles_pedido(pedido_id):
    detalles_pedido = DetallesPedidos.query.filter_by(pedido_id=pedido_id).all()
    return detalles_pedido

# Función para generar código de orden de pago aleatorio
def generar_codigo_orden():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Vista para mostrar la orden confirmada
@app.route('/orden_confirmada/<int:pedido_id>')
def orden_confirmada(pedido_id):
    pedido = Pedidos.query.get(pedido_id)
    if pedido:
        detalles_pedido = DetallesPedidos.query.filter_by(pedido_id=pedido_id).all()
        
        # Generar código de orden de pago solo si el método de pago es 'transferencia_bancaria'
        codigo_orden = generar_codigo_orden() if pedido.metodo_pago == 'codigo_orden' else None
        pedido.codigo_orden = codigo_orden  # Asigna el código al pedido
        db.session.commit()  # Guarda en la base de datos
        
        return render_template('orden_confirmada.html', pedido=pedido, detalles_pedido=detalles_pedido, codigo_orden=codigo_orden)
    else:
        flash('Pedido no encontrado.', 'error')
        return redirect(url_for('carrito'))
    
@app.route('/eliminar_producto/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
        return jsonify({'message': 'Producto eliminado correctamente'}), 200
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404


@app.route('/detalles_pedido_e')
def lista_pedidos_e():
    if 'logged_in' in session and session['logged_in']:
        if session.get('tipo') == 'empleado' or session.get('role') == 'admin':
            pedidos = Pedidos.query.all()  # Obtener todos los pedidos
            return render_template('lista_pedidos_e.html', pedidos=pedidos)
        else:
            flash('Debes iniciar sesión como empleado para ver los pedidos.', 'error')
            return redirect(url_for('login'))
    else:
        flash('Debes iniciar sesión para ver los pedidos.', 'error')
        return redirect(url_for('login'))

@app.route('/detalles_pedido_e/<int:pedido_id>')
def detalles_pedido_e(pedido_id):
    if 'logged_in' in session and session['logged_in']:
        if session.get('tipo') == 'empleado'or session.get('role') == 'admin':
             pedido = Pedidos.query.get(pedido_id)
        if pedido:
            return render_template('detalles_pedido_e.html', pedido=pedido)
        else:
            flash('Pedido no encontrado.', 'error')
            return redirect(url_for('lista_pedidos_e'))
    else:
        flash('Debes iniciar sesión como empleado para ver los detalles del pedido.', 'error')
        return redirect(url_for('login'))
    
@app.route('/detalles_pedido_ad/<int:pedido_id>')
def detalles_pedido_ad(pedido_id):
    if 'logged_in' in session and session['logged_in']:
        if session.get('tipo') == 'empleado'or session.get('role') == 'admin':
             pedido = Pedidos.query.get(pedido_id)
        if pedido:
            return render_template('detalles_pedido_ad.html', pedido=pedido)
        else:
            flash('Pedido no encontrado.', 'error')
            return redirect(url_for('lista_pedidos_ad'))
    else:
        flash('Debes iniciar sesión como empleado para ver los detalles del pedido.', 'error')
        return redirect(url_for('login'))


@app.route('/detalles_pedido_ad')
def lista_pedidos_ad():
    if 'logged_in' in session and session['logged_in']:
        if session.get('tipo') == 'empleado' or session.get('role') == 'admin':
            pedidos = Pedidos.query.all()  # Obtener todos los pedidos
            return render_template('lista_pedidos_ad.html', pedidos=pedidos)
        else:
            flash('Debes iniciar sesión como empleado para ver los pedidos.', 'error')
            return redirect(url_for('login'))
    else:
        flash('Debes iniciar sesión para ver los pedidos.', 'error')
        return redirect(url_for('login'))


@app.route('/detalles_pedido')
def lista_pedidos():
    if 'logged_in' in session and session['logged_in'] and session.get('tipo') == 'cliente':
        username = session.get('username')
        cliente = Cliente.query.filter_by(username=username).first()
        if cliente:
            pedidos = Pedidos.query.filter_by(id_cliente=cliente.id_cli).all()
            return render_template('lista_pedidos.html', pedidos=pedidos)
        else:
            flash('No se encontraron datos del cliente.', 'error')
            return redirect(url_for('index'))
    else:
        flash('Debes iniciar sesión para ver tus pedidos.', 'error')
        return redirect(url_for('login'))


@app.route('/cambiar_estado_pedido/<int:pedido_id>', methods=['POST'])
def cambiar_estado_pedido(pedido_id):
    if 'logged_in' in session and session['logged_in']:
        if session.get('tipo') == 'empleado' or session.get('role') == 'admin':
            nuevo_estado = request.form.get('estado')
            pedido = Pedidos.query.get(pedido_id)
            
            if pedido:
                
                # Obtén los detalles del pedido
                detalles_pedido = DetallesPedidos.query.filter_by(pedido_id=pedido_id).all()
                
                # Manejar el cambio de estado a Anulado
                if nuevo_estado == 'Anulado' and pedido.estado != 'Anulado':
                    for detalle in detalles_pedido:
                        producto = Producto.query.get(detalle.producto_id)
                        if producto:
                            producto.stock += detalle.cantidad
                            db.session.add(producto)
                
                # Manejar el cambio desde Anulado a otro estado
                if pedido.estado == 'Anulado' and nuevo_estado != 'Anulado':
                    for detalle in detalles_pedido:
                        producto = Producto.query.get(detalle.producto_id)
                        if producto:
                            producto.stock -= detalle.cantidad
                            db.session.add(producto)
                
                # Actualizar el estado del pedido
                pedido.estado = nuevo_estado
                db.session.commit()
                
                flash('Estado del pedido actualizado correctamente.', 'success')
                return redirect(url_for('detalles_pedido_e', pedido_id=pedido_id))
            else:
                flash('Pedido no encontrado.', 'error')
                return redirect(url_for('lista_pedidos_e'))
        else:
            flash('Debes iniciar sesión como empleado para cambiar el estado del pedido.', 'error')
            return redirect(url_for('login'))
    else:
        flash('Debes iniciar sesión para cambiar el estado del pedido.', 'error')
        return redirect(url_for('login'))


@app.route('/detalles_pedido/<int:pedido_id>')
def detalles_pedido(pedido_id):
    pedido = Pedidos.query.get(pedido_id)
    if pedido:
        detalles_pedido = obtener_detalles_pedido(pedido_id)
        codigo_orden = None
        if pedido.metodo_pago == 'codigo_orden':

            codigo_orden = pedido.codigo_orden if pedido.metodo_pago == 'codigo_orden' else None

        return render_template('detalles_pedido.html', pedido=pedido, detalles_pedido=detalles_pedido, codigo_orden=codigo_orden)
    else:
        flash('Pedido no encontrado.', 'error')
        return redirect(url_for('lista_pedidos'))


@app.route("/pagar", methods=['GET'])
def pagar():
    cart_items = session.get('cart', [])

    for item in cart_items:
        item['price'] = float(item['price']) if isinstance(item['price'], (int, float, str)) else 0.0
        item['quantity'] = int(item['quantity']) if isinstance(item['quantity'], (int, str)) else 0
        item['precio_dis'] = float(item.get('precio_dis', 0))
        if item['presentacion'] in ["12 litros", "20 litros", "200 litros"]:
            presentacion_factor = int(item['presentacion'].split()[0])
            item['price'] = item['precio_dis'] * presentacion_factor
        item['subtotal'] = item['price'] * item['quantity']
    total = sum(float(item['subtotal']) for item in cart_items)
    username = session.get('username')

    # Obtiene los datos del cliente si hay una sesión de usuario activa
    if username:
        cliente = Cliente.query.filter_by(username=username).first()

        if cliente:
            nombre = cliente.nombre
            apellidos = cliente.apellidos
            direccion = cliente.direccion
        else:
            nombre = ''
            apellidos = ''
            direccion = ''
    else:
        nombre = ''
        apellidos = ''
        direccion = ''

    # Actualiza el stock de los productos comprados
    for item in cart_items:
        producto_id = item['producto_id']
        cantidad_comprada = int(item['quantity'])

        # Busca el producto en la base de datos y actualiza el stock
        producto = Producto.query.get(producto_id)
        if producto:
            producto.stock -= cantidad_comprada
            db.session.commit()

    # Renderiza la plantilla de pago con los datos necesarios
    return render_template("Pagar.html", cart_items=cart_items, total=total, nombre=nombre, apellidos=apellidos, direccion=direccion)

@app.route('/cancelar_pedido/<int:pedido_id>', methods=['POST'])
def cancelar_pedido(pedido_id):
    pedido = Pedidos.query.get_or_404(pedido_id)
    
    if pedido.estado == 'Pendiente':
        # Obtén los detalles del pedido
        detalles_pedido = DetallesPedidos.query.filter_by(pedido_id=pedido_id).all()
        
        # Devuelve el stock de los productos
        for detalle in detalles_pedido:
            producto = Producto.query.get(detalle.producto_id)
            if producto:
                producto.stock += detalle.cantidad
                db.session.add(producto)
        
        # Actualiza el estado del pedido
        pedido.estado = 'Cancelado'
        db.session.commit()
    
    return redirect(url_for('detalles_pedido', pedido_id=pedido_id))

def get_pedido_by_id(pedido_id):
    # Implementar esta función para obtener el pedido desde la base de datos
    pass

def save_pedido(pedido):
    # Implementar esta función para guardar el pedido en la base de datos
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Usuario.query.filter_by(usuario=username).first()  
        if user and check_password_hash(user.contrasena, password):
            session['logged_in'] = True
            session['username'] = username
            session['tipo'] = user.tipo  # Almacenar el tipo de usuario en la sesión
            if user.tipo == 'admin':
                session['role'] = 'admin'
            else:
                session['role'] = user.tipo

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

    # Manejo de la imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        # Guardar la imagen en el sistema de archivos
        if imagen.filename != '':
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
    else:
        filename = None

    # Ahora guarda los datos en la base de datos
    nuevo_mensaje = MensajeContacto(nombre=nombre, email=email, asunto=asunto, mensaje=mensaje, imagen=filename)
    db.session.add(nuevo_mensaje)
    db.session.commit()

    flash('¡Tu mensaje ha sido enviado correctamente!')
    return redirect(url_for('home_cliente'))


@app.route('/subir_imagen', methods=['POST'])
def subir_imagen():
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        if imagen.filename != '':
            # Guarda el archivo de manera segura en el directorio UPLOAD_FOLDER
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Aquí deberías guardar 'filename' en tu base de datos

    return 'Imagen subida correctamente'

@app.route('/ver_solicitudes')
def ver_solicitudes():
    mensajes = MensajeContacto.query.all()
    return render_template('ver_solicitudes.html', mensajes=mensajes)

@app.route('/cambiar_estado/<int:mensaje_id>', methods=['POST'])
def cambiar_estado(mensaje_id):
    mensaje = MensajeContacto.query.get_or_404(mensaje_id)
    nuevo_estado = request.form['estado']
    mensaje.estado = nuevo_estado
    db.session.commit()
    return redirect(url_for('ver_solicitudes'))

@app.route('/ver_solicitudes_ad')
def ver_solicitudes_ad():
    mensajes = MensajeContacto.query.all()
    return render_template('ver_solicitudes_ad.html', mensajes=mensajes)

@app.route('/cambiar_estado_ad/<int:mensaje_id>', methods=['POST'])
def cambiar_estado_ad(mensaje_id):
    mensaje = MensajeContacto.query.get_or_404(mensaje_id)
    nuevo_estado = request.form['estado']
    mensaje.estado = nuevo_estado
    db.session.commit()
    return redirect(url_for('ver_solicitudes_ad'))

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
    tipo_producto_id = request.args.get('tipo_producto', type=int)

    if tipo_producto_id:
        productos = Producto.query.filter_by(tipo_producto_id=tipo_producto_id).paginate(page=page, per_page=per_page)
    else:
        productos = Producto.query.paginate(page=page, per_page=per_page)

    total_pages = ceil(productos.total / per_page)
    tipos_productos = TipoProducto.query.all()  # Obtener todos los tipos de productos

    return render_template('catalogo.html', productos=productos.items, total_pages=total_pages, current_page=page, tipos_productos=tipos_productos)

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
    tipos_productos= TipoProducto.query.all()  # Obtener todos los tipos de productos
    return render_template('catalogo_in.html', productos=productos.items, total_pages=total_pages, current_page=page, tipos_producto=tipos_productos)

def execute_procedure(proc_name, params):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.callproc(proc_name, params)
    results = [result.fetchall() for result in cursor.stored_results()]
    conn.commit()
    cursor.close()
    conn.close()
    return results

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
    tipos_productos = TipoProducto.query.all()  # Obtener todos los tipos de productos

    return render_template('catalogo_e.html', productos=productos.items, total_pages=total_pages, current_page=page, tipos_productos=tipos_productos)

@app.route('/inventario')
def catalogo_admin():
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Número de productos por página
    tipo_producto_id = request.args.get('tipo_producto_id', type=int)

    if tipo_producto_id:
        productos = Producto.query.filter_by(tipo_producto_id=tipo_producto_id).paginate(page=page, per_page=per_page)
    else:
        productos = Producto.query.paginate(page=page, per_page=per_page)

    total_pages = ceil(productos.total / per_page)
    tipos_productos = TipoProducto.query.all()  # Obtener todos los tipos de productos

    return render_template('inventario.html', productos=productos.items, total_pages=total_pages, current_page=page, tipos_productos=tipos_productos)

@app.route('/update_product', methods=['POST'])
def update_product():
    try:
        data = request.form
        producto_id = data.get('id')  # Asegúrate de obtener el 'id' del formulario
        producto = Producto.query.get(producto_id)

        tipo_producto_id = data.get('tipo_producto_id', type=int)

        if producto:
            producto.nombre = data['nombre']
            producto.descripcion = data['descripcion']
            producto.presentacion = data['presentacion']
            producto.precio_dis = data['precio_dis']
            producto.precio_pub = data['precio_pub']
            producto.stock = data['stock']
            producto.tipo_producto_id = tipo_producto_id  # Usar el tipo_producto_id correcto

            db.session.commit()
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="Producto no encontrado")
    except Exception as e:
        print(f"Error al actualizar el producto: {e}")
        return jsonify(success=False, error=str(e)), 500

@app.route('/increase_stock', methods=['POST'])
def increase_stock():
    data = request.form
    producto = Producto.query.get(data['id'])
    if producto:
        producto.stock += int(data['amount'])
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and session['logged_in'] and session['tipo'] == 'admin':
            return f(*args, **kwargs)
        else:
            flash('Acceso denegado. Debes ser un administrador.', 'error')
            return redirect(url_for('login'))
    return decorated_function

def agregar_usuario_con_sp(username, hashed_password, tipo, **kwargs):
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
        
        hashed_password = generate_password_hash(password)

        # Usar procedimiento almacenado para agregar el usuario
        agregar_usuario_con_sp(username, hashed_password, 'cliente')

        # Recuperar el usuario recién creado para obtener su id
        user = Usuario.query.filter_by(usuario=username).first()
        
        if user:
            # Crear nuevo cliente y asociarlo con su propio id
            nuevo_cliente = Cliente(
                id_cli=user.id,  # Asociar el cliente con su propio id
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


@app.route('/datos_e', methods=['GET', 'POST'])
def datos_e():
    if 'logged_in' in session and session['logged_in'] and session.get('tipo') == 'empleado':
        username = session.get('username')
        empleado = Empleado.query.filter_by(username=username).first()
        if empleado:
            if request.method == 'POST':
                # Obtener los datos actualizados del formulario
                empleado.nombre = request.form['nombre']
                empleado.apellidos = request.form['apellidos']
                empleado.correo = request.form['correo']
                empleado.telefono_celular = request.form['telefono_celular']
                empleado.dni = request.form['dni_ruc']  # Se usa 'dni' en lugar de 'dni_ruc'
                empleado.fecha_nacimiento = request.form['fecha_nacimiento']
                empleado.direccion = request.form['direccion']
                # Guardar los cambios en la base de datos
                db.session.commit()
                flash('Datos actualizados correctamente.', 'success')
                return redirect(url_for('datos_e'))
            else:
                return render_template('datos_e.html', empleado=empleado)
        else:
            flash('No se encontraron datos del empleado.', 'error')
    return redirect(url_for('login'))


@app.route('/datos_c', methods=['GET', 'POST'])
def datos_c():
    if 'logged_in' in session and session['logged_in'] and session.get('tipo') == 'cliente':
        username = session.get('username')
        cliente = Cliente.query.filter_by(username=username).first()
        if cliente:
            if request.method == 'POST':
                # Obtener los datos actualizados del formulario
                cliente.nombre = request.form['nombre']
                cliente.apellidos = request.form['apellidos']
                cliente.correo = request.form['correo']
                cliente.telefono_celular = request.form['telefono_celular']
                cliente.dni_ruc = request.form['dni_ruc']
                cliente.fecha_nacimiento = request.form['fecha_nacimiento']
                cliente.departamento = request.form['departamento']
                cliente.provincia = request.form['provincia']
                cliente.distrito = request.form['distrito']
                cliente.direccion = request.form['direccion']
                # Guardar los cambios en la base de datos
                db.session.commit()
                flash('Datos actualizados correctamente.', 'success')
                return redirect(url_for('datos_c'))
            else:
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
        
        
@app.route('/actualizar_datos', methods=['GET'])
def mostrar_formulario_actualizar_datos():
    if 'logged_in' in session and session['logged_in'] and session.get('tipo') == 'cliente':
        username = session.get('username')
        cliente = Cliente.query.filter_by(username=username).first()
        if cliente:
            return render_template('actualizar_datos.html', cliente=cliente)
        else:
            flash('No se encontraron datos del cliente.', 'error')
            return redirect(url_for('datos_c'))  # Redirigir al usuario de vuelta a la página de datos del cliente si no se encuentran datos
    return redirect(url_for('login'))
    
@app.route('/actualizar_datos', methods=['POST'])
def actualizar_datos():
    if 'logged_in' in session and session['logged_in'] and session.get('tipo') == 'cliente':
        username = session.get('username')
        cliente = Cliente.query.filter_by(username=username).first()
        if cliente:
            # Actualizar los datos del cliente con los valores enviados desde el formulario
            cliente.nombre = request.form['nombre']
            cliente.apellidos = request.form['apellidos']
            cliente.correo = request.form['correo']
            cliente.telefono_celular = request.form['telefono_celular']
            cliente.dni_ruc = request.form['dni_ruc']
            cliente.fecha_nacimiento = request.form['fecha_nacimiento']
            cliente.departamento = request.form['departamento']
            cliente.provincia = request.form['provincia']
            cliente.distrito = request.form['distrito']
            cliente.direccion = request.form['direccion']
            
            # Guardar los cambios en la base de datos
            db.session.commit()
            flash('Datos actualizados correctamente.', 'success')
            return redirect(url_for('home_cliente'))
        else:
            flash('No se encontraron datos del cliente.', 'error')
    return redirect(url_for('login'))

@app.route('/chat')
def chat():
    return render_template('chat.html', initial_options=initial_options)

@app.route('/get_response', methods=['POST'])
def get_response():
    global unanswered_questions_count
    user_message = request.form['message'].lower()
    
    # Verificar si la pregunta del usuario coincide con alguna pregunta frecuente
    matched_question = get_best_match(user_message, list(faq_responses.keys()))

    if matched_question:
        response = faq_responses[matched_question]
        unanswered_questions_count = 0
    else:
        response = "Lo siento, no entiendo tu pregunta. Un asesor se pondrá en contacto contigo."
        unanswered_questions_count += 1
        if unanswered_questions_count >= 1:
            response += " Un asesor se pondrá en contacto contigo."
            # Aquí podrías implementar la lógica para notificar a un asesor

    return jsonify({"response": response})

def get_best_match(question, options):
    # Calcular la mejor coincidencia entre la pregunta del usuario y las opciones disponibles
    match = difflib.get_close_matches(question, options, n=1, cutoff=0.5)
    return match[0] if match else None

@app.route('/ad_usuarios')
def ad_usuarios():
    clientes = Cliente.query.all()
    empleados = Empleado.query.all()
    administradores = Administrador.query.all()
    return render_template('ad_usuarios.html', clientes=clientes, empleados=empleados, administradores=administradores)

@app.route('/registro_cliente', methods=['GET', 'POST'])
def registro_cliente():
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
        
        hashed_password = generate_password_hash(password)

        # Usar procedimiento almacenado para agregar el usuario
        agregar_usuario_con_sp(username, hashed_password, 'cliente')

        # Recuperar el usuario recién creado para obtener su id
        user = Usuario.query.filter_by(usuario=username).first()
            
        if user:
            # Crear nuevo cliente y asociarlo con su propio id
            nuevo_cliente = Cliente(
                id_cli=user.id,  # Asociar el cliente con su propio id
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
    
    return render_template('registro_cliente.html')



@app.route('/registro_empleado', methods=['GET', 'POST'])
def registro_empleado():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        correo = request.form['correo']
        telefono_celular = request.form['telefono_celular']
        dni = request.form['dni']
        fecha_nacimiento = request.form['fecha_nacimiento']
        direccion = request.form['direccion']
        sueldo = request.form['sueldo']
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)
        
        # Usar procedimiento almacenado para agregar el usuario
        agregar_usuario_con_sp(username, hashed_password, 'empleado')

        # Recuperar el usuario recién creado para obtener su id
        user = Usuario.query.filter_by(usuario=username).first()
        
        if user:
            # Crear nuevo empleado y asociarlo con su propio id
            nuevo_empleado = Empleado(
                id=user.id,  # Asociar el empleado con su propio id
                nombre=nombre,
                apellidos=apellidos,
                correo=correo,
                telefono_celular=telefono_celular,
                dni=dni,
                fecha_nacimiento=fecha_nacimiento,
                direccion=direccion,
                sueldo=sueldo,
                username=username
            )
            db.session.add(nuevo_empleado)
            db.session.commit()
            
            flash('Empleado registrado exitosamente.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error al crear el empleado. Usuario no encontrado.', 'error')
    
    return render_template('registro_empleado.html')


@app.route('/registro_administrador', methods=['GET', 'POST'])
def registro_administrador():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        correo = request.form['correo']
        telefono_celular = request.form['telefono_celular']
        dni = request.form['dni']
        fecha_nacimiento = request.form['fecha_nacimiento']
        direccion = request.form['direccion']
        sueldo = request.form['sueldo']
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)
        
        # Usar procedimiento almacenado para agregar el usuario
        agregar_usuario_con_sp(username, hashed_password, 'admin')

        # Recuperar el usuario recién creado para obtener su id
        user = Usuario.query.filter_by(usuario=username).first()
        
        if user:
            # Crear nuevo administrador y asociarlo con su propio id
            nuevo_administrador = Administrador(
                id=user.id,  # Asociar el administrador con su propio id
                nombre=nombre,
                apellidos=apellidos,
                correo=correo,
                telefono_celular=telefono_celular,
                dni=dni,
                fecha_nacimiento=fecha_nacimiento,
                direccion=direccion,
                sueldo=sueldo,
                username=username
            )
            db.session.add(nuevo_administrador)
            db.session.commit()
            
            flash('Administrador registrado exitosamente.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error al crear el administrador. Usuario no encontrado.', 'error')
    
    return render_template('registro_administrador.html')


@app.route('/reporte')
def reporte():
    year = request.args.get('year')
    month = request.args.get('month')

    if not year or not month:
        # Si year o month no están presentes, renderizamos una página sin datos
        return render_template('reporte.html', pedidos=[], total_ventas=0)

    # Convertimos year y month a enteros para usarlos en la consulta
    try:
        year = int(year)
        month = int(month)
    except ValueError:
        flash('Año o mes inválidos. Por favor, selecciona valores correctos.')
        return redirect(url_for('reporte'))

    # Query para obtener los pedidos del año y mes seleccionados
    pedidos = db.session.query(Pedidos).filter(
        extract('year', Pedidos.fecha_pedido) == year,
        extract('month', Pedidos.fecha_pedido) == month
    ).all()

    total_ventas = sum(pedido.total for pedido in pedidos)

    return render_template('reporte.html', pedidos=pedidos, total_ventas=total_ventas)

@app.route('/reporte_ad')
def reporte_ad():
    year = request.args.get('year')
    month = request.args.get('month')

    if not year or not month:
        # Si year o month no están presentes, renderizamos una página sin datos
        return render_template('reporte_ad.html', pedidos=[], total_ventas=0)

    # Convertimos year y month a enteros para usarlos en la consulta
    try:
        year = int(year)
        month = int(month)
    except ValueError:
        flash('Año o mes inválidos. Por favor, selecciona valores correctos.')
        return redirect(url_for('reporte'))

    # Query para obtener los pedidos del año y mes seleccionados
    pedidos = db.session.query(Pedidos).filter(
        extract('year', Pedidos.fecha_pedido) == year,
        extract('month', Pedidos.fecha_pedido) == month
    ).all()

    total_ventas = sum(pedido.total for pedido in pedidos)

    return render_template('reporte_ad.html', pedidos=pedidos, total_ventas=total_ventas)


sugerencias_estaticas = ['Alga sheer', 'Fito alga', 'Otra sugerencia']

@app.route('/api/sugerencias')
def sugerencias():
    query = request.args.get('q', '')
    sugerencias_filtradas = [s for s in sugerencias_estaticas if query.lower() in s.lower()]
    return jsonify(sugerencias_filtradas)

# Función de ejemplo para obtener sugerencias (debes adaptarla según tu modelo de datos)
def obtener_sugerencias(query):
    # Ejemplo simple: retornar algunas sugerencias estáticas
    sugerencias = ['Alga sheer', 'Fito alga', 'Otra sugerencia']
    # Aquí podrías consultar tu base de datos u otro origen de datos para obtener sugerencias dinámicas
    return sugerencias

@app.route('/buscar_productos')
def buscar_productos():
    # Obtener los parámetros de búsqueda desde la solicitud GET
    query = request.args.get('q', '')
    tipo_producto_id = request.args.get('tipo_producto', '')
    precio = request.args.get('precio', '')
    presentacion = request.args.get('presentacion', '')

    # Convertir tipo_producto_id a entero si es válido
    try:
        tipo_producto_id = int(tipo_producto_id)
    except ValueError:
        tipo_producto_id = None

    # Consulta para obtener todos los tipos de productos disponibles
    tipos_productos = TipoProducto.query.all()

    # Comenzar la consulta filtrando por nombre y descripción que contengan el término de búsqueda
    productos_query = Producto.query.filter(or_(
        Producto.nombre.ilike(f'%{query}%'),
        Producto.descripcion.ilike(f'%{query}%')
    ))

    # Filtrar por tipo de producto si se proporciona
    if tipo_producto_id:
        # Verificar si el tipo_producto_id proporcionado existe en la base de datos
        tipo_producto_existente = TipoProducto.query.get(tipo_producto_id)
        if tipo_producto_existente:
            productos_query = productos_query.filter_by(tipo_producto_id=tipo_producto_id)
        else:
            # Manejar el caso donde el tipo_producto_id no existe
            return render_template('error.html', mensaje="El tipo de producto especificado no existe."), 404

    # Filtrar por precio si se especifica 'menor' o 'mayor'
    if precio == 'menor':
        productos_query = productos_query.order_by(Producto.precio_pub.asc())
    elif precio == 'mayor':
        productos_query = productos_query.order_by(Producto.precio_pub.desc())

    # Filtrar por presentación si se especifica
    if presentacion:
        productos_query = productos_query.filter(Producto.presentacion.ilike(f'%{presentacion}%'))

    # Obtener los resultados finales
    productos = productos_query.all()

    # Renderizar el template de resultados de búsqueda con los productos encontrados
    return render_template('resultados_busqueda.html', productos=productos, tipos_productos=tipos_productos)
    

@app.route('/buscar_productos_e')
def buscar_productos_e():
    # Obtener los parámetros de búsqueda desde la solicitud GET
    query = request.args.get('q', '')
    tipo_producto_id = request.args.get('tipo_producto', '')
    precio = request.args.get('precio', '')
    presentacion = request.args.get('presentacion', '')

    # Consulta para obtener todos los tipos de productos disponibles
    tipos_productos = TipoProducto.query.all()

    # Comenzar la consulta filtrando por nombre y descripción que contengan el término de búsqueda
    productos_query = Producto.query.filter(or_(
        Producto.nombre.ilike(f'%{query}%'),
        Producto.descripcion.ilike(f'%{query}%')
    ))

    # Filtrar por tipo de producto si se proporciona
    if tipo_producto_id:
        productos_query = productos_query.filter_by(tipo_producto_id=tipo_producto_id)

    # Ordenar por precio si se especifica 'mayor' o 'menor'
    if precio == 'mayor':
        productos_query = productos_query.order_by(Producto.precio_pub.desc())
    elif precio == 'menor':
        productos_query = productos_query.order_by(Producto.precio_pub.asc())

    # Filtrar por presentación si se especifica
    if presentacion:
        productos_query = productos_query.filter(Producto.presentacion.ilike(f'%{presentacion}%'))

    # Obtener los resultados finales
    productos = productos_query.all()

    # Renderizar el template de resultados de búsqueda con los productos encontrados
    return render_template('resultados_busqueda_e.html', productos=productos, tipos_productos=tipos_productos)

@app.route('/buscar_productos_ad')
def buscar_productos_ad():
    # Obtener los parámetros de búsqueda desde la solicitud GET
    query = request.args.get('q', '')
    tipo_producto_id = request.args.get('tipo_producto', '')
    precio = request.args.get('precio', '')
    presentacion = request.args.get('presentacion', '')

    # Consulta para obtener todos los tipos de productos disponibles
    tipos_productos = TipoProducto.query.all()

    # Comenzar la consulta filtrando por nombre y descripción que contengan el término de búsqueda
    productos_query = Producto.query.filter(or_(
        Producto.nombre.ilike(f'%{query}%'),
        Producto.descripcion.ilike(f'%{query}%')
    ))

    # Filtrar por tipo de producto si se proporciona
    if tipo_producto_id:
        productos_query = productos_query.filter_by(tipo_producto_id=tipo_producto_id)

    # Ordenar por precio si se especifica 'mayor' o 'menor'
    if precio == 'mayor':
        productos_query = productos_query.order_by(Producto.precio_pub.desc())
    elif precio == 'menor':
        productos_query = productos_query.order_by(Producto.precio_pub.asc())

    # Filtrar por presentación si se especifica
    if presentacion:
        productos_query = productos_query.filter(Producto.presentacion.ilike(f'%{presentacion}%'))

    # Obtener los resultados finales
    productos = productos_query.all()

    # Renderizar el template de resultados de búsqueda con los productos encontrados
    return render_template('resultados_busqueda_ad.html', productos=productos, tipos_productos=tipos_productos)

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'GET':
        tipos_productos = TipoProducto.query.all()
        return render_template('agregar_producto.html', tipos_productos=tipos_productos)
    elif request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        presentacion = request.form['presentacion']
        precio_dis = request.form['precio_dis']
        precio_pub = request.form['precio_pub']
        stock = request.form['stock']
        tipo_producto_id = request.form['tipo_producto']
        
        nuevo_producto = Producto(nombre=nombre, descripcion=descripcion, presentacion=presentacion,
                                  precio_dis=precio_dis, precio_pub=precio_pub, stock=stock,
                                  tipo_producto_id=tipo_producto_id)
        
        db.session.add(nuevo_producto)
        db.session.commit()
        
        return redirect(url_for('catalogo_empleado'))
    
@app.route('/agregar_producto_ad', methods=['GET', 'POST'])
def agregar_producto_ad():
    if request.method == 'GET':
        tipos_productos = TipoProducto.query.all()
        return render_template('agregar_producto_ad.html', tipos_productos=tipos_productos)
    elif request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        presentacion = request.form['presentacion']
        precio_dis = request.form['precio_dis']
        precio_pub = request.form['precio_pub']
        stock = request.form['stock']
        tipo_producto_id = request.form['tipo_producto']
        
        nuevo_producto = Producto(nombre=nombre, descripcion=descripcion, presentacion=presentacion,
                                  precio_dis=precio_dis, precio_pub=precio_pub, stock=stock,
                                  tipo_producto_id=tipo_producto_id)
        
        db.session.add(nuevo_producto)
        db.session.commit()
        
        return redirect(url_for('catalogo_admin'))



@app.route('/editar', methods=['POST'])
def editar():
    print(f"Datos recibidos: {request.form}")

    id = request.form.get('id_cli')
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    apellidos = request.form.get('apellidos')
    correo = request.form.get('correo')
    telefono_celular = request.form.get('telefono')
    dni_ruc = request.form.get('dni_ruc')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    direccion = request.form.get('direccion')
    username = request.form.get('username')
    sueldo = request.form.get('sueldo')
    table_type = request.form.get('table_type')


    print(f"ID recibido: {id}")
    print(f"Tipo de tabla: {table_type}")

    if table_type == 'cliente':
        cliente = Cliente.query.get(id)
        if cliente:
            cliente.nombre = nombre if nombre is not None else cliente.nombre
            cliente.apellidos = apellidos if apellidos is not None else cliente.apellidos
            cliente.correo = correo if correo is not None else cliente.correo
            cliente.telefono_celular = telefono_celular if telefono_celular is not None else cliente.telefono_celular
            cliente.dni_ruc = dni_ruc if dni_ruc is not None else cliente.dni_ruc
            cliente.fecha_nacimiento = fecha_nacimiento if fecha_nacimiento is not None else cliente.fecha_nacimiento
            cliente.direccion = direccion if direccion is not None else cliente.direccion
            cliente.username = username if username is not None else cliente.username
            db.session.commit()
            print(f"Cliente actualizado: {cliente.id_cli}, {cliente.nombre} {cliente.apellidos}")

    elif table_type == 'empleado':
        empleado = Empleado.query.get(id)
        if empleado:
            empleado.nombre = nombre if nombre is not None else empleado.nombre
            empleado.apellidos = apellidos if apellidos is not None else empleado.apellidos
            empleado.correo = correo if correo is not None else empleado.correo
            empleado.telefono_celular = telefono_celular if telefono_celular is not None else empleado.telefono_celular
            empleado.dni = dni_ruc if dni_ruc is not None else empleado.dni
            empleado.fecha_nacimiento = fecha_nacimiento if fecha_nacimiento is not None else empleado.fecha_nacimiento
            empleado.direccion = direccion if direccion is not None else empleado.direccion
            empleado.sueldo = sueldo if sueldo is not None else empleado.sueldo
            db.session.commit()
            print(f"Empleado actualizado: {empleado.id}, {empleado.nombre} {empleado.apellidos}")

    elif table_type == 'administrador':
        administrador = Administrador.query.get(id)
        if administrador:
            administrador.nombre = nombre if nombre is not None else administrador.nombre
            administrador.apellidos = apellidos if apellidos is not None else administrador.apellidos
            administrador.correo = correo if correo is not None else administrador.correo
            administrador.telefono_celular = telefono_celular if telefono_celular is not None else administrador.telefono_celular
            administrador.dni = dni_ruc if dni_ruc is not None else administrador.dni
            administrador.fecha_nacimiento = fecha_nacimiento if fecha_nacimiento is not None else administrador.fecha_nacimiento
            administrador.direccion = direccion if direccion is not None else administrador.direccion
            administrador.sueldo = sueldo if sueldo is not None else administrador.sueldo
            db.session.commit()
            print(f"Administrador actualizado: {administrador.id}, {administrador.nombre} {administrador.apellidos}")

    return jsonify({'success': True})

# Ruta para eliminar un cliente
@app.route('/eliminar_cliente/<int:id_cli>', methods=['POST'])
def eliminar_cliente(id_cli):
    cliente = Cliente.query.get_or_404(id_cli)
    try:
        # Cambiar el estado del cliente a inactivo (estado=0)
        cliente.id_cli = 0
        db.session.commit()
        return jsonify({'success': True, 'message': 'Cliente cambiado a inactivo correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# Ruta para eliminar un empleado
@app.route('/eliminar_empleado/<int:id>', methods=['POST'])
def eliminar_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    try:
        # Cambiar el estado del empleado a inactivo (estado=0)
        empleado.id = 0
        db.session.commit()
        return jsonify({'success': True, 'message': 'Empleado cambiado a inactivo correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# Ruta para eliminar un administrador
@app.route('/eliminar_administrador/<int:id>', methods=['POST'])
def eliminar_administrador(id):
    administrador = Administrador.query.get_or_404(id)
    try:
        # Cambiar el estado del administrador a inactivo (estado=0)
        administrador.id = 0
        db.session.commit()
        return jsonify({'success': True, 'message': 'Administrador cambiado a inactivo correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})
if __name__ == '__main__':
    app.run(debug=True)

