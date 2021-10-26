#funções que consultam o banco de dados local

from datetime import datetime
import json
import config
import util
import printer
import os

def getproductsMap():
	filename = 'estoque.in'
	print("Reading file: " + filename)
	f = open(filename)

	lines = f.readlines()
	f.close()

	mapFile = {}
	i = 1
	while (i < len(lines)):
		values=lines[i].split('\t')
		i = i+1
		if(len(values) > 1):
			name = values[0]
			maxValue = int(values[1])
			
			if name in mapFile:
				print('ERROR: Duplicate products in estoque.in.\n'+name)
			mapFile[name] = maxValue

	return mapFile

def lista_compras():
	#generate_database.create_database('produtos')

	dirFile = config.outputdir
	util.create_output_dir(dirFile)
	
	mapProducts = getproductsMap() 

	filename= dirFile+'/comprar.txt'
	util.removing_existing_file(filename)
	print("Creating file: " + filename)
	f = open(filename, 'w')
	f.write(str(datetime.now()) + '\n')

	listaDeCompras = {}	
	entries = os.scandir(config.databasedir + 'produtos')
	for entry in entries:
		if(not entry.is_file()):
			continue

		if(not entry.name.endswith('.db')):
			continue

		json_obj = util.parser_file(entry.path)
	
		for item in json_obj['data']:
			produto = item['nome']
			if(produto in mapProducts):
				estoqueQtde = int(mapProducts[produto])
				curQtde = int(item['estoque'])
				if(curQtde < estoqueQtde):
					comprar = estoqueQtde - curQtde
					f.write(produto + '\t' + str(comprar) + '\n')

	f.close()

def valor_em_estoque():
	#generate_database.create_database('produtos')

	dirFile = config.outputdir
	util.create_output_dir(dirFile)
	
	mapProducts = getproductsMap() 

	filename= dirFile+'/valor_em_estoque.txt'
	print("Creating file: " + filename)
	f = open(filename, 'a')
	#f.write('Data' + '\t' + 'Valor_Custo' + '\t' + 'Valor_Venda' + '\n')
	valor_custo = 0
	valor_venda = 0
	entries = os.scandir(config.databasedir + 'produtos')
	for entry in entries:
		if(not entry.is_file()):
			continue

		if(not entry.name.endswith('.db')):
			continue

		json_obj = util.parser_file(entry.path)
	
		for item in json_obj['data']:
			curQtde = int(item['estoque'])
			valor_custo += (float(item['valor_custo'])*curQtde)
			valor_venda += (float(item['valor_venda'])*curQtde)
		
	f.write(str(datetime.now()) + '\t' + str(valor_custo) + '\t' + str(valor_venda) + '\n')
	f.close()

def isBike(produto):
	if(produto.find('BICICLETA') != -1):
		if(produto.find(' SENSE') != -1 or produto.find(' TSW') != -1 or produto.find(' RAVA') != -1 or produto.find(' NATHOR') != -1):
			return True
	elif(produto.find('BIC') != -1):
		if(produto.find('TSW') != -1):
			return True

	return False

def lista_bicicletas():
	#generate_database.create_database('produtos')

	dirFile = config.outputdir
	util.create_output_dir(dirFile)

	filename= dirFile+'/bicicletas.txt'
	util.removing_existing_file(filename)
	print("Creating file: " + filename)
	f = open(filename, 'w')
	f.write(str(datetime.now()) + '\n')

	listaDeBikes = {}	
	entries = os.scandir(config.databasedir + 'produtos')
	for entry in entries:
		if(not entry.is_file()):
			continue

		if(not entry.name.endswith('.db')):
			continue

		json_obj = util.parser_file(entry.path)
	
		for item in json_obj['data']:
			produto = item['nome']
			if(isBike(produto)): # and (produto.find('SENSE') or produto.find('TSW') or produto.find('RAVA') or produto.find('NATHOR')) or (produto.find('BIC') and produto.find('TSW'))):
				qtde = int(item['estoque'])
				if(qtde != 0.0):
					f.write(produto + '\t' + str(qtde) + '\n')
	f.close()

