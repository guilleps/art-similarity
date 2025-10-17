# Service-cnn

### Structure
```
📁service-cnn/
└── 📁app/
    ├── __init__.py
    ├── cloudinary_config.py
    ├── logger_config.py
    ├── main.py          # FastAPI app / endpoints
    ├── model_vgg.py     # Truncated VGG-19 + classifier
├── .python-version     # 3.10.0
├── README.md
└── requirements.txt
```

### Design summary
- Language: Python 3.10.0
- Dependencies installed via pip (requirements.txt)
- Model: PyTorch with truncated VGG-19 (features[:15]). The head (fully connected) is replaced by a classifier with 2 outputs.
- No Gram matrices or Gram-based losses are used; there are no special convolutional techniques beyond VGG-19.

### Quick installation
1. Create an environment (pyenv/venv/conda) with Python 3.10.0.
2. pip install -r requirements.txt

### Run locally
- With Uvicorn (from the app directory):
```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Operational notes
- Adjust paths and parameters in app/main.py according to deployment.
- Set environment variables used in cloudinary_config.py and logger_config.py before running (e.g., CLOUDINARY_URL, LOG_LEVEL).
- As a persistent practice, separate inference logic and ingestion to ease scaling.

---

# Service-transform

### Structure
```
service-transform/
└── app/
    ├── __init__.py
    ├── cloudinary_config.py
    ├── logger_config.py
    ├── main.py                 # FastAPI app / endpoints
    ├── transformation_core.py  # core operations
    └── utils_transformations.py
├── .python-version
├── Dockerfile
├── docker-compose.yml
├── README.md
└── requirements.txt
```

### Design summary
- Language: Python 3.10.0
- Dependencies via pip
- Main library: OpenCV (cv2) for reading/transforming/writing images
- Clear separation: transformation_core contains the main logic; utils_transformations groups utilities

### Quick installation
1. Create an environment with Python 3.10.0.
2. pip install -r requirements.txt

### Run locally
- With Uvicorn (from the app directory):
```
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

### Operational notes
- Check and correct __init__.py filenames if necessary.
- Verify handling of large files (streaming / temporary files) to avoid excessive memory usage.
- Configure environment variables required for cloudinary/storage if external uploads are used.
