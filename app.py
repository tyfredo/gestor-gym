from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'gym.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/consultar/<id_socio>', methods=['GET'])
def consultar_socio(id_socio):
    conn = get_db_connection()
    # JOIN para traer el Plan y el Nombre del Recepcionista que cobró el último pago
    socio = conn.execute('''
        SELECT s.nombre_completo, p.fecha_pago, m.nombre_plan, r.nombre AS nombre_recep
        FROM Socios s 
        LEFT JOIN Pagos p ON s.id_socio = p.id_socio 
        LEFT JOIN Membresias m ON s.id_membresia = m.id_membresia
        LEFT JOIN Recepcionistas r ON p.id_recepcionista = r.id_recepcionista
        WHERE s.id_socio = ? 
        ORDER BY p.id_pago DESC LIMIT 1
    ''', (id_socio,)).fetchone()
    conn.close()

    if socio is None:
        return jsonify({"error": "Socio no encontrado"}), 404

    nombre = socio['nombre_completo']
    fecha_pago_str = socio['fecha_pago']
    plan = socio['nombre_plan'] if socio['nombre_plan'] else "Sin plan"
    recepcionista = socio['nombre_recep'] if socio['nombre_recep'] else "Desconocido"

    fecha_pago = datetime.strptime(fecha_pago_str, '%Y-%m-%d')
    diferencia = (datetime.now() - fecha_pago).days

    if diferencia > 30:
        titulo = "¡Suscripción Vencida!"
        mensaje = f"Socio: {nombre}\nPlan: {plan}\nAtendido por: {recepcionista}\n(Vencido por {diferencia - 30} días)"
        estado = "danger"
    else:
        titulo = "¡Suscripción Al Día!"
        mensaje = f"Socio: {nombre}\nPlan: {plan}\nAtendido por: {recepcionista}\n(Faltan {30 - diferencia} días)"
        estado = "success"

    return jsonify({
        "titulo": titulo,
        "mensaje": mensaje,
        "estadoBootstrap": estado,
        "nombre": nombre
    })

@app.route('/api/guardar', methods=['POST'])
def guardar_socio():
    datos = request.json
    id_s = datos['id']
    nom = datos['nombre']
    fec = datos['fecha']
    id_r = datos['id_recepcionista'] # Recibimos el recepcionista de la web

    conn = get_db_connection()
    try:
        # Actualizar o insertar socio
        existe = conn.execute('SELECT 1 FROM Socios WHERE id_socio = ?', (id_s,)).fetchone()
        if existe:
            conn.execute('UPDATE Socios SET nombre_completo = ? WHERE id_socio = ?', (nom, id_s))
        else:
            conn.execute('INSERT INTO Socios (id_socio, nombre_completo, id_membresia) VALUES (?, ?, 1)', (id_s, nom))
        
        # Registrar el pago con el ID del recepcionista real
        conn.execute('INSERT INTO Pagos (id_socio, fecha_pago, id_recepcionista) VALUES (?, ?, ?)', (id_s, fec, id_r))
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)