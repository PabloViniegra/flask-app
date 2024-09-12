# Flask Client REST API

Este proyecto es una API RESTful construida con Flask, Flask-Smorest, SQLAlchemy, y Marshmallow, diseñada para gestionar usuarios y direcciones. La API proporciona endpoints para la creación, lectura, actualización y eliminación (CRUD) de usuarios y direcciones, y está documentada con Swagger.

## Requisitos

- Python 3.x
- [pip](https://pip.pypa.io/en/stable/) - Administrador de paquetes de Python

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

### 2. Crear un entorno virtual

Es recomendable crear un entorno virtual para aislar las dependencias del proyecto.

```bash
python -m venv venv
```

### 3. Activar entorno virtual

- En Windows:
  ```
  venv\Scripts\activate
  ```
- En Linux:
  ```
  source venv/bin/activate
  ```

### 4. Instalar dependencias

Las dependencias del proyecto están especificadas en el archivo requirements.txt. Para instalarlas, ejecuta el siguiente comando:

```
pip install -r requirements.txt
```

### 5. Base de Datos

El proyecto utiliza SQLite como base de datos por defecto. No es necesario hacer ninguna configuración adicional para el entorno de desarrollo. Si deseas usar otra base de datos, puedes configurar la URL de la base de datos en el archivo .flaskenv o pasando el parámetro db_url al iniciar la aplicación.




