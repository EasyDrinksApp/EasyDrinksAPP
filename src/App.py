from flask import Flask, render_template, redirect, url_for
import psycopg2
from pprint import pprint

#database = peewee.PostgresqlDatabase("dec3h86c92b21q", 
#host="ec2-54-225-129-101.compute-1.amazonaws.com", 
#port="5432", 
#user="teqoigyfhnlpyr", 
#password="55dc4764a5eb9481f805fe44fe3d7d9c6a40816b866ad03fdba74fa75c42b7cb")
#class Productos(peewee.Model):
#    id = peewee.IntegerField()
#    nombre = peewee.CharField()
#    precio = peewee.CharField()
#
#    class Meta:
#        database = database
#        db_table = 'productos'
#database.connect()

app = Flask(__name__)

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
    return render_template('productos.html', productos = bebidas)

@app.route('/adminProd')
def adminProd():

    return render_template('adminProd.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
