from flask import Flask, jsonify, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
DATABASE = 'users.db'

# --- Utilities ---
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def validate_user_data(data, for_update=False):
    required = ['name', 'email', 'password'] if not for_update else ['name', 'email']
    for field in required:
        if field not in data:
            return False, f"Missing required field: {field}"

    if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
        return False, "Invalid email format"

    return True, ""

# --- Routes ---
@app.route('/')
def health_check():
    return jsonify({'status': 'ok'}), 200

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT id, name, email FROM users').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users]), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT id, name, email FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user)), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    valid, msg = validate_user_data(data)
    if not valid:
        return jsonify({'error': msg}), 400

    hashed_password = generate_password_hash(data['password'])
    try:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (data['name'], data['email'], hashed_password)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'User created'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 409

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    valid, msg = validate_user_data(data, for_update=True)
    if not valid:
        return jsonify({'error': msg}), 400

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404

    conn.execute(
        'UPDATE users SET name = ?, email = ? WHERE id = ?',
        (data['name'], data['email'], user_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'User updated'}), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User deleted'}), 200

@app.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name', '')
    if not name:
        return jsonify({'error': 'Missing name parameter'}), 400
    conn = get_db_connection()
    users = conn.execute('SELECT id, name, email FROM users WHERE name LIKE ?', (f'%{name}%',)).fetchall()
    conn.close()
    return jsonify([dict(user) for user in users]), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password required'}), 400

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (data['email'],)).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], data['password']):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

# --- Main ---
if __name__ == '__main__':
    app.run(debug=True)
