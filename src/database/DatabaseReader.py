# funções que geram um banco de dados local

from urllib.request import Request, urlopen
from datetime import datetime
import os
import json
import util
import config


class DatabaseReader:
    '''Classe responsável por ler e fazer o parser dos arquivos gerados pelo DatabaseGenerator.'''

    def scan_dir(self, dir_files):
        '''Funcao responsável por ler e fazer o parser dos arquivos gerados pelo DatabaseGenerator.'''

        entries = os.scandir(dir_files)
        vec = []
        for entry in entries:
            if not entry.is_file():
                continue

            if not entry.name.endswith('.db'):
                continue

            json_obj = util.parser_file(entry.path)

            vec.extend(json_obj['data'])

        return vec

    def produtos(self):
        '''Retorna todos os produtos da base de dados.'''
        dir_files = config.databasedir + '/produtos'
        return self.scan_dir(dir_files)

    def vendas(self, year):
        '''Retorna todas as vendas da base de dados.'''
        dir_files = config.databasedir + str(year) + '/vendas'
        return self.scan_dir(dir_files)

    def pagamentos(self, year):
        '''Retorna todos os pagamentos da base de dados.'''
        dir_files = config.databasedir + str(year) + '/pagamentos'
        return self.scan_dir(dir_files)

    def recebimentos(self, year):
        '''Retorna todos os recebimentos da base de dados.'''
        dir_files = config.databasedir + str(year) + '/recebimentos'
        return self.scan_dir(dir_files)

    def ordens_servicos(self, year=''):
        '''Retorna todas as ordens de servicos da base de dados.'''
        dir_files = config.databasedir + str(year) + '/ordens_servicos'
        return self.scan_dir(dir_files)
