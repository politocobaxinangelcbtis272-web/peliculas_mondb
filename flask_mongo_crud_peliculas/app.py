from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")

MONGO_URI = os.environ.get("MONGO_URI" ,"mongodb+srv://peliculas:peliculas1253@peliculas.0nwysmz.mongodb.net/?peliculas=peliculas1253")
client = MongoClient(MONGO_URI)
db = client['peliculas_db']
peliculas_collection = db['peliculas']


app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif','webp'}


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


users = {
    'admin': generate_password_hash('admin123'),
    'usuario': generate_password_hash('password123'),
    'polito': generate_password_hash('polito123')
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def to_str_id(doc):
    if not doc:
        return None
    doc['id'] = str(doc['_id'])
    return doc

def to_str_list(cursor):
    return [to_str_id(d) for d in cursor]

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('🔒 Por favor inicia sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    """Redirige al login desde la raíz"""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    # Si ya está logueado, redirigir al dashboard
    if 'user' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('❌ Por favor ingresa usuario y contraseña', 'danger')
            return render_template('login.html')
        
        if username in users and check_password_hash(users[username], password):
            session['user'] = username
            session['login_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            flash(f'🎉 ¡Bienvenido {username}! Has iniciado sesión correctamente', 'success')
            return redirect(url_for('index'))
        else:
            flash('❌ Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    if 'user' in session:
        username = session['user']
        session.clear()
        flash(f'👋 ¡Hasta pronto {username}! Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

@app.route("/dashboard")
@login_required
def index():
    """Dashboard principal con todas las películas"""
    todas_peliculas = to_str_list(peliculas_collection.find().sort("fecha_creacion", -1))
    
    stats = {
        'total_peliculas': peliculas_collection.count_documents({}),
        'usuario_actual': session.get('user')
    }
    
    return render_template("index.html", 
                         peliculas=todas_peliculas, 
                         stats=stats,
                         username=session.get('user'))

@app.route('/profile')
@login_required
def profile():
    """Página de perfil del usuario"""
    user_info = {
        'username': session.get('user'),
        'login_time': session.get('login_time'),
        'session_id': session.sid[:8] + '...' if session.sid else 'N/A'
    }
    return render_template('profile.html', user=user_info)

@app.route("/pelicula/new", methods=["GET", "POST"])
@login_required
def create_pelicula():
    """Crear nueva película"""
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        año = request.form.get("año", "").strip()
        genero = request.form.get("genero", "").strip()
        calificacion_str = request.form.get("calificacion", "").strip()
        comentario = request.form.get("comentario", "").strip()
        
        try:
            calificacion = float(calificacion_str) if calificacion_str else None
        except ValueError:
            calificacion = None
        
        data = {
            "nombre": nombre,
            "año": int(año) if año.isdigit() else None,
            "genero": genero,
            "calificacion": calificacion,
            "comentario": comentario,
            "fecha_creacion": datetime.now(),
            "creado_por": session.get('user')
        }
        
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                data['imagen'] = filename
        
        peliculas_collection.insert_one(data)
        flash('🎬 Película agregada correctamente!', 'success')
        return redirect(url_for('index'))
    
    return render_template("create.html")

@app.route("/pelicula/<id>")
@login_required
def view_pelicula(id):
    """Ver detalles de una película"""
    try:
        pelicula = peliculas_collection.find_one({"_id": ObjectId(id)})
    except:
        pelicula = None
    
    if not pelicula:
        flash("Película no encontrada.", "danger")
        return redirect(url_for("index"))
    
    pelicula = to_str_id(pelicula)
    return render_template("view.html", pelicula=pelicula)

@app.route("/pelicula/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_pelicula(id):
    """Editar película existente"""
    try:
        pelicula = peliculas_collection.find_one({"_id": ObjectId(id)})
    except:
        pelicula = None
    
    if not pelicula:
        flash("Película no encontrada.", "danger")
        return redirect(url_for("index"))
    
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        año = request.form.get("año", "").strip()
        genero = request.form.get("genero", "").strip()
        calificacion_str = request.form.get("calificacion", "").strip()
        comentario = request.form.get("comentario", "").strip()
        
        try:
            calificacion = float(calificacion_str) if calificacion_str else None
        except ValueError:
            calificacion = None
        
        update_data = {
            "nombre": nombre,
            "año": int(año) if año.isdigit() else None,
            "genero": genero,
            "calificacion": calificacion,
            "comentario": comentario,
            "ultima_actualizacion": datetime.now()
        }
        
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                update_data['imagen'] = filename
        
        peliculas_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        flash("✅ Película actualizada correctamente.", "success")
        return redirect(url_for("index"))
    
    pelicula = to_str_id(pelicula)
    return render_template("edit.html", pelicula=pelicula)

@app.route("/pelicula/delete/<id>", methods=["POST"])
@login_required
def delete_pelicula(id):
    """Eliminar película"""
    try:
        peliculas_collection.delete_one({"_id": ObjectId(id)})
        flash("🗑️ Película eliminada correctamente.", "info")
    except Exception as e:
        flash("Error al eliminar: " + str(e), "danger")
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found_error(error):
    flash('⚠️ Página no encontrada', 'warning')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(error):
    flash('❌ Error interno del servidor', 'danger')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)