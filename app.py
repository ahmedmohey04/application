from flask import Flask, request, jsonify, session, redirect, url_for, render_template
import mariadb

app = Flask(__name__)
app.secret_key = "b'8\xf9\x1e\xd7\xaf\xf6\xd0\xd8\x08\x9c/\xb2\xca\x11-+\xc6\xcf(\xdb\xb9\xf3P|'"

# Database connection
def get_db_connection():
    conn = mariadb.connect(
        user='root',
        password='31283128',
        host='127.0.0.1',
        port=3306,
        database='contacts_db'
    )
    return conn

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('contact_list'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

# My Contact List page
@app.route('/contacts')
def contact_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name FROM contacts WHERE user_id=?", (user_id,))
    contacts = cur.fetchall()
    return render_template('contact_list.html', contacts=contacts)

# Add Contact page
@app.route('/contacts/add', methods=['GET', 'POST'])
def add_contact():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        user_id = session['user_id']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO contacts (user_id, full_name, email, phone_number) VALUES (?, ?, ?, ?)",
                    (user_id, full_name, email, phone_number))
        conn.commit()
        return redirect(url_for('contact_list'))
    return render_template('add_contact.html')

# Contact Details page
@app.route('/contacts/<int:contact_id>', methods=['GET', 'POST'])
def contact_details(contact_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        email = request.form['email']
        phone_number = request.form['phone_number']
        cur.execute("UPDATE contacts SET email=?, phone_number=? WHERE id=?",
                    (email, phone_number, contact_id))
        conn.commit()
        return redirect(url_for('contact_list'))
    cur.execute("SELECT full_name, email, phone_number FROM contacts WHERE id=?", (contact_id,))
    contact = cur.fetchone()
    return render_template('contact_details.html', contact=contact)

if __name__ == '__main__':
    app.run(debug=True)
