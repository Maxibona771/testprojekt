FROM python:3.11-slim
WORKDIR /app

# Копируем зависимости отдельно
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

EXPOSE 5000
CMD ["sh", "-c", "python migrate.py && python importer.py"]
