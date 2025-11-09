from flask import Flask, request, jsonify
import sqlite3
import subprocess

app = Flask(__name__)

# Initialize a simple database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (id, username, email) VALUES (1, 'alice', 'alice@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, email) VALUES (2, 'bob', 'bob@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, email) VALUES (3, 'charlie', 'charlie@example.com')")
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the User API", "endpoints": ["/user/<username>", "/ping"]})

# VULNERABILITY 1: SQL Injection
# Using string formatting instead of parameterized queries
@app.route('/user/<username>')
def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # VULNERABLE: SQL injection through string formatting
    query = "SELECT * FROM users WHERE username = '%s'" % username
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({"id": user[0], "username": user[1], "email": user[2]})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/ping')
def ping():
    host = request.args.get('host', '127.0.0.1')
    try:
        result = subprocess.run(['ping', '-c', '1', host], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        return jsonify({
            "message": f"Ping to {host} completed", 
            "exit_code": result.returncode,
            "output": result.stdout
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Ping timeout"}), 408
    except Exception as e:
        return jsonify({"error": "Ping failed"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

