from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'gustavo'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def listar_productos():
    productos = session.get('productos', [])
    return render_template('listar_productos.html', productos=productos)

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        id_producto = request.form['id']
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']

        
        nuevo_producto = {
            'id': id_producto,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }

        productos = session.get('productos', [])

        
        if any(prod['id'] == id_producto for prod in productos):
            return "Error: ID de producto ya existe", 400

       
        productos.append(nuevo_producto)

     
        session['productos'] = productos

        return redirect(url_for('listar_productos'))

    return render_template('agregar_producto.html')

@app.route('/editar_producto/<id>', methods=['GET', 'POST'])
def editar_producto(id):
    
    productos = session.get('productos', [])
    producto_a_editar = next((prod for prod in productos if prod['id'] == id), None)

    if request.method == 'POST':

        producto_a_editar['nombre'] = request.form['nombre']
        producto_a_editar['cantidad'] = int(request.form['cantidad'])
        producto_a_editar['precio'] = float(request.form['precio'])
        producto_a_editar['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto_a_editar['categoria'] = request.form['categoria']

        session['productos'] = productos
        return redirect(url_for('listar_productos'))

    return render_template('editar_producto.html', producto=producto_a_editar)

@app.route('/eliminar_producto/<id>', methods=['POST'])
def eliminar_producto(id):
    productos = session.get('productos', [])

    productos = [prod for prod in productos if prod['id'] != id]


    session['productos'] = productos

    return redirect(url_for('listar_productos'))

if __name__ == '__main__':
    app.run(debug=True)