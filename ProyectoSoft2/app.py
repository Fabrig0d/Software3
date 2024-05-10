from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Se usa para manejar sesiones y cookies.

# Datos de prueba con un atributo para el tipo de usuario
usuarios = {
    "cliente1": {"password": "psw1", "role": "cliente"},
    "empleado1": {"password": "psw2", "role": "empleado"},
}

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


# Ejemplo de una función para mostrar el catálogo
@app.route('/catalogo')
def mostrar_catalogo():
    catalogo = [
        {"nombre": "Producto 1", "descripcion": "Descripción del producto 1", "precio": 10.99},
        {"nombre": "Producto 2", "descripcion": "Descripción del producto 2", "precio": 20.49},
 
    ]
    # Renderiza la plantilla y pasa el catálogo
    return render_template('catalogo.html', catalogo=catalogo)

if __name__ == '__main__':
    app.run(debug=True)


 
"""# Modifica la función mostrar_catalogo para obtener los productos de la base de datos
@app.route('/catalogo')
def mostrar_catalogo():
    # Conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
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
    
    #HTML catalogo html
    <div class="col-md-9"> <!-- Amplié el tamaño del contenido del catálogo a 9 de 12 columnas -->
    <div class="row">
        {% for producto in productos %}
        <div class="col-md-4">
            <div class="card my-2">
                <div class="card-body">
                    <h5 class="card-title">{{ producto[1] }}</h5> <!-- Nombre del producto -->
                    <p class="card-text">{{ producto[2] }}</p> <!-- Descripción del producto -->
                    <p class="card-text">Precio: ${{ producto[3] }}</p> <!-- Precio del producto -->
                </div>
            </div>
        </div>
        {% endfor %}"""
 