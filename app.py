from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miga_pro.db'
db = SQLAlchemy(app)

# MODELO DE BASE DE DATOS
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100))
    sabor = db.Column(db.String(50))
    docenas = db.Column(db.Float)
    estado = db.Column(db.String(20), default="Pendiente")

# RECETAS (Gramajes por 1 Plancha / 2 Docenas)
RECETAS = {
    "jamon_y_queso": {"nombre": "Jamón y Queso", "jamon": 0.45, "queso": 0.40},
    "jamon_y_huevo": {"nombre": "Jamón y Huevo", "jamon": 0.45, "huevo": 6}
}

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/pedidos', methods=['GET', 'POST'])
def gestionar_pedidos():
    if request.method == 'POST':
        data = request.json
        nuevo = Pedido(cliente=data['cliente'], sabor=data['sabor'], docenas=float(data['docenas']))
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"msg": "Pedido Guardado"})
    
    pedidos = Pedido.query.all()
    return jsonify([{"cliente": p.cliente, "sabor": p.sabor, "docenas": p.docenas} for p in pedidos])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
