from handler import HandlerPDF

path = '/home/stas/PycharmProjects/OCRdemo/Пример_ТЗ_3.pdf'
h = HandlerPDF()
pdfFileObj = open(path, 'rb')
print(h.extrations_from_pdf(path))