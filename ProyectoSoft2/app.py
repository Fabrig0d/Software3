from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector 

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Se usa para manejar sesiones y cookies.

# Datos de prueba con un atributo para el tipo de usuario
usuarios = {
    "cliente1": {"password": "psw1", "role": "cliente"},
    "empleado1": {"password": "psw2", "role": "empleado"},
}

products = [
    {"id": 1, "name": "Producto 1", "price": 10},
    {"id": 2, "name": "Producto 2", "price": 20},
    {"id": 3, "name": "Producto 3", "price": 30},
]

# Carrito de compra (almacenado en memoria, en una aplicación real podría ser una base de datos)
cart = []

 #Index Visita
@app.route('/')
def index():
    return render_template('index.html', products=products, cart=cart)

 #Carrito add/rm
@app.route('/carrito')
def carrito():
    if 'cart' in session:
        cart_items = session['cart']
    else:
        cart_items = []
    return render_template('carrito.html', cart_items=cart_items)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form['producto_id'])
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart_item = {'id': product['id'], 'name': product['name'], 'price': product['price'], 'quantity': 1}  
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append(cart_item)
        return redirect(url_for('mostrar_catalogo'))
    else:
        return "Producto no encontrado"

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    global cart
    cart = [item for item in cart if item['id'] != product_id]
    return redirect(url_for('carrito'))

@app.route('/borrar_carrito', methods=['POST'])
def borrar_carrito():
    session.pop('carrito', None)
    return redirect(url_for('carrito'))

@app.route('/pagar', methods=['POST'])
def pagar():
    # Aquí puedes agregar la lógica para procesar el pago
    return '¡Gracias por su compra!'


#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in usuarios and usuarios[username]["password"] == password:
            session['logged_in'] = True
            session['username'] = username
            session['role'] = usuarios[username]["role"]
            

            # Redirigir según el tipo de usuario
            if session['role'] == 'cliente':
                return redirect(url_for('home_cliente'))
            elif session['role'] == 'empleado':
                return redirect(url_for('home_empleado'))
        else:
            flash('Usuario o contraseña incorrectos.', 'error')

    return render_template('login.html')


@app.route('/home_cliente')
def home_cliente():
    if 'logged_in' in session and session['logged_in'] and session['role'] == 'cliente':
        return render_template('home_cliente.html', username=session['username'])
    else:
        flash('Acceso denegado. Debes ser un cliente.', 'error')
        return redirect(url_for('login'))


@app.route('/home_empleado')
def home_empleado():
    if 'logged_in' in session and session['logged_in'] and session['role'] == 'empleado':
        return render_template('home_empleado.html', username=session['username'])
    else:
        flash('Acceso denegado. Debes ser un empleado.', 'error')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

 
# Modifica la función mostrar_catalogo para obtener los productos de la base de datos
@app.route('/catalogo')
def mostrar_catalogo():
    # Conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="925024936F@b.", #pon tu contra :v
        port = "3305", #Cambia el port segun el tuyo (default 3306)
        database="fitogreen"
    )

    # Crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # Consulta para obtener los productos desde la base de datos
    query = "SELECT * FROM productos"

    # Ejecutar la consulta
    cursor.execute(query)

    # Obtener todos los productos
    productos = cursor.fetchall()

    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    conn.close()

    # Renderiza la plantilla y pasa los productos
    return render_template('catalogo.html', productos=productos) 

@app.route('/catalogo_e')
def catalogo_empleado():
    # Conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="", #pon tu contra :v
        port = "3306", #Cambia el port segun el tuyo (default 3306)
        database="fitogreen"
    )

    # Crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # Consulta para obtener los productos desde la base de datos
    query = "SELECT * FROM productos"

    # Ejecutar la consulta
    cursor.execute(query)

    # Obtener todos los productos
    productos = cursor.fetchall()

    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    conn.close()

    # Renderiza la plantilla y pasa los productos
    return render_template('catalogo_e.html', productos=productos) 



if __name__ == '__main__':
    app.run(debug=True)


 