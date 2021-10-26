#funções que consultam o banco de dados local

from datetime import datetime
import json
import config
import util
import printer
import os

import generate_database

def print_table_categoria_ano_mes(filename, map, years):
	util.removing_existing_file(filename)
	print("Creating file: " + filename)
	f = open(filename, 'w')

	years.sort()
	meses = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
	total = []
	for ano in years:
		for i in range(0, 12):
			f.write('\t' + meses[i] + '-' + str(ano))
			total.append(0.0)
	f.write('\n')

	for categoria in map:
		f.write(categoria)
		i = 0
		for ano in years:
			if(ano in map[categoria]):
				for valor in map[categoria][ano]:
					f.write('\t' + str("{:.2f}".format(valor)).replace('.', ','))
					total[i] += valor
					i += 1
		f.write('\n')
	
	f.write('Total')
	for valor in total:
		f.write('\t' + str("{:.2f}".format(valor)).replace('.', ','))
	f.write('\n')
	f.write('\n')

	f.close()

def consulta_vendas_sem_pagamento(year):
	generate_database.create_database('vendas', year)

	dirFile = config.outputdir
	util.create_output_dir(dirFile)

	filename = dirFile + 'vendas_sem_pagamento.txt'
	util.removing_existing_file(filename)
	print("Creating file: " + filename)
	f = open(filename, 'w')
	f.write('Cliente\tDt. Entrada\tValor')
	
	servicos = {}
	entries = os.scandir(config.databasedir + year + '/vendas')
	for entry in entries:
		if(not entry.is_file()):
			continue

		if(not entry.name.endswith('.db')):
			continue

		json_obj = util.parser_file(entry.path)
		#print(json_obj)
	
		for item in json_obj['data']:

			situacao = item['nome_situacao']
			pagamentos = item['pagamentos']
			valor_total = item['valor_total']

			if(situacao == 'Concretizada' and valor_total != '0.00' and len(pagamentos) == 0):
				os_id = item['id']
				data_entrada = item['data']
				nome_cliente = item['nome_cliente']
				valor_total = item['valor_total']
				f.write(nome_cliente + '\t' + data_entrada + '\t' + valor_total.replace('.', ','))
				f.write('\n')
	f.close()


def atualiza_vendas_sem_pagamento(year):
	generate_database.create_database('vendas', year)

	dirFile = config.outputdir
	util.create_output_dir(dirFile)

	filename = dirFile + 'vendas_sem_pagamento.txt'
	util.removing_existing_file(filename)
	print("Creating file: " + filename)
	f = open(filename, 'w')
	f.write('Cliente\tDt. Entrada\tValor')
	
	servicos = {}
	entries = os.scandir(config.databasedir + year + '/vendas')
	for entry in entries:
		if(not entry.is_file()):
			continue

		if(not entry.name.endswith('.db')):
			continue

		json_obj = util.parser_file(entry.path)
		#print(json_obj)
	
		for item in json_obj['data']:

			situacao = item['nome_situacao']
			pagamentos = item['pagamentos']
			valor_total = item['valor_total']
			if(situacao == 'Concretizada' and valor_total != '0.00' and len(pagamentos) == 0):
				#print(item)
				os_id = item['id']
				data_entrada = item['data_entrada']
				nome_cliente = item['nome_cliente']
				valor_total = item['valor_total']
				f.write(nome_cliente + '\t' + data_entrada + '\t' + valor_total.replace('.', ','))
				f.write('\n')
				item['situacao_id'] = '3596363'
				url = 'vendas/' + str(os_id)
				util.edit_tuple(url, item)

	f.close()



def consulta_servicos_sem_pagamento(year):
	generate_database.create_database('ordens_servicos', year)

	dirFile = config.outputdir
	util.create_output_dir(dirFile)

	filename = dirFile + 'servicos_sem_pagamento.txt'
	util.removing_existing_file(filename)
	print("Creating file: " + filename)
	f = open(filename, 'w')
	f.write('Cliente\tDt. Entrada\tValor')
	
	servicos = {}
	entries = os.scandir(config.databasedir + year + '/ordens_servicos')
	for entry in entries:
		if(not entry.is_file()):
			continue

		if(not entry.name.endswith('.db')):
			continue

		json_obj = util.parser_file(entry.path)
		#print(json_obj)
	
		for item in json_obj['data']:

			situacao = item['nome_situacao']
			pagamentos = item['pagamentos']
			valor_total = item['valor_total']
			if(situacao == 'Concretizada' and valor_total != '0.00' and len(pagamentos) == 0):
				#print(item)
				os_id = item['id']
				data_entrada = item['data_entrada']
				nome_cliente = item['nome_cliente']
				valor_total = item['valor_total']
				f.write(nome_cliente + '\t' + data_entrada + '\t' + valor_total.replace('.', ','))
				f.write('\n')
	f.close()


def atualiza_servicos_sem_pagamento(year):
	generate_database.create_database('ordens_servicos', year)

	dirFile = config.outputdir
	util.create_output_dir(dirFile)

	filename = dirFile + 'servicos_sem_pagamento.txt'
	util.removing_existing_file(filename)
	print("Creating file: " + filename)
	f = open(filename, 'w')
	f.write('Cliente\tDt. Entrada\tValor')
	
	servicos = {}
	entries = os.scandir(config.databasedir + year + '/ordens_servicos')
	for entry in entries:
		if(not entry.is_file()):
			continue

		if(not entry.name.endswith('.db')):
			continue

		json_obj = util.parser_file(entry.path)
		#print(json_obj)
	
		for item in json_obj['data']:

			situacao = item['nome_situacao']
			pagamentos = item['pagamentos']
			valor_total = item['valor_total']
			if(situacao == 'Concretizada' and valor_total != '0.00' and len(pagamentos) == 0):
				#print(item)
				os_id = item['id']
				data_entrada = item['data_entrada']
				nome_cliente = item['nome_cliente']
				valor_total = item['valor_total']
				f.write(nome_cliente + '\t' + data_entrada + '\t' + valor_total.replace('.', ','))
				f.write('\n')
				item['situacao_id'] = '3529586'
				
				url = 'ordens_servicos/' + str(os_id)
				util.edit_tuple(url, item)

	f.close()
