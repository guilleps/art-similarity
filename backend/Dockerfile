# imagen oficial de python
FROM python:3.13 

# establecer el directio app (aqui se almacena todo)
RUN mkdir /app

# insertamos el directorio dentro del contenedor
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
