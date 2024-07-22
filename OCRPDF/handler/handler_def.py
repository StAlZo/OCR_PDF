from io import BytesIO

import PyPDF2
# Для анализа структуры PDF и извлечения текста
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
# Для извлечения текста из таблиц в PDF
import pdfplumber
# Для извлечения изображений из PDF
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes
# Для выполнения OCR, чтобы извлекать тексты из изображений
import pytesseract
# Для удаления дополнительно созданных файлов
import os


def text_extraction(element):
    # Извлекаем текст из вложенного текстового элемента
    line_text = element.get_text()

    # Находим форматы текста
    # Инициализируем список со всеми форматами, встречающимися в строке текста
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            # Итеративно обходим каждый символ в строке текста
            for character in text_line:
                if isinstance(character, LTChar):
                    # Добавляем к символу название шрифта
                    line_formats.append(character.fontname)
                    # Добавляем к символу размер шрифта
                    line_formats.append(character.size)
    # Находим уникальные размеры и названия шрифтов в строке
    format_per_line = list(set(line_formats))

    # Возвращаем кортеж с текстом в каждой строке вместе с его форматом
    return (line_text, format_per_line)


def crop_image(element, pageObj):
    # Получаем координаты для вырезания изображения из PDF
    [image_left, image_top, image_right, image_bottom] = [element.x0, element.y0, element.x1, element.y1]
    # Обрезаем страницу по координатам (left, bottom, right, top)
    pageObj.mediabox.lower_left = (image_left, image_bottom)
    pageObj.mediabox.upper_right = (image_right, image_top)
    # Создаем буфер BytesIO для сохранения PDF
    cropped_pdf_buffer = BytesIO()
    # Сохраняем обрезанную страницу в новый PDF
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(pageObj)
    # Записываем PDF в буфер
    cropped_pdf_writer.write(cropped_pdf_buffer)
    # Сбрасываем указатель в начало буфера
    cropped_pdf_buffer.seek(0)
    return cropped_pdf_buffer


# Создаём функцию для преобразования PDF в изображения
def convert_to_images(cropped_pdf_buffer):
    # Преобразуем буфер PDF в изображения
    images = convert_from_bytes(cropped_pdf_buffer.read())
    # Получаем первое изображение из списка
    image = images[0]
    # Создаем буфер BytesIO для сохранения PNG изображения
    png_image_buffer = BytesIO()
    # Сохраняем изображение в формате PNG в буфер
    image.save(png_image_buffer, format='PNG')
    # Сбрасываем указатель чтения/записи в начало буфера
    png_image_buffer.seek(0)
    return png_image_buffer


# Создаём функцию для считывания текста из изображений
def image_to_text(image_path):
    image_path.seek(0)
    # Считываем изображение
    img = Image.open(image_path)
    # Извлекаем текст из изображения
    text = pytesseract.image_to_string(img, lang="rus", config='--psm 6')
    return text


# Извлечение таблиц из страницы

def extract_table(pdf_path, page_num, table_num):
    # Открываем файл pdf
    pdf = pdfplumber.open(pdf_path)
    # Находим исследуемую страницу
    table_page = pdf.pages[page_num]
    # Извлекаем соответствующую таблицу
    table = table_page.extract_tables()[table_num]
    return table


# Преобразуем таблицу в соответствующий формат
def table_converter(table):
    table_string = ''
    # Итеративно обходим каждую строку в таблице
    for row_num in range(len(table)):
        row = table[row_num]
        # Удаляем разрыв строки из текста с переносом
        cleaned_row = [
            item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item
            in row]
        # Преобразуем таблицу в строку
        table_string += ('|' + '|'.join(cleaned_row) + '|' + '\n')
    # Удаляем последний разрыв строки
    table_string = table_string[:-1]
    return table_string
