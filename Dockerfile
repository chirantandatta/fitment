FROM python:3.6-slim
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 2000
ENTRYPOINT FLASK_APP=app.py python -m flask run --host=0.0.0.0 --port=2000