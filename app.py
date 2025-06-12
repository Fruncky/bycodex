import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'change_me')
DATABASE = 'contacts.db'

# Ensure database exists
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()
cursor.execute(
    """CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone TEXT,
        postal_code TEXT,
        schedule TEXT
    )"""
)
conn.commit()
conn.close()


def send_email(data):
    server = os.getenv('MAIL_SERVER')
    port = int(os.getenv('MAIL_PORT', '0'))
    username = os.getenv('MAIL_USERNAME')
    password = os.getenv('MAIL_PASSWORD')
    receiver = os.getenv('RECEIVER_EMAIL')
    use_tls = os.getenv('MAIL_USE_TLS', 'False') == 'True'

    msg_content = """
Nouveau contact:
Prénom: {first_name}
Nom: {last_name}
Email: {email}
Téléphone: {phone}
Code postal: {postal_code}
Créneau: {schedule}
""".format(**data)
    msg = MIMEText(msg_content)
    msg['Subject'] = 'Nouveau contact Formation IA'
    msg['From'] = username
    msg['To'] = receiver

    with smtplib.SMTP(server, port) as smtp:
        if use_tls:
            smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(msg)


def save_contact(data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO contacts (first_name, last_name, email, phone, postal_code, schedule) VALUES (?, ?, ?, ?, ?, ?)',
        (
            data['first_name'],
            data['last_name'],
            data['email'],
            data['phone'],
            data['postal_code'],
            data['schedule'],
        ),
    )
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/contact', methods=['POST'])
def contact():
    required_fields = ['first_name', 'last_name', 'email', 'phone', 'postal_code']
    data = {field: request.form.get(field, '').strip() for field in required_fields}
    data['schedule'] = request.form.get('schedule', '').strip()

    if not all(data[field] for field in required_fields):
        flash('Veuillez remplir tous les champs obligatoires.')
        return redirect(url_for('index'))

    try:
        save_contact(data)
        send_email(data)
    except Exception:
        flash("Une erreur s'est produite lors de l'envoi du message.")
        return redirect(url_for('index'))

    return render_template('confirm.html', data=data)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
