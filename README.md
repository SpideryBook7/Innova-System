# 🏡 Innova System - Cabañas "El Despertar"

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)
![SQLite](https://img.shields.io/badge/SQLite-Integrated-lightgrey.svg)

**Innova System** es una plataforma web integral para la gestión de reservaciones de cabañas turísticas. Diseñada para facilitar la administración del negocio y ofrecer una experiencia de reserva fluida a los clientes.

---

## ✨ Características Principales

### 🌟 Portal Público
*   **Catálogo de Cabañas**: Vistas detalladas de las cabañas disponibles (Bonita, Golosa, Consentida, etc.) con galerías de imágenes.
*   **Formulario de Reservación**: Interfaz moderna y amigable para realizar reservas, con validación de datos en tiempo real.
*   **Generación de PDF**: Creación automática de comprobantes de reserva en formato PDF descargable.

### 🛡️ Panel Administrativo (BaaS)
*   **Dashboard**: Vista general con accesos rápidos a las funciones principales.
*   **Gestión de Reservas (CRUD)**:
    *   Visualización de todas las reservas en una tabla responsiva.
    *   Edición de datos "in-line" (directamente en la tabla).
    *   Eliminación y creación de nuevos registros.
*   **Seguridad**: Autenticación de administradores protegida por sesiones y hash de contraseñas.
*   **Estadísticas**: Gráficos generados con `Matplotlib` para visualizar la ocupación y tendencias de reserva.

---

## 🛠️ Tecnologías Utilizadas

*   **Backend**: Python (Flask)
*   **Base de Datos**: SQLite (Migrado de MySQL para portabilidad)
*   **Frontend**: HTML5, CSS3, Bootstrap 5 (Glassmorphism UI)
*   **Librerías Clave**:
    *   `pandas` & `matplotlib`: Análisis de datos y gráficos.
    *   `reportlab`: Generación de PDFs.
    *   `wtforms`: Manejo y validación de formularios.
    *   `gunicorn`: Servidor de producción WSGI.

---

## 🚀 Instalación y Uso Local

1.  **Clonar el repositorio**:
    ```bash
    git clone https://github.com/SpideryBook7/innova-system.git
    cd innova-system
    ```

2.  **Crear entorno virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicializar Base de Datos**:
    Este script creará el archivo `database.db` y un usuario administrador por defecto.
    ```bash
    python init_db.py
    ```
    *Credenciales por defecto:*
    *   User: `admin@innova.com`
    *   Pass: `admin`

5.  **Ejecutar la aplicación**:
    ```bash
    python app/app.py
    ```
    Visita `http://127.0.0.1:5000/` en tu navegador.

---

## ☁️ Despliegue (Deployment)

Este proyecto está configurado para desplegarse fácilmente en servicios como **Render**.

### Pasos para desplegar en Render (Gratis):

1.  Sube tu código a **GitHub**.
2.  Crea una cuenta en [Render.com](https://render.com/).
3.  Selecciona **"New Web Service"** y conecta tu repositorio.
4.  Configuración:
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn app.app:app`
5.  En la sección **Advanced** (opcional pero recomendado), añade una variable de entorno:
    *   `PYTHON_VERSION`: `3.11.0` (o la versión que uses).
6.  ¡Desplegar! 🚀

---
**Desarrollado por Cristian Huerta - 2023**
