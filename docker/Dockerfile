FROM python:3.11.4-slim
LABEL authors="Serghei.D"

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src /app/

COPY docker/entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh