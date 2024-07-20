from handler import HandlerPDF

path = '/Пример_ТЗ_3.pdf'
h = HandlerPDF()
pdfFileObj = open(path, 'rb')
print(h.extrations_from_pdf(path))