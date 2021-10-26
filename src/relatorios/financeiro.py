#funções que consultam o banco de dados local

from datetime import datetime
import calendar
import json
import config
import util
import printer
import os
import numpy
from relatorios import relatorio_pdf as pdf
import conta_corrente as conta

def taxa_operadora(year):
	dirFile = config.outputdir + year
	util.create_output_dir(dirFile)
	
	#Ignora as categorias abaixo
	ignore = ['Transferência', 'Boleto Bancário', 'Cartão Inter', 'Débito Stone', 
	'Crédito Stone 2x a 6x', 'Débito Sicredi Pagamento']

	recebimentos = {}
	years = []
	entries = os.scandir(config.databasedir + year + '/recebimentos')
	for entry in entries:
		if(not entry.is_file()):
			continue

		if(not entry.name.endswith('.db')):
			continue

		json_obj = util.parser_file(entry.path)
		#print(json_obj)
	
		for item in json_obj['data']:
			categoria = item['nome_forma_pagamento']
			if(categoria not in ignore):
				if(item['data_liquidacao'] != None):
					date_time = datetime.strptime(item['data_liquidacao'], '%Y-%m-%d')

					if(date_time.year >= int(year)):
						if(date_time.year not in years):
							years.append(date_time.year)

						
						if(categoria not in recebimentos):
							recebimentos[categoria] = {}

						if(date_time.year not in recebimentos[categoria]):
							recebimentos[categoria][date_time.year] = []
							for i in range(0, 12):
								recebimentos[categoria][date_time.year].append(0.0)
					
						recebimentos[categoria][date_time.year][date_time.month-1] += float(item['taxa_operadora'])

	print_table_categoria_ano_mes(dirFile+'/taxa_operadora.csv', recebimentos, years)



def getRecebimentosDoMes(date):
	
	numberOfDays = calendar.monthrange(date.year, date.month)[1]
	recebimentos = [0]*numberOfDays

	entries = os.scandir(config.databasedir + str(date.year) + '/recebimentos')
	for entry in entries:
		if(not entry.is_file()):
			continue

		if(not entry.name.endswith('.db')):
			continue

		json_obj = util.parser_file(entry.path)
		for item in json_obj['data']:
			categoria = item['nome_plano_conta']
			if(item['data_liquidacao'] == None or categoria == 'Ajuste de caixa'):
				continue

			date_time = datetime.strptime(item['data_liquidacao'], '%Y-%m-%d')
			if(date_time.year != date.year or date_time.month != date.month):
				continue
			
			recebimentos[date_time.day-1] += float(item['valor_total'])

	return recebimentos


def getPagamentosDoMes(date):
	
	numberOfDays = calendar.monthrange(date.year, date.month)[1]
	pagamentos = [0]*numberOfDays

	entries = os.scandir(config.databasedir + str(date.year) + '/pagamentos')
	for entry in entries:
		if(not entry.is_file()):
			continue

		if(not entry.name.endswith('.db')):
			continue

		json_obj = util.parser_file(entry.path)
		for item in json_obj['data']:
			if(item['descricao'] == 'Transferência entre contas'):
				continue

			if (item['data_liquidacao'] == None):
				date_time = datetime.strptime(item['data_vencimento'], '%Y-%m-%d')
			else:
				date_time = datetime.strptime(item['data_liquidacao'], '%Y-%m-%d')
				
			if(date_time.year != date.year or date_time.month != date.month):
				continue
			
			pagamentos[date_time.day-1] -= float(item['valor_total'])

	return pagamentos

def saldo_mes(elements, date):
	dirFile = config.outputdir + str(date.year)
	util.create_output_dir(dirFile)
	saldo = {}
	years = []

	saldo['recebimentos'] = getRecebimentosDoMes(date)
	saldo['pagamentos'] = getPagamentosDoMes(date)
	saldo['saldo'] = numpy.add(saldo['recebimentos'],saldo['pagamentos']).tolist()

	title = 'Resumo - Mês - ' + str(date.month) + '/' + str(date.year)
	header = ['Receita', 'Despesa', 'Saldo Mes', 'Saldo Conta']
	firstcolumn = ['', 'Atual', 'Futuro', 'Total']
	
	diaDeHoje = datetime.today().day
	monthNumber = date.month
	numberOfDays = calendar.monthrange(date.year, date.month)[1]
	values = [
	[ #hoje
	numpy.sum(saldo['recebimentos'][0:diaDeHoje]),
	numpy.sum(saldo['pagamentos'][0:diaDeHoje]),
	numpy.sum(saldo['saldo'][0:diaDeHoje]),
	conta.sicredi[date.year][monthNumber]+numpy.sum(saldo['saldo'][0:diaDeHoje])
	],
	[ #futuro
	numpy.sum(saldo['recebimentos'][diaDeHoje:numberOfDays]),
	numpy.sum(saldo['pagamentos'][diaDeHoje:numberOfDays]),
	numpy.sum(saldo['saldo'][diaDeHoje:numberOfDays]),
	conta.sicredi[date.year][monthNumber]+numpy.sum(saldo['saldo'][diaDeHoje:numberOfDays])
	],
	[ #total
	numpy.sum(saldo['recebimentos']), 
	numpy.sum(saldo['pagamentos']),
	numpy.sum(saldo['saldo']),
	conta.sicredi[date.year][monthNumber]+numpy.sum(saldo['saldo'])
	]
	]

	t = pdf.generate_table(title, header, firstcolumn, values)
	elements.append(t)

	title = 'Diário - ' + str(date.month) + '/' + str(date.year)
	header = ['Receita', 'Despesa', 'Saldo Dia', 'Saldo Conta']
	#firstcolumn that will be inserted
	numberOfDays = calendar.monthrange(date.year, date.month)[1]
	firstcolumn = ['Dia']
	[firstcolumn.append(str(i)) for i in range(1, numberOfDays+1)]
	
	#matrix values
	saldo_em_conta = []
	saldoEmConta = conta.sicredi[date.year][date.month]
	for i in range(0,numberOfDays):
		saldoEmConta += saldo['saldo'][i]
		saldo_em_conta.append(saldoEmConta)

	values = numpy.array([saldo['recebimentos'],saldo['pagamentos'],saldo['saldo'], saldo_em_conta]).T.tolist()

	t = pdf.generate_table(title, header, firstcolumn, values)
	elements.append(t)

	pdf.addSpace(elements)


