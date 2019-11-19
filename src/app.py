from flask import Flask, render_template, redirect, url_for, request, session, escape, make_response, abort
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from forms import FormProducto, LoginForm, FormCliente, FormChangePassword, FormCarrito
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import config
import json
from datetime import datetime as dt
from sqlalchemy import desc
import googlemaps

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route('/')
def Index():
    return render_template('index.html')

@app.route("/registro", methods=["get", "post"])
def registro():
    from models import Clientes
    if current_user.is_authenticated:
        return redirect(url_for("categorias"))
    form = FormCliente()
    if form.validate_on_submit():
        existe_usuario = Clientes.query.filter_by(usuario=form.usuario.data).first()
        if existe_usuario is None:
            user = Clientes()
            form.populate_obj(user)
            print(user)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("Index"))
        form.usuario.errors.append("Nombre de usuario ya existe.")
    return render_template("registro.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    from models import Clientes
    if current_user.is_authenticated:
        return redirect(url_for("categorias"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Clientes.query.filter_by(usuario=form.usuario.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('Index'))
        form.usuario.errors.append("Usuario o contraseña incorrectas.")
    return render_template('login.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    from models import Clientes
    return Clientes.query.get(int(user_id))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Index'))

@app.route('/categorias')
@app.route('/categoria/<id>')
def categorias(id = '0'):
    from models import Productos,Categorias
    categoria = Categorias.query.get(id)
    if id == '0':
            productos=Productos.query.all()
    else:
            productos=Productos.query.filter_by(categoriaId=id)
    categorias=Categorias.query.order_by(Categorias.id).all()
    print(categorias)
    return render_template('categorias.html',productos=productos,categorias=categorias,categoria=categoria)

@app.route('/perfil/<usuario>', methods=["get", "post"])
@login_required
def perfil(usuario):
    from models import Clientes
    user = Clientes.query.filter_by(usuario=usuario).first()
    print(user.usuario)
    if user is None:
        abort(404)
    form = FormCliente(request.form, obj=user)
    del form.password
    if form.validate_on_submit():
        form.populate_obj(user)
        user.save()
        
        return redirect(url_for("Index"))
    return render_template("registro.html", form=form, perfil=True)

@app.route('/cambiar_password/<usuario>', methods=["get", "post"])
@login_required
def cambiar_password(usuario):
    from models import Clientes
    user = Clientes.query.filter_by(usuario=usuario).first()
    print(user)
    if user is None:
        abort(404)
    form = FormChangePassword()
    if form.validate_on_submit():
        form.populate_obj(user)
        user.save()
        return redirect(url_for("Index"))
    return render_template("cambiar_password.html", form=form)



@app.route('/carrito/add/<id>', methods=["get", "post"])
def carrito_add(id):
    from models import Productos
    if current_user.is_authenticated:
        prod = Productos.query.get(id)
        form = FormCarrito()
        form.id.data = id
        if form.validate_on_submit():
            if prod.stock >= int(form.cantidad.data):
                try:
                    datos = json.loads(request.cookies.get(str(current_user.id)))
                except:
                    datos = []
                actualizar = False
                for dato in datos:
                    if dato["id"] == id:
                        dato["cantidad"] = form.cantidad.data
                        actualizar = True
                if not actualizar:
                    datos.append({"id": form.id.data,
                                "cantidad": form.cantidad.data})
                resp = make_response(redirect(url_for('categorias')))
                resp.set_cookie(str(current_user.id), json.dumps(datos))
                return resp
            form.cantidad.errors.append("No hay productos suficientes.")
        return render_template("carrito_add.html", form=form, prod=prod)
    return redirect(url_for("login"))

@app.route('/carrito')
def carrito():
    from models import Productos
    try:
        datos = json.loads(request.cookies.get(str(current_user.id)))
    except:
        datos = []
    productos = []
    cantidades = []
    total = 0
    for producto in datos:
        productos.append(Productos.query.get(producto["id"]))
        cantidades.append(producto["cantidad"])
        total = total + Productos.query.get(producto["id"]).precio_final() * \
            producto["cantidad"]
    productos = zip(productos, cantidades)
    return render_template('carrito.html', productos=productos, total=total)

@app.route('/carrito_delete/<id>')
@login_required
def carrito_delete(id):
    try:
        datos = json.loads(request.cookies.get(str(current_user.id)))
    except:
        datos = []
    new_datos = []
    for dato in datos:
        if dato["id"] != id:
            new_datos.append(dato)
    resp = make_response(redirect(url_for('carrito')))
    resp.set_cookie(str(current_user.id), json.dumps(new_datos))
    return resp

@app.context_processor
def contar_carrito():
    if not current_user.is_authenticated:
        return {'num_productos': 0}
    if request.cookies.get(str(current_user.id)) is None:
        return {'num_productos': 0}
    else:
        datos = json.loads(request.cookies.get(str(current_user.id)))
        return {'num_productos': len(datos)}


@app.route('/orden')
@login_required
def orden():
    from models import Productos, Orden, Orden_items
    try:
        datos = json.loads(request.cookies.get(str(current_user.id)))
        print(current_user.id)
        print(datos)
    except:
        datos = []
    total = 0
    orden = Orden(fecha=dt.now(), id_cliente=current_user.id, estado_id='4')
    db.session.add(orden)
    db.session.commit()
    print(orden)
    ultimoorden=Orden.query.order_by(desc(Orden.id)).first()
    print(ultimoorden.id)
    for productos in datos:
        total = total + Productos.query.get(productos["id"]).precio_final() * \
            productos["cantidad"]
        detalleorden = Orden_items(id_orden=ultimoorden.id,id_producto=productos["id"], cantidad=productos["cantidad"])
        db.session.add(detalleorden)
        db.session.commit()
        
        update = Productos.query.filter_by(id=productos["id"]).first()
        update2 = update.stock - productos["cantidad"]
        update.stock = update2
        update.save()
        print(update)
    resp = make_response(render_template("orden.html", total=total))
    resp.set_cookie(str(current_user.id), "", expires=0)
    return resp

@app.route('/compras/<usuario>', methods=["get", "post"])
@login_required
def compras(usuario):
    from models import Orden, Clientes, Orden_items, Productos
    user = Clientes.query.filter_by(usuario=usuario).first()
    print(user)
    print(user.id)
    t_orden = Orden.query.filter_by(id_cliente=user.id).join(Orden.relorden).all()
    #t_orden2 = Orden_items.query.filter_by(id_orden='1').join(Orden_items.relproducto).first()
    #t_orden2 = Orden_items.query.filter_by(id_orden='1').join(Orden_items.relproducto).all()
    #print(t_orden2)
    #for prod in t_orden2:
    #    print(prod.relproducto.nombre)
    #Cerveza QUILMES Botella 1 L
    #Cosecha Tardia Chardonnay 750 CC

    #t_orden=Orden_items.query.filter_by(id_orden='1').join(Orden_items.relproducto).all()

    print(t_orden)
    #for ordenes in t_orden:
    #    print (ordenes.id)

    return render_template('compras.html',t_orden=t_orden) #,t_orden2=t_orden2

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404

if __name__ == "__main__":
    app.run(port=80, debug=False)
