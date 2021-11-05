'''Processa os relatórios do gestaoclick.'''
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate

from relatorios import financeiro
from relatorios.Financeiro import Financeiro
from relatorios import estoque
from relatorios import vendas

from database.DatabaseGenerator import DatabaseGenerator


def pdf_financeiro(date):
    filename = 'Relatorio-Anual-' + str(date.year) + '.pdf'
    doc = SimpleDocTemplate(filename, pagesize=letter)
    print("Creating file: " + filename)
    elements = []

    finan = Financeiro(date)
    finan.saldo_mes(elements)
    finan.saldo_ano(elements)
    finan.detalha_receita(elements, date)
    # financeiro.taxa_operadora(year)
    # write the document to disk
    doc.build(elements)


def generate_databases(year):
    db = DatabaseGenerator()
    db.pagamentos(year)
    db.recebimentos(year)
    db.ordens_servicos(year)
    db.vendas(year)
    db.produtos()


if __name__ == '__main__':
    import sys
    print(sys.path)

    date = datetime.today()
    #date = datetime.strptime('2021-10-31', '%Y-%m-%d')

    # generate_databases(str(date.year))

    pdf_financeiro(date)
    # estoque.valor_em_estoque()

    # estoque.lista_compras()
    # estoque.lista_bicicletas()
    vendas.consulta_servicos_sem_pagamento(str(date.year))
    # vendas.atualiza_servicos_sem_pagamento(year)
    vendas.consulta_vendas_sem_pagamento(str(date.year))