def getRecebimentosDoAno(date):
	
	recebimentos = [0]*12

	entries = os.scandir(config.databasedir + str(date.year) + '/recebimentos')
	for entry in entries:
		if(not entry.is_file()):
			continue

		if(not entry.name.endswith('.db')):
			continue

		json_obj = util.parser_file(entry.path)
		for item in json_obj['data']:
			categoria = item['nome_plano_conta']
			if(item['data_liquidacao'] == None or categoria == 'Ajuste de caixa'):
				continue

			date_time = datetime.strptime(item['data_liquidacao'], '%Y-%m-%d')
			if(date_time.year != date.year):
				continue
			
			recebimentos[date_time.month-1] += float(item['valor_total'])

	return recebimentos


def getPagamentosDoAno(date):
	
	pagamentos = [0]*12

	entries = os.scandir(config.databasedir + str(date.year) + '/pagamentos')
	for entry in entries:
		if(not entry.is_file()):
			continue

		if(not entry.name.endswith('.db')):
			continue

		json_obj = util.parser_file(entry.path)
		for item in json_obj['data']:
			if(item['descricao'] == 'Transferência entre contas'):
				continue

			if (item['data_liquidacao'] == None):
				date_time = datetime.strptime(item['data_vencimento'], '%Y-%m-%d')
			else:
				date_time = datetime.strptime(item['data_liquidacao'], '%Y-%m-%d')
			if(date_time.year != date.year):
				continue
			
			pagamentos[date_time.month-1] -= float(item['valor_total'])

	return pagamentos


def saldo_ano(elements, date):
	dirFile = config.outputdir + str(date.year)
	util.create_output_dir(dirFile)
	saldo = {}
	years = []

	saldo['recebimentos'] = getRecebimentosDoAno(date)
	saldo['pagamentos'] = getPagamentosDoAno(date)
	saldo['saldo'] = numpy.add(saldo['recebimentos'],saldo['pagamentos']).tolist()

	title = 'Resumo - Ano - ' + str(date.year)
	header = ['Receita', 'Despesa', 'Saldo Ano', 'Saldo Conta']

	monthNumber = date.month
	numberOfMonths = 12
	firstcolumn = ['', 'Final Mês', 'Futuro', 'Final do Ano']
	values = [
	[ #hoje
	numpy.sum(saldo['recebimentos'][0:monthNumber]),
	numpy.sum(saldo['pagamentos'][0:monthNumber]),
	numpy.sum(saldo['saldo'][0:monthNumber]),
	conta.sicredi[date.year][1]+numpy.sum(saldo['saldo'][0:monthNumber])
	],
	[ #futuro
	numpy.sum(saldo['recebimentos'][monthNumber:numberOfMonths]),
	numpy.sum(saldo['pagamentos'][monthNumber:numberOfMonths]),
	numpy.sum(saldo['saldo'][monthNumber:numberOfMonths]),
	conta.sicredi[date.year][1]+numpy.sum(saldo['saldo'][monthNumber-1:numberOfMonths])
	],
	[ #total
	numpy.sum(saldo['recebimentos']), 
	numpy.sum(saldo['pagamentos']),
	numpy.sum(saldo['saldo']),
	conta.sicredi[date.year][1]+numpy.sum(saldo['saldo'])
	]
	]

	t = pdf.generate_table(title, header, firstcolumn, values)
	elements.append(t)

	year = str(date.year)
	title = 'Mensal - ' + year
	header = ['Receita', 'Despesa', 'Saldo Mes', 'Saldo Conta']
	firstcolumn = ['Mês','Jan/'+year,'Fev/'+year,'Mar/'+year,'Abr/'+year,'Mai/'+year,'Jun/'+year,
	'Jul/'+year,'Ago/'+year,'Set/'+year,'Out/'+year,'Nov/'+year,'Dez/'+year ]

	saldo_em_conta = []
	for i in range(0,12):
		saldo_em_conta.append(conta.sicredi[date.year][i+1] + saldo['saldo'][i])

	values = numpy.array([saldo['recebimentos'],saldo['pagamentos'],saldo['saldo'],saldo_em_conta]).T.tolist()

	t = pdf.generate_table(title, header, firstcolumn, values)
	elements.append(t)

	pdf.addSpace(elements)



