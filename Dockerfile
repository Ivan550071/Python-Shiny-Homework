FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x /app/start.sh

ENV APP_PATH=a4_ex1/app.py
EXPOSE 8000

ENTRYPOINT ["/app/start.sh"]
