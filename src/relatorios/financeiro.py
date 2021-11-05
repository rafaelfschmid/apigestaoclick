# funções que consultam o banco de dados local

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
from database.DatabaseReader import DatabaseReader


def taxa_operadora(year):
    dirFile = config.outputdir + year
    util.create_output_dir(dirFile)

    # Ignora as categorias abaixo
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
        # print(json_obj)

        for item in json_obj['data']:
            categoria = item['nome_forma_pagamento']
            if(categoria not in ignore):
                if(item['data_liquidacao'] != None):
                    date_time = datetime.strptime(
                        item['data_liquidacao'], '%Y-%m-%d')

                    if(date_time.DatabaseReaderyear >= int(year)):
                        if(date_time.year not in years):
                            years.append(date_time.year)

                        if(categoria not in recebimentos):
                            recebimentos[categoria] = {}

                        if(date_time.year not in recebimentos[categoria]):
                            recebimentos[categoria][date_time.year] = []
                            for i in range(0, 12):
                                recebimentos[categoria][date_time.year].append(
                                    0.0)

                        recebimentos[categoria][date_time.year][date_time.month -
                                                                1] += float(item['taxa_operadora'])


def getRecebimentosCategoria(date):

    recebimentos = {}

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

            if categoria not in recebimentos:
                recebimentos[categoria] = [0]*12

            recebimentos[categoria][date_time.month -
                                    1] += float(item['valor_total'])

    return recebimentos
