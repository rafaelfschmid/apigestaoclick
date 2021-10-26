from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import numpy

def format_data(title, header, firstcolumn, values):
	titleLine = []
	titleLine.append(title)
	for i in range(len(header)-1):
		titleLine.append('')

	data = [titleLine, header]
	
	import locale
	locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')

	for row in values:
		data.append([locale.currency(v) for v in row])

	if(len(firstcolumn) > 0):
		firstcolumn.insert(0, title)
		print(firstcolumn)
		print(data)
		aux = numpy.array(data)
		data = numpy.insert(aux, 0, firstcolumn, axis=1).tolist()

	return data


def generate_table(title, header, firstcolumn, values):
	tStyle = TableStyle([
	('SPAN',(0,0),(-1,0)),	
	('ALIGN',(0,0),(-1,-1),'CENTER'),
	('VALIGN',(0,0),(-1,-1),'MIDDLE'),
	#cabecalho
	('BACKGROUND', (0, 0), (-1, 0), colors.gray),
	('BACKGROUND', (0, 1), (-1, 1), colors.darkgray),
	#valores
	('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
	('BOX', (0,0), (-1,-1), 0.25, colors.black),
	])

	# Loop through list of lists creating styles for cells with negative value.
	for row, elements, in enumerate(values):
	    for column, value in enumerate(elements):
	        if value < 0:
	        	tStyle.add('TEXTCOLOR', (column+1, row+2), (column+1, row+2), colors.red)

	data = format_data(title, header, firstcolumn, values)
	
	t=Table(data,len(data[0])*[1.2*inch], len(data)*[0.16*inch])
	t.setStyle(tStyle)
	
	return t

def addSpace(elements):
	# Adding space between two tables
	from reportlab.platypus import Table
	t=Table([['\n']])
	elements.append(t)