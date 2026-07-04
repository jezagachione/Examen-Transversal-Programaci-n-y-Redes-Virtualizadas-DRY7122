import sqlite3
import hashlib
from flask import Flask, request, render_template_string

# 1. Creación de la instancia del sitio web
app = Flask(__name__)


INTEGRANTES = {
    "Jean Zagachione": "cisco123",
    "Catalina Torres": "cisco123",
}

def inicializar_bd():
    """Crea la base de datos y almacena usuarios con contraseñas en hash"""
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    # 2. Creación de la tabla SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # 3. Almacenar usuarios y contraseñas en hash
    for user, pwd in INTEGRANTES.items():
        # Uso de hashlib para generar el hash SHA-256 de la contraseña
        pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
        try:
            cursor.execute('INSERT INTO usuarios (username, password_hash) VALUES (?, ?)', (user, pwd_hash))
        except sqlite3.IntegrityError:
            # Si el usuario ya existe, ignoramos el error para no duplicar
            pass 
            
    conn.commit()
    conn.close()

# 4. Ruta principal para validar usuarios
@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ""
    if request.method == 'POST':
        # Obtener datos del formulario
        username_ingresado = request.form.get('username')
        password_ingresada = request.form.get('password')
        
        # Convertir la contraseña ingresada a hash para compararla
        hash_ingresado = hashlib.sha256(password_ingresada.encode()).hexdigest()
        
        # Consulta SQL para validar
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = ? AND password_hash = ?', (username_ingresado, hash_ingresado))
        usuario_valido = cursor.fetchone()
        conn.close()
        
        if usuario_valido:
            mensaje = f" ¡Validación exitosa! Bienvenido, {username_ingresado}."
        else:
            mensaje = " Error: Usuario o contraseña incorrectos."

    # HTML incrustado para la interfaz del sitio web
    html = '''
    <div style="font-family: Arial; margin: 50px;">
        <h2>Sitio de Validación - Examen DRY7122</h2>
        <form method="POST">
            <label>Usuario (Integrante):</label><br>
            <input type="text" name="username" required><br><br>
            <label>Contraseña:</label><br>
            <input type="password" name="password" required><br><br>
            <button type="submit">Validar Ingreso</button>
        </form>
        <h3>{{ mensaje }}</h3>
    </div>
    '''
    return render_template_string(html, mensaje=mensaje)

if __name__ == '__main__':
    print("Inicializando base de datos SQLite...")
    inicializar_bd()
    print("Iniciando servidor web en el puerto 7500...")
    # 5. Ejecutar sitio web utilizando el puerto 7500
    app.run(host='0.0.0.0', port=7500)
