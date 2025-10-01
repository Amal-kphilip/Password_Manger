from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for
import sqlite3
import hashlib
import os
import secrets
import string
from cryptography.fernet import Fernet
import base64
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Database configuration
DATABASE_PATH = 'passwords.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class PasswordEncryption:
    @staticmethod
    def encrypt_password(master_password, password):
        key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), b'salt', 100000, 32)
        fernet = Fernet(base64.urlsafe_b64encode(key))
        return fernet.encrypt(password.encode()).decode()

    @staticmethod
    def decrypt_password(master_password, encrypted_password):
        try:
            key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), b'salt', 100000, 32)
            fernet = Fernet(base64.urlsafe_b64encode(key))
            return fernet.decrypt(encrypted_password.encode()).decode()
        except:
            return None

    @staticmethod
    def hash_password(password):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return f"{salt.hex()}:{key.hex()}"

    @staticmethod
    def verify_password(stored_hash, password):
        try:
            salt_hex, key_hex = stored_hash.split(':')
            salt = bytes.fromhex(salt_hex)
            stored_key = bytes.fromhex(key_hex)
            new_key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            return new_key == stored_key
        except:
            return False

    @staticmethod
    def generate_password(length=16):
        chars = string.ascii_letters + string.digits + "!@#$%"
        while True:
            password = ''.join(secrets.choice(chars) for _ in range(length))
            if (any(c.islower() for c in password) and
                any(c.isupper() for c in password) and
                any(c.isdigit() for c in password)):
                return password

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters!', 'danger')
            return render_template('register.html')

        conn = get_db_connection()
        
        # Check if user exists
        existing_user = conn.execute(
            'SELECT id FROM users WHERE username = ?', (username,)
        ).fetchone()
        
        if existing_user:
            flash('Username already exists!', 'danger')
            conn.close()
            return render_template('register.html')

        # Create user
        password_hash = PasswordEncryption.hash_password(password)
        conn.execute(
            'INSERT INTO users (username, email, master_password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        conn.close()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        conn.close()

        if user and PasswordEncryption.verify_password(user['master_password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    password_count = conn.execute(
        'SELECT COUNT(*) FROM passwords WHERE user_id = ?', (session['user_id'],)
    ).fetchone()[0]
    conn.close()

    return render_template('dashboard.html', 
                         username=session['username'],
                         password_count=password_count)

@app.route('/passwords')
@login_required
def passwords():
    master_password = request.args.get('master_password', '')
    search = request.args.get('search', '')

    passwords_list = []
    if master_password:
        conn = get_db_connection()
        
        query = 'SELECT * FROM passwords WHERE user_id = ?'
        params = [session['user_id']]
        
        if search:
            query += ' AND (website LIKE ? OR username LIKE ?)'
            params.extend([f'%{search}%', f'%{search}%'])
        
        passwords_data = conn.execute(query, params).fetchall()
        conn.close()

        for pwd in passwords_data:
            decrypted = PasswordEncryption.decrypt_password(master_password, pwd['encrypted_password'])
            if decrypted:
                passwords_list.append({
                    'id': pwd['id'],
                    'website': pwd['website'],
                    'username': pwd['username'],
                    'password': decrypted,
                    'url': pwd['url'],
                    'category': pwd['category']
                })

    return render_template('passwords.html', passwords=passwords_list, search=search)

@app.route('/add_password', methods=['GET', 'POST'])
@login_required
def add_password():
    if request.method == 'POST':
        website = request.form['website']
        username = request.form['username']
        password = request.form['password']
        url = request.form.get('url', '')
        category = request.form.get('category', 'General')
        master_password = request.form['master_password']

        encrypted = PasswordEncryption.encrypt_password(master_password, password)
        
        conn = get_db_connection()
        conn.execute(
            '''INSERT INTO passwords 
            (user_id, website, username, encrypted_password, url, category) 
            VALUES (?, ?, ?, ?, ?, ?)''',
            (session['user_id'], website, username, encrypted, url, category)
        )
        conn.commit()
        conn.close()
        
        flash('Password added successfully!', 'success')
        return redirect(url_for('passwords') + f'?master_password={master_password}')

    return render_template('add_password.html')

@app.route('/edit_password/<int:password_id>', methods=['GET', 'POST'])
@login_required
def edit_password(password_id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        website = request.form['website']
        username = request.form['username']
        password = request.form['password']
        url = request.form.get('url', '')
        category = request.form.get('category', 'General')
        master_password = request.form['master_password']

        # Encrypt the new password
        encrypted = PasswordEncryption.encrypt_password(master_password, password)
        
        # Update the password entry
        conn.execute(
            '''UPDATE passwords 
            SET website = ?, username = ?, encrypted_password = ?, url = ?, category = ?
            WHERE id = ? AND user_id = ?''',
            (website, username, encrypted, url, category, password_id, session['user_id'])
        )
        conn.commit()
        conn.close()
        
        flash('Password updated successfully!', 'success')
        return redirect(url_for('passwords') + f'?master_password={master_password}')
    
    # GET request - show edit form
    password_data = conn.execute(
        'SELECT * FROM passwords WHERE id = ? AND user_id = ?',
        (password_id, session['user_id'])
    ).fetchone()
    conn.close()
    
    if not password_data:
        flash('Password not found!', 'danger')
        return redirect(url_for('passwords'))
    
    return render_template('edit_password.html', password=password_data)

@app.route('/delete_password/<int:password_id>')
@login_required
def delete_password(password_id):
    conn = get_db_connection()
    conn.execute(
        'DELETE FROM passwords WHERE id = ? AND user_id = ?',
        (password_id, session['user_id'])
    )
    conn.commit()
    conn.close()
    
    flash('Password deleted successfully!', 'success')
    return redirect(url_for('passwords'))

@app.route('/generate_password')
@login_required
def generate_password():
    length = int(request.args.get('length', 16))
    password = PasswordEncryption.generate_password(length)
    return jsonify({'password': password})

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)