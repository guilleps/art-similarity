## Service Transform Documentation

### Prerrequisitos
Asegúrese de tener instalado lo siguiente en su sistema:
- Python 3.10
- pip (gestor de paquetes de Python)
- Una herramienta de entorno virtual (opcional pero recomendable)

### Instalacion
1. Crea y activa un entorno virtual (opcional):

    - **Windows**
      ```bash
      py -3.10 -m venv venv
      .\venv\Scripts\activate
      ```

    - **Linux/macOS**
      ```bash
      python3.10 -m venv venv
      source venv/bin/activate
      ```

    - **Linux (pyenv)**
      ```bash
      pyenv virtualenv 3.10 service_transform
      pyenv local service_transform
      pyenv activate service_transform
      ```

2. Instala dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```

### Ejecuta la aplicacion
1. Inicia el servidor:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
    ```

2. El servidor correrá en el puerto `http://127.0.0.1:8002` por defecto.