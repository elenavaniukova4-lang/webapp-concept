FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Сначала копируем только requirements.txt (для кэширования зависимостей)
COPY todo-list/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем всё остальное
COPY . .

# Запускаем приложение
EXPOSE 5000
CMD ["python", "todo-list/app.py"]

