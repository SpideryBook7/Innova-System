from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from buscar import validate_input 
import hashlib
from io import BytesIO
from flask import Flask, request, render_template, Response
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from wtforms import StringField, DateField, validators
from wtforms import Form, StringField, validators
from datetime import datetime
from wtforms import FloatField
from wtforms import Form, StringField, validators, DecimalField
import base64
# pylint: disable=unused-import
import pandas as pd
import matplotlib.pyplot as plt
# pylint: enable=unused-importfrom wtforms import StringField, HiddenField
from wtforms import StringField, HiddenField
from wtforms import Form, StringField, HiddenField


app = Flask(__name__)

# Configura la conexión a la base de datos MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "crud"
}

#/ADreservar/#

def connect_to_database():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

@app.route("/ADreservar", methods=["GET", "POST"])
def show_records():
    conn = connect_to_database()
    if not conn:
        return "Error de conexión a la base de datos"

    if request.method == "POST":
        keyword = request.form["keyword"]
        cursor = conn.cursor()
        search_query = """
            SELECT id, nombre, apellidos, correo, telefono, Fecha, nombre_cabana, fecha_de_salida, precio   
            FROM reservaciones
            WHERE nombre LIKE %s OR apellidos LIKE %s OR fecha LIKE %s
        """
        data = (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
        cursor.execute(search_query, data)
        records = cursor.fetchall()
        cursor.close()
    else:
        cursor = conn.cursor()
        select_query = "SELECT id, nombre, apellidos, correo, telefono, Fecha, nombre_cabana, fecha_de_salida, precio  FROM reservaciones"
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        return render_template("ADreservar.html", records=records)

    conn.close()

@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    conn = connect_to_database()
    if not conn:
        return "Error de conexión a la base de datos"

    if request.method == "POST":
        keyword = request.form["keyword"]
        cursor = conn.cursor()
        search_query = """
            SELECT id, nombre, apellidos, correo, telefono, Fecha, nombre_cabana, fecha_de_salida, precio
            FROM reservaciones
            WHERE nombre LIKE %s OR apellidos LIKE %s OR fecha LIKE %s
        """
        data = (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
        cursor.execute(search_query, data)
        records = cursor.fetchall()
        cursor.close()
        return render_template("ADreservar.html", records=records)
    return render_template('ADreservar.html')


@app.route("/insert", methods=["POST"])
def insert_record():
    conn = connect_to_database()
    if not conn:
        return "Error de conexión a la base de datos"

    cursor = conn.cursor()
    insert_query = """
        INSERT INTO reservaciones (nombre, apellidos, correo, telefono, Fecha, nombre_cabana , fecha_de_salida, precio)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (request.form["nombre"], request.form["apellidos"], request.form["correo"], request.form["telefono"], request.form["Fecha"], request.form["nombre_cabana"], request.form["fecha_de_salida"], request.form["precio"] )
    cursor.execute(insert_query, data)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("show_records"))

@app.route("/update/<int:record_id>", methods=["POST"])
def update_record(record_id):
    conn = connect_to_database()
    if not conn:
        return "Error de conexión a la base de datos"

    cursor = conn.cursor()
    update_query = """
        UPDATE reservaciones
        SET nombre = %s, apellidos = %s, correo = %s, telefono = %s, Fecha = %s, nombre_cabana = %s, fecha_de_salida = %s, precio = %s
        WHERE id = %s
    """
    data = (request.form["nombre"], request.form["apellidos"], request.form["correo"], request.form["telefono"], request.form["Fecha"], request.form["nombre_cabana"], request.form["fecha_de_salida"], request.form["precio"], record_id)
    cursor.execute(update_query, data)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("show_records"))

@app.route("/delete/<int:record_id>", methods=["POST"])
def delete_record(record_id):
    conn = connect_to_database()
    if not conn:
        return "Error de conexión a la base de datos"

    cursor = conn.cursor()
    delete_query = "DELETE FROM reservaciones WHERE id = %s"
    cursor.execute(delete_query, (record_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("show_records"))

#/ADreservar/#

#/login/#

@app.route('/acceso-login', methods=["GET", "POST"])
def login():

    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword':
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']
        _password_hash = hashlib.sha512(_password.encode()).hexdigest()

        
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)        
        cursor.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s',(_correo,_password,))
        account = cursor.fetchone()
        cursor.close()
        conn.close()

        if account:
            session['logueado'] = True
            session['id'] = account['id']

            return redirect(url_for("admin"))
        else:

            return render_template('login.html', mensaje="Ingrese los datos / correctos. ")
    return render_template('login.html')

#/login/#


#/validacion/FORMULARIO/#

class ReservaForm(Form):
    nombre = StringField('Nombre', [validators.InputRequired(), validators.Regexp(r'^[^0-9]*$', message="No se permiten números en el nombre")])
    apellidos = StringField('Apellidos', [validators.InputRequired(), validators.Regexp(r'^[^0-9]*$', message="No se permiten números en los apellidos")])
    correo = StringField('Correo electrónico', [validators.InputRequired(), validators.Email()])
    telefono = StringField('Teléfono', [
        validators.InputRequired(),
        validators.Regexp(r'^\+?[0-9]*$', message="Número de teléfono inválido"),
        validators.Length(min=10, max=12, message="El número de teléfono debe tener entre 10 y 12 dígitos")
    ])
    fecha = StringField('Fecha de reserva', [validators.InputRequired()])
    nombre_cabana = HiddenField('Nombre de la cabaña')
    fecha_de_salida = StringField('Fecha de salida')
    precio = HiddenField('Precio', default=150)  # Establecer el valor del precio fijo


@app.route('/formulario', methods=['GET', 'POST'])
def reserva():
    form = ReservaForm(request.form)
    
    if request.method == 'POST' and form.validate():
        nombre = form.nombre.data
        apellidos = form.apellidos.data
        correo = form.correo.data
        telefono = form.telefono.data
        fecha = form.fecha.data
        nombre_cabana = form.nombre_cabana.data
        fecha_de_salida = form.fecha_de_salida.data
        precio = form.precio.data

        # Validar que la fecha no sea anterior a la fecha actual
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        if fecha < fecha_actual:
            form.fecha.errors.append("La fecha de reserva no puede ser anterior a la fecha actual.")
            return render_template('formulario.html', form=form)

        # Conectar a la base de datos y realizar la inserción
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insertar los datos en la base de datos
        insert_query = "INSERT INTO reservaciones (nombre, apellidos, correo, telefono, fecha, nombre_cabana, fecha_de_salida, precio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (nombre, apellidos, correo, telefono, fecha, nombre_cabana , fecha_de_salida, precio)
        cursor.execute(insert_query, data)
        connection.commit()

        # Cerrar la conexión a la base de datos
        cursor.close()
        connection.close()
        
        # Generar el PDF
        pdf = generate_pdf(nombre, apellidos, correo, telefono, fecha, nombre_cabana, fecha_de_salida, precio)
        
        # Enviar el PDF como respuesta de descarga
        return send_pdf(pdf)

    return render_template('formulario.html', form=form)

def generate_pdf(nombre, apellidos, correo, telefono, fecha, nombre_cabana, fecha_de_salida, precio):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.alignment = TA_CENTER
    title = Paragraph("Reservacion Exitosa:comprobante.", title_style)
    elements.append(title)

    details_style = ParagraphStyle(
        "details",
        parent=styles['Normal'],
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    details = [
        f"<b>Nombre de la cabaña:</b> {nombre_cabana}",
        f"<b>Nombre:</b> {nombre}",
        f"<b>Apellidos:</b> {apellidos}",
        f"<b>Correo electrónico:</b> {correo}",
        f"<b>Teléfono:</b> {telefono}",
        f"<b>Fecha de reserva:</b> {fecha}",
        f"<b>Fecha de salida:</b> {fecha_de_salida}",
        f"<b>Precio:</b> {precio}",
        f"<b>Políticas Generales del Establecimiento</b>",
        f"<b>1. Toda persona que entre a su cabaña en calidad de huésped, tiene la obligación de registrarse en recepción por cada cabaña (en excepción de no tener previa reservación).</b>",
        f"<b>2. Toda persona titular o a cargo de su cabaña tiene la obligación de cubir cualquier desperfecto que cause o cargo adicional que se realice, está obligado a cubrir el costo.</b>",
        f"<b>3. La hora de entrega de la cabaña es a las 3:00 P.M.</b>",
        f"<b>4. La hora de la salida de la cabaña es a las 12:00 P.M. en caso de hacer un CHECK OUT posterior al acordado se cobrará una tarifa adicional. a menos que notifique a recepción y sea autorizado a prolongar su estancia sin costo.</b>",
        f"<b>5. El cobro de la cabaña se genera a partir de la entrega de la misma.</b>",
        f"<b>6. Usted tiene el derecho de revisar la cabaña con anterioridad a su registro o pago y aclarar cualquier inconformidad, de lo contrario queda obligado a cubrir el pago total de la misma, según la tarifa acordada antes de hacer la reservación.</b>",
        f"<b>7. Le llegara a su correo el metodo de pago para cubrir su reservacion. Si el pago no se llega a realizar en un lapso de 3 horas se cancelara la reservacion, favor de realizar su pago a tiempo.</b>",
    ]

    for detail in details:
        elements.append(Paragraph(detail, details_style))

    # Agregar un botón para regresar a la página /reservar
    return_button = Paragraph('<a href="/reservar">Toque aqui para regresar..</a>', styles['Normal'])
    elements.append(Spacer(1, 20))
    elements.append(return_button)

    doc.build(elements)
    buffer.seek(0)
    return buffer

def send_pdf(pdf):
    response = Response(pdf.read(), content_type='application/pdf')
    response.headers['Content-Disposition'] = 'inline; filename=reservacion.pdf'
    return response

#/formulario/#

#/Estadisticas/

@app.route('/Estadisticas')
def Estadisticas():
        # Consulta SQL para obtener las fechas de reservaciones
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT fecha FROM reservaciones")
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        # Procesar los resultados usando pandas
        data = pd.DataFrame(results, columns=['fecha'])

        # Convertir la columna 'fecha' al formato datetime
        data['fecha'] = pd.to_datetime(data['fecha'])

        # Contar las reservaciones por día
        reservations_per_day = data['fecha'].value_counts().sort_index()

        # Crear la gráfica
        plt.figure(figsize=(11, 6))
        reservations_per_day.plot(kind='bar')
        plt.title('Reservaciones por día')
        plt.xlabel('Fecha')
        plt.ylabel('Cantidad de Reservaciones')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Convertir la gráfica en una imagen base64 para mostrar en HTML
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode()

        # Renderizar la plantilla HTML y pasar la imagen base64
        return render_template('Estadisticas.html', graph=img_base64)

#/Estadisticas/#

#/html/#

@app.route("/inicio/")
def inicio():
    return render_template("inicio.html")

@app.route("/reservar/")
def reservar():
    return render_template("reservar.html")

@app.route("/admin/")
def admin():
    return render_template("admin.html")

@app.route("/ADusuarios/")
def ADusuarios():
    return render_template("ADusuarios.html")

@app.route("/ADcabañas/")
def ADcabañas():
    return render_template("ADcabañas.html")

@app.route("/ADreservar/")
def ADreservar():
    return render_template("ADreservar.html")

#/html/#

if __name__ == "__main__":
            app.secret_key="Marina"
            app.run(debug=True)