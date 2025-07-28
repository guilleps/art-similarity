## Backend Documentacion

### Prerrequisitos
Asegúrese de tener instalado lo siguiente en su sistema:
- Python 3.10
- pip (gestor de paquetes de Python)
- Una herramienta de entorno virtual (opcional pero recomendable)

### Instalacion
1. Clone the repository:
    ```bash
    git clone https://github.com/guilleps/art-similarity.git
    cd tesis_project/backend
    ```

2. Crea y activdad un entorno virtual (opcional):
    ```bash
    py -3.10 -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. Instala dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```

### Ejecuta la aplicacion
1. Inicia el servidor:
    ```bash
    python manage.py runserver
    ```

2. El servidor correrá en el puerto `http://127.0.0.1:8000` por defecto.

### Estructura del proyecto
```
└── 📁backend
    └── 📁api
        └── 📁application
        └── 📁domain
            └── 📁models
        └── 📁infrastructure
            └── 📁config
            └── 📁exceptions
            └── 📁services
        └── 📁presentation
    └── 📁backend
    └── 📁tests
    └── .dockerignore
    └── .env
    └── .gitignore
    └── conftest.py
    └── db.sqlite3
    └── Dockerfile
    └── manage.py
    └── pytest.ini
    └── README.md
    └── requirements.txt
```

### API Endpoints
La documentación de los endpoints de la API está disponible automáticamente al ejecutar el backend. Puedes acceder a ella en los siguientes enlaces:

- **Swagger UI**: [http://127.0.0.1:8000/api/docs/swagger/](http://127.0.0.1:8000/api/docs/swagger/) - Interfaz interactiva para explorar y probar los endpoints.

Asegúrate de que el servidor esté corriendo para poder acceder a estas herramientas.

### Testing
Ejectua las pruebas:
```bash
pytest
```

### Notas
- Asegúrese de que la base de datos (si procede) está correctamente configurada antes de ejecutar la aplicación.
- Actualice el archivo `.env` con las variables de entorno necesarias.
- Y que los servicios de transformación y cnn estén en funcionamiento.
