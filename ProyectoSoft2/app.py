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
