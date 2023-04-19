FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py main.py
RUN mkdir app_config
COPY app_config/ /app_config/
RUN echo '10.193.4.247 clickhouse.prod.edu' >> /etc/hosts

EXPOSE 9438

CMD ["python", "main.py"]