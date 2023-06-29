import pdfkit

pdfkit_config = pdfkit.configuration(wkhtmltopdf = r'../wkhtmltopdf/bin/wkhtmltopdf.exe')
pdfkit.from_file('foodOnline/templates/marketplace/random.html', 'foodOnline/templates/marketplace/random.pdf', configuration=pdfkit_config)