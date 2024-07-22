FROM python:3.11
# Определяем переменные среды
# Чтобы python не создавал файлы .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Чтобы видеть выходные данные приложения в реальном времени
ENV PYTHONUNBUFFERED=1
# Устанавливаем рабочую директорию
WORKDIR ./OCRPDF
# Копируем в рабочую директорию файл зависимостей
COPY requirements.txt /OCRPDF/requirements.txt

# Обновляем pip, устанавливаем зависимости
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install gunicorn
RUN apt-get update && apt-get install -y poppler-utils
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-rus
#    groupadd -r stas && useradd -r -g stas stas && \
#    chsh -s /usr/sbin/nologin root
# делаем энрипоинт исполняймым



# Копируем содержимое локальной директории в рабочую директорию
COPY . /OCRPDF/

