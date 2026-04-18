import sqlite3

def crear_base_datos():
    # Creamos un archivo nuevo y limpio
    conexion = sqlite3.connect('gym.db')
    cursor = conexion.cursor()

    # --- CREACIÓN DE LAS 5 TABLAS OBLIGATORIAS ---
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Membresias (
            id_membresia INTEGER PRIMARY KEY,
            nombre_plan VARCHAR(50) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Recepcionistas (
            id_recepcionista INTEGER PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Socios (
            id_socio VARCHAR(10) PRIMARY KEY,
            nombre_completo VARCHAR(100) NOT NULL,
            id_membresia INT,
            FOREIGN KEY (id_membresia) REFERENCES Membresias(id_membresia)
        );

        CREATE TABLE IF NOT EXISTS Pagos (
            id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
            id_socio VARCHAR(10),
            fecha_pago DATE NOT NULL,
            id_recepcionista INT,
            FOREIGN KEY (id_socio) REFERENCES Socios(id_socio),
            FOREIGN KEY (id_recepcionista) REFERENCES Recepcionistas(id_recepcionista)
        );

        CREATE TABLE IF NOT EXISTS Accesos (
            id_acceso INTEGER PRIMARY KEY AUTOINCREMENT,
            id_socio VARCHAR(10),
            estado_acceso VARCHAR(20) NOT NULL,
            FOREIGN KEY (id_socio) REFERENCES Socios(id_socio)
        );
    ''')

    # --- INSERCIÓN DE DATOS (Exactamente 10 registros por tabla) ---
    try:
        cursor.executescript('''
            -- 10 Registros en Membresias
            INSERT INTO Membresias (id_membresia, nombre_plan) VALUES 
            (1, 'Básica'), (2, 'Premium'), (3, 'Anual'), (4, 'Estudiante'), (5, 'VIP'),
            (6, 'Familiar'), (7, 'Pareja'), (8, 'Semestral'), (9, 'Trimestral'), (10, 'Diaria');

            -- 10 Registros en Recepcionistas
            INSERT INTO Recepcionistas (id_recepcionista, nombre) VALUES 
            (1, 'Gerardo'), (2, 'Ana'), (3, 'Carlos'), (4, 'Diana'), (5, 'Elena'),
            (6, 'Fernando'), (7, 'Gloria'), (8, 'Hugo'), (9, 'Irene'), (10, 'Javier');

            -- 10 Registros en Socios
            INSERT INTO Socios (id_socio, nombre_completo, id_membresia) VALUES 
            ('SOC-001', 'Jose Alfredo', 1), ('SOC-002', 'Maria Fernanda', 2), 
            ('SOC-003', 'Luis Magallanes', 3), ('SOC-004', 'Andrea Torres', 4), 
            ('SOC-005', 'Pedro Soto', 5), ('SOC-006', 'Sofia Garza', 6), 
            ('SOC-007', 'Raul Medina', 7), ('SOC-008', 'Carmen Vega', 8), 
            ('SOC-009', 'Roberto Pineda', 9), ('SOC-010', 'Laura Salinas', 10);

            -- 10 Registros en Pagos
            INSERT INTO Pagos (id_socio, fecha_pago, id_recepcionista) VALUES 
            ('SOC-001', '2026-03-15', 1), ('SOC-002', '2026-04-10', 2), 
            ('SOC-003', '2026-02-28', 3), ('SOC-004', '2026-04-15', 4), 
            ('SOC-005', '2026-01-10', 5), ('SOC-006', '2026-04-01', 6), 
            ('SOC-007', '2026-03-05', 7), ('SOC-008', '2026-04-18', 8), 
            ('SOC-009', '2026-04-02', 9), ('SOC-010', '2026-03-20', 10);
            
            -- 10 Registros en Accesos
            INSERT INTO Accesos (id_socio, estado_acceso) VALUES 
            ('SOC-001', 'Permitido'), ('SOC-002', 'Permitido'), ('SOC-003', 'Denegado'), 
            ('SOC-004', 'Permitido'), ('SOC-005', 'Permitido'), ('SOC-006', 'Permitido'), 
            ('SOC-007', 'Denegado'), ('SOC-008', 'Permitido'), ('SOC-009', 'Permitido'), 
            ('SOC-010', 'Permitido');
        ''')
        
    except sqlite3.IntegrityError:
        print("Los registros ya existen en la base de datos.")

    conexion.commit()
    conexion.close()

if __name__ == '__main__':
    crear_base_datos()