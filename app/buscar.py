
import mysql.connector
import re



def validate_input(nombre, apellidos, telefono):
    if re.search(r'\d', nombre) or re.search(r'\d', apellidos):
        return "El nombre y los apellidos no deben contener números"

    if not telefono.isdigit():
        return "El teléfono debe contener solo números"

    return None
