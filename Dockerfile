FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["/app/main.py", "--fitfile", "/activity.fit", "--photo", "/photos"]