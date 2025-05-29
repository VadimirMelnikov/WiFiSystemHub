FROM python:3.12

WORKDIR /app

#COPY requirements.txt .
#COPY src/. /

COPY . .

RUN ls -R /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt


# Открываем порт, на котором работает Flask
EXPOSE 5000

# Запускаем приложение
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.Controller:app"]