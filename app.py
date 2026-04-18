from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Función auxiliar para conectar a la BD
def get_db_connection():
    conn = sqlite3.connect('gym.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ruta 1: Mostrar la página web HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta 2: (API) Consultar Estatus y Procesar Lógica de 30 días
@app.route('/api/consultar/<id_socio>', methods=['GET'])
def consultar_socio(id_socio):
    conn = get_db_connection()
    # Hacemos un JOIN para traer al socio y su último pago
    socio = conn.execute('''
        SELECT s.nombre_completo, p.fecha_pago 
        FROM Socios s 
        LEFT JOIN Pagos p ON s.id_socio = p.id_socio 
        WHERE s.id_socio = ? 
        ORDER BY p.fecha_pago DESC LIMIT 1
    ''', (id_socio,)).fetchone()
    conn.close()

    if socio is None:
        return jsonify({"error": "Socio no encontrado"}), 404

    nombre = socio['nombre_completo']
    fecha_pago_str = socio['fecha_pago']

    # --- LÓGICA DE NEGOCIO (Los 30 días) ---
    fecha_pago = datetime.strptime(fecha_pago_str, '%Y-%m-%d')
    fecha_actual = datetime.now()
    diferencia = (fecha_actual - fecha_pago).days

    if diferencia > 30:
        titulo = "¡Suscripción Vencida!"
        mensaje = f"La suscripción de {nombre} ha expirado.\nTiene {diferencia - 30} días de retraso."
        estado = "danger"
    elif 0 <= diferencia <= 30:
        titulo = "¡Suscripción Al Día!"
        mensaje = f"La cuenta de {nombre} está activa.\nFaltan {30 - diferencia} días para su próximo pago."
        estado = "success"
    else:
        titulo = "Error"
        mensaje = "Fecha futura detectada."
        estado = "warning"

    return jsonify({
        "nombre": nombre,
        "titulo": titulo,
        "mensaje": mensaje,
        "estadoBootstrap": estado
    })

# Ruta 3: (API) Guardar o Actualizar Socio y su Pago
@app.route('/api/guardar', methods=['POST'])
def guardar_socio():
    datos = request.json
    id_socio = datos['id']
    nombre = datos['nombre']
    fecha = datos['fecha']

    conn = get_db_connection()
    # Actualizar o Insertar Socio (Evita duplicados)
    conn.execute('''
        INSERT INTO Socios (id_socio, nombre_completo) 
        VALUES (?, ?) 
        ON CONFLICT(id_socio) DO UPDATE SET nombre_completo = excluded.nombre_completo
    ''', (id_socio, nombre))
    
    # Registrar el nuevo pago
    conn.execute('''
        INSERT INTO Pagos (id_socio, fecha_pago) VALUES (?, ?)
    ''', (id_socio, fecha))
    
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "mensaje": "Datos guardados correctamente en SQLite"})

if __name__ == '__main__':
    app.run(debug=True)