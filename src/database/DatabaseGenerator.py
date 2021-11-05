# funções que geram um banco de dados local

import json
import util
import config


class DatabaseGenerator:
    '''Classe responsavel por acessar o BD do gestaoclick e atualizar as bases de dados.'''

    def create_database(self, funct_name, year=''):
        '''Função genérica de uso da api do gestaoclick.'''
        if(year == ''):
            dir_files = config.databasedir+funct_name+'/'
            get_link = funct_name+'?limit=100&pagina='
        else:
            dir_files = config.databasedir + year + '/' + funct_name + '/'
            get_link = funct_name+'?data_inicio=' + year + '-01-01&limit=100&pagina='

        util.create_output_dir(dir_files)
        string = util.string_response(get_link + '1')

        filename = dir_files + 'page.'
        page_name = filename + '1.db'
        util.removing_existing_file(page_name)
        print("Creating file: " + page_name)
        f = open(page_name, 'w')
        f.write(string)

        json_obj = json.loads(string)
        paginas = json_obj['meta']['total_paginas']
        # print(paginas)
        for pag in range(2, paginas+1):
            string = util.string_response(get_link + str(pag))
            page_name = filename + str(pag) + '.db'
            print(page_name)
            util.removing_existing_file(page_name)
            print("Creating file: " + page_name)
            f = open(page_name, 'w')
            f.write(string)

    def produtos(self):
        '''Cria/atualiza a base de dados de produtos.'''
        self.create_database('produtos')

    def vendas(self, year=''):
        '''Cria/atualiza a base de dados de vendas.'''
        self.create_database('vendas', year)

    def pagamentos(self, year=''):
        '''Cria/atualiza a base de dados de pagamentos.'''
        self.create_database('pagamentos', year)

    def recebimentos(self, year=''):
        '''Cria/atualiza a base de dados de recebimentos.'''
        self.create_database('recebimentos', year)

    def ordens_servicos(self, year=''):
        '''Cria/atualiza a base de dados de ordens de servicos.'''
        self.create_database('ordens_servicos', year)
