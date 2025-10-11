from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from config import DB_CONFIG, SECRET_KEY
from datetime import date

app = Flask(__name__)
app.secret_key = SECRET_KEY


# ---------- Helper ----------
def get_db():
    """Establish a new DB connection each time."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print("Database connection error:", err)
        return None


# ---------- Routes ----------

@app.route('/')
def index():
    return render_template('index.html')


# ---------- Register ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']

        hashed = generate_password_hash(password)

        conn = get_db()
        if not conn:
            flash("Database connection failed", "danger")
            return redirect(url_for('register'))

        cur = conn.cursor()
        try:
            cur.execute(
                'INSERT INTO users (name, email, password, address) VALUES (%s, %s, %s, %s)',
                (name, email, hashed, address)
            )
            conn.commit()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as e:
            conn.rollback()
            flash(f'Error: {e}', 'danger')
        finally:
            cur.close()
            conn.close()

    return render_template('register.html')


# ---------- Login ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        if not conn:
            flash("Database connection failed", "danger")
            return redirect(url_for('login'))

        cur = conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM users WHERE email=%s', (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['role'] = user['role']
            flash('Logged in successfully', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')


# ---------- Logout ----------
@app.route('/logout')
def logout():
    session.clear()
    flash('You are logged out', 'info')
    return redirect(url_for('index'))


# ---------- Dashboard redirect ----------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('view_status'))


# ---------- Raise complaint ----------
@app.route('/raise', methods=['GET', 'POST'])
def raise_complaint():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        waste_type = request.form['waste_type']
        description = request.form['description']
        complaint_date = request.form.get('complaint_date') or date.today().isoformat()

        conn = get_db()
        if not conn:
            flash("Database connection failed", "danger")
            return redirect(url_for('raise_complaint'))

        cur = conn.cursor()
        cur.execute(
            'INSERT INTO complaints (user_id, complaint_date, waste_type, description) VALUES (%s, %s, %s, %s)',
            (session['user_id'], complaint_date, waste_type, description)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash('Complaint raised successfully', 'success')
        return redirect(url_for('view_status'))

    return render_template('raise_complaint.html')


# ---------- View status (User) ----------
@app.route('/status')
def view_status():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    if not conn:
        flash("Database connection failed", "danger")
        return redirect(url_for('dashboard'))

    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM complaints WHERE user_id=%s ORDER BY created_at DESC', (session['user_id'],))
    complaints = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('view_status.html', complaints=complaints)


# ---------- Admin dashboard ----------
@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied', 'danger')
        return redirect(url_for('login'))

    conn = get_db()
    if not conn:
        flash("Database connection failed", "danger")
        return redirect(url_for('dashboard'))

    cur = conn.cursor(dictionary=True)
    cur.execute('''
        SELECT c.id, c.complaint_date, c.waste_type, c.description, c.status,
               u.name AS user_name, u.address
        FROM complaints c
        JOIN users u ON c.user_id = u.id
        ORDER BY c.complaint_date ASC, c.created_at DESC
    ''')
    complaints = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('admin_dashboard.html', complaints=complaints)


# ---------- Update status (Admin AJAX) ----------
@app.route('/update_status', methods=['POST'])
def update_status():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'msg': 'Unauthorized'}), 403

    data = request.get_json()
    cid = data.get('id')
    new_status = data.get('status')

    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE complaints SET status=%s WHERE id=%s', (new_status, cid))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'success': True})


# ---------- Run ----------
if __name__ == '__main__':
    app.run(port=5000,debug=True)
