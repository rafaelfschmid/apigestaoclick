#funções que geram um banco de dados local

from urllib.request import Request, urlopen
from datetime import datetime
import json
import util
import config


def create_database(functName, year = ''):
	if(year == ''):
		dirFiles=config.databasedir+functName+'/'
	else:
		dirFiles=config.databasedir + year + '/'+ functName +'/'
	
	util.create_output_dir(dirFiles)

	getLink = functName+'?data_inicio=' + year + '-01-01&limit=100&pagina='
	string = util.string_response(getLink + '1')

	filename= dirFiles + 'page.'
	pageName = filename + '1.db'
	util.removing_existing_file(pageName)
	print("Creating file: " + pageName)
	f = open(pageName, 'w')
	f.write(string)
	
	json_obj = json.loads(string)
	paginas = json_obj['meta']['total_paginas']
	#print(paginas)
	for pag in range(2, paginas+1):
		string = util.string_response(getLink + str(pag))
		pageName = filename + str(pag) + '.db'
		print(pageName)
		util.removing_existing_file(pageName)
		print("Creating file: " + pageName)
		f = open(pageName, 'w')
		f.write(string)

