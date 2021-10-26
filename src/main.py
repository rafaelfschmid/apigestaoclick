from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate

from relatorios import financeiro
from relatorios import estoque
from relatorios import vendas

import generate_database
from datetime import datetime

def pdf_financeiro(date):
	filename = 'Relatorio-Anual-'+ str(date.year) +'.pdf'
	doc = SimpleDocTemplate(filename, pagesize=letter)
	print("Creating file: " + filename)
	elements = []

	financeiro.saldo_mes(elements, date)
	financeiro.saldo_ano(elements, date)
	#financeiro.taxa_operadora(year)
	# write the document to disk
	doc.build(elements)

def generate_databases(year):
	generate_database.create_database('pagamentos', year)
	generate_database.create_database('recebimentos', year)
	#generate_database.create_database('ordens_servicos', year)
	generate_database.create_database('produtos')


if __name__ == '__main__':
	date = datetime.today()
	#hoje = datetime.strptime('2021-10-11', '%Y-%m-%d')
#	year = '2021'
#	month = '10'
	
	generate_databases(str(date.year))	

	pdf_financeiro(date)
	estoque.valor_em_estoque()
	#estoque.lista_compras()
	#estoque.lista_bicicletas()
	#vendas.consulta_servicos_sem_pagamento(year)
	#vendas.atualiza_servicos_sem_pagamento(year)
	#vendas.consulta_vendas_sem_pagamento(year)	