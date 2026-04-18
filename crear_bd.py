import sqlite3

def crear_base_datos():
    # Se conecta (y crea) el archivo SQLite
    conexion = sqlite3.connect('gym.db')
    cursor = conexion.cursor()

    # 1. Crear Tablas (Simplificadas para tu UI)
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Socios (
            id_socio VARCHAR(10) PRIMARY KEY,
            nombre_completo VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Pagos (
            id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
            id_socio VARCHAR(10),
            fecha_pago DATE NOT NULL,
            FOREIGN KEY (id_socio) REFERENCES Socios(id_socio)
        );
    ''')

    # 2. Insertar algunos registros de prueba (Ignorar si ya existen)
    try:
        cursor.executescript('''
            INSERT INTO Socios (id_socio, nombre_completo) VALUES 
            ('SOC-001', 'Jose Alfredo'), 
            ('SOC-002', 'Juan Pérez'),
            ('SOC-003', 'León García');

            INSERT INTO Pagos (id_socio, fecha_pago) VALUES 
            ('SOC-001', '2026-03-15'), 
            ('SOC-002', '2026-04-10'),
            ('SOC-003', '2026-02-28');
        ''')
        print("Base de datos creada y poblada exitosamente.")
    except sqlite3.IntegrityError:
        print("La base de datos ya tenía registros iniciales.")

    conexion.commit()
    conexion.close()

if __name__ == '__main__':
    crear_base_datos()