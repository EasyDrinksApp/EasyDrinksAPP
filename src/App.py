from flask import Flask, render_template, redirect, url_for, request, session, escape
import psycopg2
from pprint import pprint
#from flask_sqlalchemy import SQLAlchemy
#from src import config

app = Flask(__name__)
#app.config.from_object(config)
#db = SQLAlchemy(app)

conn = psycopg2.connect(database="d99im3kf48j37", 
user="jyoaemdhbzzmmo", 
password="b7dfc5cb281e23651d3ce373469a74dd82a7ec880831d3d2b2fbeebdbbf16aca", 
host="ec2-23-21-91-183.compute-1.amazonaws.com", 
port="5432")
print("Database Connected...")
cur = conn.cursor()

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    cur.execute("select * from productos")
    bebidas = cur.fetchall()
    #bebidas = Productos.query.all()
    return render_template('productos.html', productos = bebidas)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        usser = request.form["usuario"]
        passwd = request.form["password"]
        query = 'INSERT INTO clientes (usuario, password) VALUES (%s, %s)'
        param = (usser,passwd)
        cur.execute(query, param)
        conn.commit()

        return "You've registered successfully."
        
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usser = request.form["usuario"]
        passwd = request.form["password"]
        query = """select * from clientes where usuario=%s and password=%s"""
        param = (usser,passwd)
        cur.execute(query, param)
        num_row = cur.rowcount

        if (num_row == 1):
            session["usuario"] = usser
            return render_template('index.html')
        return "Your credentials are invalid, check and try again."

    return render_template("login.html")

@app.route("/home")
def home():
    if "usuario" in session:
        return "You are %s" % escape(session["usuario"])
    return "Yoy must log in first."

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return render_template('index.html')

app.secret_key = "123456"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
