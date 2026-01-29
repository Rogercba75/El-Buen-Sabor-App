import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Base de datos segura
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miga_pro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DICCIONARIO COMPLETO DE LA FOTO (Precios por Docena)
MENU = {
    "paleta_queso": {"nombre": "Paleta y Queso", "precio": 22000},
    "paleta_verdura": {"nombre": "Paleta y Verdura", "precio": 22000},
    "jamon_queso": {"nombre": "Jamón y Queso", "precio": 26000},
    "jamon_verdura": {"nombre": "Jamón y Verdura", "precio": 26000},
    "jamon_roquefort": {"nombre": "Jamón y Roquefort", "precio": 30000},
    "jamon_palmitos": {"nombre": "Jamón y Palmitos", "precio": 30000},
    "jamon_anana": {"nombre": "Jamón y Ananá", "precio": 32000},
    "jamon_rucula": {"nombre": "Jamón y Rúcula", "precio": 30000},
    "jamon_crudo_queso": {"nombre": "Crudo y Queso", "precio": 36000},
    "bondiola_queso": {"nombre": "Bondiola y Queso", "precio": 34000},
    "ternera_queso": {"nombre": "Ternera y Queso", "precio": 36000},
    "atun_queso": {"nombre": "Atún y Queso", "precio": 34000},
    "queso_tomate_huevo": {"nombre": "Queso, Tomate, Huevo y Aceitunas", "precio": 32000}
}

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100))
    sabor = db.Column(db.String(100))
    docenas = db.Column(db.Float)
    total = db.Column(db.Float)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html', menu=MENU)

@app.route('/api/pedidos', methods=['GET', 'POST'])
def gestionar_pedidos():
    if request.method == 'POST':
        data = request.json
        s_key = data['sabor']
        cant = float(data['docenas'])
        total_v = MENU[s_key]['precio'] * cant
        nuevo = Pedido(cliente=data['cliente'], sabor=MENU[s_key]['nombre'], docenas=cant, total=total_v)
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"status": "success", "total": total_v})
    
    pedidos = Pedido.query.order_by(Pedido.id.desc()).all()
    return jsonify([{"cliente": p.cliente, "sabor": p.sabor, "docenas": p.docenas, "total": p.total} for p in pedidos])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