def getRecebimentosDoAno(date):
	
	recebimentos = [0]*12
	len(recebimentos)

	entries = os.scandir(config.databasedir + str(date.year) + '/recebimentos')
	for entry in entries:
		if(not entry.is_file()):
			continue

		if(not entry.name.endswith('.db')):
			continue

		json_obj = util.parser_file(entry.path)
		for item in json_obj['data']:
			categoria = item['nome_plano_conta']
			if(item['data_liquidacao'] == None or categoria == 'Ajuste de caixa'):
				continue

			date_time = datetime.strptime(item['data_liquidacao'], '%Y-%m-%d')
			if(date_time.year != date.year):
				continue
			
			recebimentos[date_time.month-1] += float(item['valor_total'])

	return recebimentos


def getPagamentosDoAno(date):
	
	pagamentos = [0]*12

	entries = os.scandir(config.databasedir + str(date.year) + '/pagamentos')
	for entry in entries:
		if(not entry.is_file()):
			continue

		if(not entry.name.endswith('.db')):
			continue

		json_obj = util.parser_file(entry.path)
		for item in json_obj['data']:
			if(item['descricao'] == 'Transferência entre contas'):
				continue

			if (item['data_liquidacao'] == None):
				date_time = datetime.strptime(item['data_vencimento'], '%Y-%m-%d')
			else:
				date_time = datetime.strptime(item['data_liquidacao'], '%Y-%m-%d')
			if(date_time.year != date.year):
				continue
			
			pagamentos[date_time.month-1] -= float(item['valor_total'])

	return pagamentos


def saldo_ano(elements, date):
	dirFile = config.outputdir + str(date.year)
	util.create_output_dir(dirFile)
	saldo = {}
	years = []

	saldo['recebimentos'] = getRecebimentosDoAno(date)
	saldo['pagamentos'] = getPagamentosDoAno(date)
	saldo['saldo'] = numpy.add(saldo['recebimentos'],saldo['pagamentos']).tolist()

	title = 'Resumo - Ano - ' + str(date.year)
	header = ['Receita', 'Despesa', 'Saldo Ano', 'Saldo Conta']

	monthNumber = date.month
	numberOfMonths = 12
	firstcolumn = ['', 'Final Mês', 'Futuro', 'Final do Ano']
	values = [
	[ #hoje
	numpy.sum(saldo['recebimentos'][0:monthNumber]),
	numpy.sum(saldo['pagamentos'][0:monthNumber]),
	numpy.sum(saldo['saldo'][0:monthNumber]),
	conta.sicredi[date.year][1]+numpy.sum(saldo['saldo'][0:monthNumber])
	],
	[ #futuro
	numpy.sum(saldo['recebimentos'][monthNumber:numberOfMonths]),
	numpy.sum(saldo['pagamentos'][monthNumber:numberOfMonths]),
	numpy.sum(saldo['saldo'][monthNumber:numberOfMonths]),
	conta.sicredi[date.year][1]+numpy.sum(saldo['saldo'][monthNumber-1:numberOfMonths])
	],
	[ #total
	numpy.sum(saldo['recebimentos']), 
	numpy.sum(saldo['pagamentos']),
	numpy.sum(saldo['saldo']),
	conta.sicredi[date.year][1]+numpy.sum(saldo['saldo'])
	]
	]

	t = pdf.generate_table(title, header, firstcolumn, values)
	elements.append(t)

	year = str(date.year)
	title = 'Mensal - ' + year
	header = ['Receita', 'Despesa', 'Saldo Mes', 'Saldo Conta']
	firstcolumn = ['Mês','Jan/'+year,'Fev/'+year,'Mar/'+year,'Abr/'+year,'Mai/'+year,'Jun/'+year,
	'Jul/'+year,'Ago/'+year,'Set/'+year,'Out/'+year,'Nov/'+year,'Dez/'+year ]

	saldo_em_conta = []
	for i in range(0,12):
		saldo_em_conta.append(conta.sicredi[date.year][i+1] + saldo['saldo'][i])

	values = numpy.array([saldo['recebimentos'],saldo['pagamentos'],saldo['saldo'],saldo_em_conta]).T.tolist()

	t = pdf.generate_table(title, header, firstcolumn, values)
	elements.append(t)

	pdf.addSpace(elements)