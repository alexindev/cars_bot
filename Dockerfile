FROM python:3.10-slim

WORKDIR app

COPY requirements.txt .

RUN apt update && apt upgrade -y \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
