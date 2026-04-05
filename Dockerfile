FROM python:3.11-slim

WORKDIR /src/app

COPY engine/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY engine/ .

EXPOSE 5050

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5050", "--workers", "1", "--threads", "2", "--timeout", "120"]