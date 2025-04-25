# Uso de Python 3.12 en este Proyecto

Este proyecto utiliza **Python 3.12**. Puedes verificar la versión instalada ejecutando:

```bash
    python3 --version    
    python --version
```

> Instala `pip`, el gestor de paquetes de Python, si no está ya instalado.

## Instalación de Dependencias

1. Crea un entorno virtual para aislar las dependencias del proyecto:
    ```bash
    python -m venv venv
    ```

2. Activa el entorno virtual:
    - En **Linux/MacOS**:
      ```bash
      source venv/bin/activate
      ```
    - En **Windows**:
      ```bash
      .\venv\Scripts\activate
      ```

3. Instala las dependencias desde el archivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4. Verifica que las dependencias se hayan instalado correctamente:
    ```bash
    pip list
    ```