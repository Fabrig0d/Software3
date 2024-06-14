from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
import smtplib
import pymysql
import difflib
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
 

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

# Carrito de compra (almacenado en memoria, en una aplicación real podría ser una base de datos)
cart = []

@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', products=productos, cart=session.get('cart', []))

@app.route('/pago')
def pago():
    user_id = session.get('user_id')  # Obtener el ID del usuario de la sesión actual
    if user_id:
        cart_items = CartItem.query.filter_by(user_id=user_id).all()  # Obtener los productos del carrito del usuario
        return render_template('pago.html', cart_items=cart_items)
    else:
        # Manejar el caso donde no hay usuario en la sesión
        return redirect('/login')

@app.route('/carrito')
def carrito():
    cart_items = session.get('cart', [])
    for item in cart_items:
        item['price'] = float(item['price']) if isinstance(item['price'], str) else item['price']
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('carrito.html', cart_items=cart_items, total=total)

@app.route('/update_quantity/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    new_quantity = int(request.form['quantity'])
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] = new_quantity  # Actualizar la cantidad
            session['cart'] = cart
            return redirect(url_for('carrito'))
    return "Producto no encontrado en el carrito"

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form['producto_id'])
    product = Producto.query.get(product_id)
    if product:
        cart = session.get('cart', [])
        # Verificar si el producto ya está en el carrito
        for item in cart:
            if item['id'] == product_id:
                item['quantity'] += 1  # Incrementar la cantidad
                session['cart'] = cart
                return redirect(url_for('mostrar_catalogo'))
        # Si el producto no está en el carrito, agregarlo
        cart_item = {'id': product.id, 'name': product.nombre, 'price': product.precio_pub, 'quantity': 1}
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

@app.route("/pagar")
def pagar():
    return render_template("Pagos_cli.html")

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

def execute_procedure(proc_name, params):
    conn = pymysql.connector.connect(**db_config)
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
    tipos_producto = TipoProducto.query.all()  # Obtener todos los tipos de productos
    return render_template('catalogo_e.html', productos=productos.items, total_pages=total_pages, current_page=page, tipos_producto=tipos_producto)

@app.route('/update_product', methods=['POST'])
def update_product():
    product_id = request.form['id']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    presentacion = request.form['presentacion']
    precio_dis = request.form['precio_dis']
    precio_pub = request.form['precio_pub']
    stock = request.form['stock']
    tipo_producto_id = request.form['tipo_producto_id']
    
    execute_procedure('editar_producto', [product_id, nombre, descripcion, presentacion, precio_dis, precio_pub, stock, tipo_producto_id])
    return jsonify({'success': True})

@app.route('/increase_stock', methods=['POST'])
def increase_stock():
    product_id = request.form['id']
    amount = int(request.form['amount'])
    
    conn = pymysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT stock FROM productos WHERE id = %s", (product_id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if producto:
        nuevo_stock = producto['stock'] + amount
        execute_procedure('editar_producto', [product_id, producto['nombre'], producto['descripcion'], producto['presentacion'], producto['precio_dis'], producto['precio_pub'], nuevo_stock, producto['tipo_producto_id']])
        return jsonify({'success': True})
    return jsonify({'success': False})


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


if __name__ == '__main__':
    app.run(debug=True)

