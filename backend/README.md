## Documentation

This backend is implemented using a hexagonal (ports and adapters) architecture, organized into application, domain, infrastructure, and presentation layers.

### Prerequisites
Make sure the following are installed on your system:
- Python 3.10.0
- pip (Python package manager)
- A virtual environment tool (recommended)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/guilleps/art-similarity.git
    cd art-similarity/backend
    ```

2. Create and activate a virtual environment (optional but recommended):

    - Windows
      ```bash
      py -3.10 -m venv venv
      .\venv\Scripts\activate
      ```

    - Linux/macOS
      ```bash
      python3.10 -m venv venv
      source venv/bin/activate
      ```

    - Using pyenv
      ```bash
      pyenv install 3.10.0          # if not already installed
      pyenv virtualenv 3.10.0 backend
      pyenv local backend
      pyenv activate backend
      ```

3. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Run the application
1. Start the server:
    ```bash
    python manage.py runserver
    ```

2. By default the server will run at: http://127.0.0.1:8000

### Project structure
```
└── backend
    └── api
        └── application
        └── domain
            └── models
        └── infrastructure
            └── config
            └── exceptions
            └── services
        └── presentation
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── urls.py
    └── backend
        ├── __init__.py
        ├── asgi.py
        ├── settings.py
        ├── setup.py
        ├── urls.py
        ├── wsgi.py
    └── tests
    ├── .dockerignore
    ├── .env
    ├── .gitignore
    ├── .python-version
    ├── conftest.py
    ├── Dockerfile
    ├── manage.py
    ├── pytest.ini
    ├── README.md
    └── requirements.txt
```

### API Endpoints
API documentation is generated automatically when the backend is running. Access it at:

- Swagger UI: http://127.0.0.1:8000/api/docs/swagger/ — interactive interface to explore and test endpoints.

Make sure the server is running to use these tools.

### Testing
Run the test suite with:
```bash
pytest
```

### Notes
- Ensure the database (if used) is properly configured before running the application.
- Update the .env file with required environment variables.
- Confirm that any external services (e.g., transformation service and CNN service) are running and accessible.
- Run migrations if applicable:
```bash
python manage.py migrate
```
- For development, consider creating a .env.example with the minimal required variables.
