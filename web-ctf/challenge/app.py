from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = "sup3r_s3cr3t_k3y_d0nt_gu3ss"

# Initialize database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)''')
    
    # Insert admin user with weak password
    admin_pass = hashlib.md5(b'admin123').hexdigest()
    c.execute("INSERT OR REPLACE INTO users VALUES (1, 'administrator', ?, 'admin')", (admin_pass,))
    
    # Insert regular user
    user_pass = hashlib.md5(b'password').hexdigest()
    c.execute("INSERT OR REPLACE INTO users VALUES (2, 'guest', ?, 'user')", (user_pass,))
    
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        
        # Vulnerable SQL injection
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashlib.md5(password.encode()).hexdigest()}'"
        
        try:
            result = c.execute(query).fetchone()
            if result:
                session['user_id'] = result[0]
                session['username'] = result[1]
                session['role'] = result[3]
                
                if result[3] == 'admin':
                    return redirect(url_for("admin"))
                else:
                    return redirect(url_for("dashboard"))
            else:
                error = "Invalid credentials"
        except sqlite3.Error as e:
            error = f"Database error: {str(e)}"
        
        conn.close()
    
    return render_template("login.html", error=error)

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("dashboard.html", username=session.get('username'))

@app.route("/admin")
def admin():
    if 'user_id' not in session or session.get('role') != 'admin':
        return "Access Denied", 403
    
    # Flag is here but needs more steps
    return render_template("admin.html", username=session.get('username'))

# Hidden debug endpoint
@app.route("/debug/info")
def debug_info():
    if request.headers.get('X-Debug-Token') == 'dev_mode_2024':
        return jsonify({
            'session': dict(session),
            'flag_hint': 'Check the source code comments in admin panel',
            'secret_endpoint': '/s3cr3t_fl4g_3ndp01nt'
        })
    return "Not found", 404

# Secret flag endpoint with additional check
@app.route("/s3cr3t_fl4g_3ndp01nt")
def secret_flag():
    if 'user_id' not in session:
        return "Unauthorized", 401
    
    # Check if user bypassed authentication properly
    user_agent = request.headers.get('User-Agent', '')
    if 'admin' in session.get('username', '').lower() and 'ctf' in user_agent.lower():
        return jsonify({'flag': 'SECE{sql_1nj3ct10n_4nd_4uth_byp4ss_m4st3r}'})
    
    return "Access denied - missing requirements", 403

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
