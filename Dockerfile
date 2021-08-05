FROM python:3.8.5

WORKDIR /app

COPY requirements.txt ./

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/app.py"]