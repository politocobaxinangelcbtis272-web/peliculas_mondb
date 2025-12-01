from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

users = {
    'admin': generate_password_hash('admin123')
}

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['admin']
        password = request.form['admin123']
        
        if username in users and check_password_hash(users[username], password):
            session['user'] = username
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas')
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))