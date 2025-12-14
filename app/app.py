import os
import shutil
import sqlite3
import hashlib
import base64
from io import BytesIO
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, Response
from wtforms import Form, StringField, HiddenField, validators
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

def get_db_connection():
    db_path = 'database.db'
    
    # Check if we are running in a serverless environment (Linux-like)
    if os.name != 'nt':
        # Use /tmp for writable database
        tmp_db_path = '/tmp/database.db'
        
        # If database doesn't exist in /tmp, copy it from source
        if not os.path.exists(tmp_db_path):
            if os.path.exists(db_path):
                shutil.copyfile(db_path, tmp_db_path)
            else:
                # Handle case where original DB might be elsewhere or init needed
                # For now assume it exists in repo
                pass
                
        db_path = tmp_db_path

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

from functools import wraps

# ... (Previous imports)

# Auth Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logueado'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["GET", "POST"])
def index_redirect():
    return redirect(url_for("inicio"))

# --- ADMIN ROUTES ---

@app.route("/ADreservar", methods=["GET", "POST"])
@login_required
def show_records():
    conn = get_db_connection()
    if request.method == "POST":
        keyword = request.form["keyword"]
        search_query = """
            SELECT * FROM reservaciones
            WHERE nombre LIKE ? OR apellidos LIKE ? OR Fecha LIKE ?
        """
        data = (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
        records = conn.execute(search_query, data).fetchall()
    else:
        records = conn.execute("SELECT * FROM reservaciones").fetchall()
    
    conn.close()
    return render_template("ADreservar.html", records=records)

@app.route("/insert", methods=["POST"])
@login_required
def insert_record():
    conn = get_db_connection()
    insert_query = """
        INSERT INTO reservaciones (nombre, apellidos, correo, telefono, Fecha, nombre_cabana, fecha_de_salida, precio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    data = (
        request.form["nombre"], 
        request.form["apellidos"], 
        request.form["correo"], 
        request.form["telefono"], 
        request.form["Fecha"], 
        request.form["nombre_cabana"], 
        request.form["fecha_de_salida"], 
        request.form["precio"]
    )
    conn.execute(insert_query, data)
    conn.commit()
    conn.close()
    return redirect(url_for("show_records"))

@app.route("/update/<int:record_id>", methods=["POST"])
@login_required
def update_record(record_id):
    conn = get_db_connection()
    update_query = """
        UPDATE reservaciones
        SET nombre = ?, apellidos = ?, correo = ?, telefono = ?, Fecha = ?, nombre_cabana = ?, fecha_de_salida = ?, precio = ?
        WHERE id = ?
    """
    data = (
        request.form["nombre"], 
        request.form["apellidos"], 
        request.form["correo"], 
        request.form["telefono"], 
        request.form["Fecha"], 
        request.form["nombre_cabana"], 
        request.form["fecha_de_salida"], 
        request.form["precio"], 
        record_id
    )
    conn.execute(update_query, data)
    conn.commit()
    conn.close()
    return redirect(url_for("show_records"))

@app.route("/delete/<int:record_id>", methods=["POST"])
@login_required
def delete_record(record_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM reservaciones WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("show_records"))

# --- AUTH ROUTES ---

@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword':
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']
        _password_hash = hashlib.sha512(_password.encode()).hexdigest()

        conn = get_db_connection()
        account = conn.execute('SELECT * FROM usuarios WHERE correo = ? AND password = ?', (_correo, _password_hash)).fetchone()
        conn.close()

        if account:
            session['logueado'] = True
            session['id'] = account['id']
            return redirect(url_for("admin"))
        else:
            return render_template('login.html', mensaje="Credenciales incorrectas")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- PUBLIC ROUTES ---
class ReservaForm(Form):
    nombre = StringField('Nombre', [validators.InputRequired()])
    apellidos = StringField('Apellidos', [validators.InputRequired()])
    correo = StringField('Correo electrónico', [validators.InputRequired(), validators.Email()])
    telefono = StringField('Teléfono', [validators.InputRequired()])
    fecha = StringField('Fecha de reserva', [validators.InputRequired()])
    nombre_cabana = HiddenField('Nombre de la cabaña')
    fecha_de_salida = StringField('Fecha de salida')
    precio = HiddenField('Precio', default=150)

@app.route('/formulario', methods=['GET', 'POST'])
def reserva():
    form = ReservaForm(request.form)
    
    if request.method == 'POST' and form.validate():
        conn = get_db_connection()
        insert_query = "INSERT INTO reservaciones (nombre, apellidos, correo, telefono, fecha, nombre_cabana, fecha_de_salida, precio) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        data = (
            form.nombre.data, 
            form.apellidos.data, 
            form.correo.data, 
            form.telefono.data, 
            form.fecha.data, 
            form.nombre_cabana.data, 
            form.fecha_de_salida.data, 
            form.precio.data
        )
        conn.execute(insert_query, data)
        conn.commit()
        conn.close()
        
        pdf = generate_pdf(
            form.nombre.data, 
            form.apellidos.data, 
            form.correo.data, 
            form.telefono.data, 
            form.fecha.data, 
            form.nombre_cabana.data, 
            form.fecha_de_salida.data, 
            form.precio.data
        )
        return send_pdf(pdf)

    return render_template('formulario.html', form=form)

def generate_pdf(nombre, apellidos, correo, telefono, fecha, nombre_cabana, fecha_de_salida, precio):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    elements.append(Paragraph("Comprobante de Reservación", styles['Title']))
    elements.append(Spacer(1, 12))
    
    details = [
        f"<b>Cabaña:</b> {nombre_cabana}",
        f"<b>Huésped:</b> {nombre} {apellidos}",
        f"<b>Fecha Entrada:</b> {fecha}",
        f"<b>Fecha Salida:</b> {fecha_de_salida}",
        f"<b>Total:</b> ${precio}",
        "<br/>",
        "<b>Políticas:</b>",
        "1. Check-in 3:00 PM / Check-out 12:00 PM",
        "2. Pago requerido para confirmar."
    ]
    
    for detail in details:
        elements.append(Paragraph(detail, styles['Normal']))
        elements.append(Spacer(1, 6))

    doc.build(elements)
    buffer.seek(0)
    return buffer

def send_pdf(pdf):
    return Response(
        pdf.read(),
        mimetype='application/pdf',
        headers={'Content-Disposition': 'inline;filename=reservacion.pdf'}
    )

@app.route('/Estadisticas')
@login_required
def Estadisticas():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT Fecha as fecha FROM reservaciones", conn)
    conn.close()

    if df.empty:
        return render_template('Estadisticas.html', graph=None)

    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    reservations_per_day = df['fecha'].value_counts().sort_index()

    plt.figure(figsize=(10, 5))
    reservations_per_day.plot(kind='bar', color='skyblue')
    plt.title('Reservaciones por Día')
    plt.tight_layout()

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.read()).decode()
    plt.close()

    return render_template('Estadisticas.html', graph=img_base64)

# --- NAVIGATION ROUTES ---

@app.route("/inicio/")
def inicio():
    return render_template("inicio.html")

@app.route("/reservar/")
def reservar():
    return render_template("reservar.html")

@app.route("/admin/")
@login_required
def admin():
    return render_template("admin.html")

@app.route("/ADusuarios/")
@login_required
def ADusuarios():
    return render_template("ADusuarios.html")

@app.route("/ADcabañas/")
@login_required
def ADcabañas():
    return render_template("ADcabañas.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)