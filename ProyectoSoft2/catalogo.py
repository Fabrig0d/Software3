from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenido a tu catálogo"

if __name__ == '__main__':
    app.run(debug=True)

catalogo = [
    {"nombre": "Producto 1", "descripcion": "Descripción del producto 1", "precio": 100},
    {"nombre": "Producto 2", "descripcion": "Descripción del producto 2", "precio": 200},
]

@app.route('/catalogo')
def mostrar_catalogo():
    # Renderiza una plantilla para mostrar el catálogo
    return render_template('catalogo.html', catalogo=catalogo)