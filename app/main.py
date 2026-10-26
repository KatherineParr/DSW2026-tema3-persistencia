from flask import Flask, redirect, render_template, url_for
from app.models import db, Producto
from app.forms import ProductoForm
##importar base de datos, con el nombre de variable de la base de datos
#y el nombre de la tabla (clase)

app = Flask(__name__)
#para añadir formularios hay que añadir una contraseña
app.config["SECRET_KEY"] = "contraseña"

#configuracion de la base de datos (en local = sqlite)
#siempre es asi al usar sqlite, y despuesde las tres / se pone el nombre de la base
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tienda.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #si se modifican los datos
##que salga una noti si algo ta bien o no y otras advertencias

#vinculamos alchemy con nuestr aappp de flask
db.init_app(app)

with app.app_context():
    #crea las tablas en la base si no existieran
    db.create_all()
    print("<<<<<<<<<<<<<<<<<<")

    producto = Producto.query.first()
    print("Producto encontrado:", producto)

    if not Producto.query.first(): #si no hay un primer objeto, crea uno
        nuevo_producto = Producto(nombre="Teclado Mecanico RGB", precio=49.99)
        #y disponible esta por defecto true
        #ahora para añadirlo a la tabla
        print("prueba")
        db.session.add(nuevo_producto)
        db.session.commit()
        print(">>>> Producto de prueba insertadoe n la base de datos <<<<<")


@app.route("/")
def hello():
    return redirect(url_for("mostrar_catalogo"))

# 1. READ: Mostrar todos los productos en la plantilla catalogo.html
@app.route("/catalogo")
def mostrar_catalogo():
    productos = Producto.query.all()
    return render_template("catalogo.html", lista_productos=productos)

#para hacer el CRUD

@app.route("/producto/nuevo", methods=["GET", "POST"])
def crear_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nuevo_producto = Producto(
            nombre = form.nombre.data,
            precio = form.precio.data,
            disponible = form.disponible.data,
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        #patron prg: redirigir despues de procesar
        return redirect(url_for("mostrar_catalogo"))

# 3. UPDATE: Recuperar un producto existente, rellenar el formulario y guardar cambios
@app.route("/producto/<int:prod_id>/editar", methods=["GET", "POST"])
def editar_producto(prod_id):
    # Busca el producto por su clave primaria o lanza un error 404 si no existe
    producto = db.get_or_404(Producto, prod_id)

    # Al pasar obj=producto, en la petición GET los campos aparecen ya rellenos con los datos actuales
    form = ProductoForm(obj=producto)

    if form.validate_on_submit():
        # Modificamos directamente los atributos del objeto recuperado de la BD
        producto.nombre = form.nombre.data
        producto.precio = form.precio.data
        producto.disponible = form.disponible.data

        # Confirmamos los cambios en la BD
        db.session.commit()
        return redirect(url_for("mostrar_catalogo"))

    return render_template("producto_form.html", form=form, titulo="Editar Producto")

# 4. DELETE: Eliminar un producto de la BD (exclusivamente por POST)
@app.route("/producto/<int:prod_id>/eliminar", methods=["POST"])
def eliminar_producto(prod_id):
    producto = db.get_or_404(Producto, prod_id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for("mostrar_catalogo"))


""" @app.route("/test.db")
def test_db():
    productos = Producto.query.all()
    return f"Todos los productos: {productos}" """




if __name__ == "__main__":
    app.run(debug=True)
