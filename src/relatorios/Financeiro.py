# funções que consultam o banco de dados local

from datetime import datetime
import calendar
import numpy

import config
import util
from relatorios import relatorio_pdf as pdf
import conta_corrente as conta
from database.DatabaseReader import DatabaseReader
from relatorios.Recebimentos import Recebimentos
from relatorios.Pagamentos import Pagamentos


class Financeiro:
    '''Classe responsável pelos cálculos financeiros.'''

    def __init__(self, date):
        self.date = date
        self.recebimentos = Recebimentos(date)
        self.pagamentos = Pagamentos(date)
        self.saldo_mensal = numpy.add(
            self.recebimentos.mensal, self.pagamentos.mensal).tolist()
        self.saldo_diario = numpy.add(
            self.recebimentos.diario, self.pagamentos.diario).tolist()

    def saldo_mes(self, elements):
        '''Retorna o saldo do mês separado por dia.'''

        saldo = numpy.add(
            self.recebimentos.diario, self.pagamentos.diario).tolist()

        if self.date.month == 1:
            saldo_conta = conta.sicredi[self.date.year]
        else:
            saldo_conta = conta.sicredi[self.date.year] + \
                numpy.sum(self.saldo_mensal[0:self.date.month-1])
        print("saldo_conta--->>>", saldo_conta)

        title = 'Resumo - Mês - ' + \
            str(self.date.month) + '/' + str(self.date.year)
        header = ['Receita', 'Despesa', 'Saldo Mes', 'Saldo Conta']
        firstcolumn = ['', 'Atual', 'Futuro', 'Total']

        dia_de_hoje = datetime.today().day
        mes_corrente = self.date.month
        qdte_dias_mes = calendar.monthrange(self.date.year, self.date.month)[1]
        values = [
            [  # hoje
                numpy.sum(self.recebimentos.diario[0:dia_de_hoje]),
                numpy.sum(self.pagamentos.diario[0:dia_de_hoje]),
                numpy.sum(saldo[0:dia_de_hoje]),
                saldo_conta + numpy.sum(saldo[0:dia_de_hoje])
            ],
            [  # futuro
                numpy.sum(self.recebimentos.diario[dia_de_hoje:qdte_dias_mes]),
                numpy.sum(self.pagamentos.diario[dia_de_hoje:qdte_dias_mes]),
                numpy.sum(saldo[dia_de_hoje:qdte_dias_mes]),
                saldo_conta + numpy.sum(saldo[0:qdte_dias_mes])
            ],
            [  # total
                numpy.sum(self.recebimentos.diario),
                numpy.sum(self.pagamentos.diario),
                numpy.sum(saldo),
                saldo_conta + numpy.sum(saldo[0:qdte_dias_mes])
            ]
        ]

        table = pdf.generate_table(title, header, firstcolumn, values)
        elements.append(table)

        title = 'Diário - ' + str(self.date.month) + '/' + str(self.date.year)
        header = ['Receita', 'Despesa', 'Saldo Dia', 'Saldo Conta']
        # firstcolumn that will be inserted
        qdte_dias_mes = calendar.monthrange(self.date.year, self.date.month)[1]
        first_column = ['Dia']
        for i in range(1, qdte_dias_mes+1):
            first_column.append(str(i))

        # matrix values
        saldo_por_mes = []
        saldo_atual = saldo_conta
        for i in range(0, qdte_dias_mes):
            saldo_atual += saldo[i]
            saldo_por_mes.append(saldo_atual)

        values = numpy.array([self.recebimentos.diario, self.pagamentos.diario,
                              saldo, saldo_por_mes]).T.tolist()

        table = pdf.generate_table(title, header, first_column, values)
        elements.append(table)

        pdf.addSpace(elements)

    def saldo_ano(self, elements):

        saldo = numpy.add(
            self.recebimentos.mensal, self.pagamentos.mensal).tolist()

        title = 'Resumo - Ano - ' + str(self.date.year)
        header = ['Receita', 'Despesa', 'Saldo Ano', 'Saldo Conta']

        monthNumber = self.date.month
        numberOfMonths = 12
        firstcolumn = ['', 'Final Mês', 'Futuro', 'Final do Ano']
        values = [
            [  # hoje
                numpy.sum(self.recebimentos.mensal[0:monthNumber]),
                numpy.sum(self.pagamentos.mensal[0:monthNumber]),
                numpy.sum(saldo[0:monthNumber]),
                conta.sicredi[self.date.year] + \
                numpy.sum(saldo[0:monthNumber])
            ],
            [  # futuro
                numpy.sum(
                    self.recebimentos.mensal[monthNumber:numberOfMonths]),
                numpy.sum(self.pagamentos.mensal[monthNumber:numberOfMonths]),
                numpy.sum(saldo[monthNumber:numberOfMonths]),
                conta.sicredi[self.date.year]+numpy.sum(saldo)
            ],
            [  # total
                numpy.sum(self.recebimentos.mensal),
                numpy.sum(self.pagamentos.mensal),
                numpy.sum(saldo),
                conta.sicredi[self.date.year]+numpy.sum(saldo)
            ]
        ]

        t = pdf.generate_table(title, header, firstcolumn, values)
        elements.append(t)

        year = str(self.date.year)
        title = 'Mensal - ' + year
        header = ['Receita', 'Despesa', 'Saldo Mes', 'Saldo Conta']
        firstcolumn = ['Mês', 'Jan/'+year, 'Fev/'+year, 'Mar/'+year, 'Abr/'+year, 'Mai/'+year, 'Jun/'+year,
                       'Jul/'+year, 'Ago/'+year, 'Set/'+year, 'Out/'+year, 'Nov/'+year, 'Dez/'+year]

        saldo_mes = conta.sicredi[self.date.year]
        saldo_em_conta = []
        for i in range(0, 12):
            saldo_mes = saldo_mes + saldo[i]
            saldo_em_conta.append(saldo_mes)

        values = numpy.array([self.recebimentos.mensal, self.pagamentos.mensal,
                              saldo, saldo_em_conta]).T.tolist()

        t = pdf.generate_table(title, header, firstcolumn, values)
        elements.append(t)

        pdf.addSpace(elements)

    def isBikeFinanceiro(self, produto):
        if(produto.find('BICICLETA') != -1):
            if(produto.find(' SENSE') != -1 or produto.find(' TSW') != -1 or produto.find(' RAVA') != -1 or produto.find(' NATHOR') != -1
                    or produto.find(' SPECIALIZED') != -1) or produto.find(' KSW') != -1 or produto.find(' FKS') != -1 or produto.find(' CALOI') != -1:
                return True
        elif(produto.find('BIC') != -1):
            if(produto.find('TSW') != -1):
                return True

        return False

    def getRecebimentosBicicletasProdutosServicosPecas(self, date):

        recebimentos = {}
        recebimentos['Bicicletas'] = [0]*12
        recebimentos['Produtos'] = [0]*12
        recebimentos['Peças'] = [0]*12
        recebimentos['Serviços'] = [0]*12
        bd_vendas = DatabaseReader().vendas(date.year)
        for item in bd_vendas:

            situacao = item['nome_situacao']
            pagamentos = item['pagamentos']
            valor_total = item['valor_total']
            if(situacao == 'Concretizada' and valor_total != '0.00' and len(pagamentos) != 0):

                date_time = datetime.strptime(item['data'], '%Y-%m-%d')
                if(date_time.year != date.year):
                    continue

                if 'produtos' in item:
                    for produto in item['produtos']:
                        if(self.isBikeFinanceiro(produto['produto']['nome_produto'])):
                            # print('##BIKE##',produto['produto']['nome_produto'])
                            recebimentos['Bicicletas'][date_time.month -
                                                       1] += float(produto['produto']['valor_venda'])
                        else:
                            # print(produto['produto']['nome_produto'])
                            recebimentos['Produtos'][date_time.month -
                                                     1] += float(produto['produto']['valor_venda'])

        bd_recebimentos = DatabaseReader().recebimentos(date.year)
        for item in bd_recebimentos:
            categoria = item['nome_plano_conta']

            if(item['data_liquidacao'] == None or categoria == 'Ajuste de caixa'):
                continue

            date_time = datetime.strptime(
                item['data_liquidacao'], '%Y-%m-%d')
            if(date_time.year != date.year):
                continue

            if categoria == 'Vendas no balcão':
                recebimentos['Produtos'][date_time.month -
                                         1] += float(item['valor_total'])

        bd_ordens = DatabaseReader().ordens_servicos(date.year)
        for item in bd_ordens:

            situacao = item['nome_situacao']
            pagamentos = item['pagamentos']
            valor_total = item['valor_total']
            if(situacao == 'Concretizada' and valor_total != '0.00' and len(pagamentos) != 0):

                servicos = item['valor_servicos']

                date_time = datetime.strptime(
                    item['data_entrada'], '%Y-%m-%d')
                if(date_time.year != date.year):
                    continue

                if 'produtos' in item:
                    for produto in item['produtos']:
                        if(self.isBikeFinanceiro(produto['produto']['nome_produto'])):
                            recebimentos['Bicicletas'][date_time.month -
                                                       1] += float(produto['produto']['valor_venda'])
                        else:
                            recebimentos['Peças'][date_time.month -
                                                  1] += float(produto['produto']['valor_venda'])

                if 'servicos' in item:
                    for servicos in item['servicos']:
                        recebimentos['Serviços'][date_time.month -
                                                 1] += float(servicos['servico']['valor_venda'])

        bicicletas = {}
        bicicletas['Bicicletas'] = recebimentos['Bicicletas']
        bicicletas['Outros (Produtos + Serviços)'] = numpy.add(numpy.add(
            recebimentos['Produtos'], recebimentos['Peças']), recebimentos['Serviços']).tolist()

        servicos = {}
        servicos['Peças'] = recebimentos['Peças']
        servicos['Serviços'] = recebimentos['Serviços']

        return bicicletas, servicos, recebimentos

    def gen_graph(self, elements, detalhamento, date, filename):
        header = []
        for categoria in detalhamento:
            header.append(categoria)

        year = str(date.year)
        title = 'Detalhamento da Receita - Ano - ' + year
        firstcolumn = ['Mês', 'Jan/'+year, 'Fev/'+year, 'Mar/'+year, 'Abr/'+year, 'Mai/'+year, 'Jun/'+year,
                       'Jul/'+year, 'Ago/'+year, 'Set/'+year, 'Out/'+year, 'Nov/'+year, 'Dez/'+year]

        values = []
        for categoria in detalhamento:
            values.append(detalhamento[categoria])

        values = numpy.array(values).T.tolist()

        t = pdf.generate_table(title, header, firstcolumn, values)
        elements.append(t)

        pdf.generate_graph(detalhamento, date.month, filename)
        from reportlab.platypus import Image
        im = Image('img/'+filename+'.png', 450, 300)
        elements.append(im)

    def detalha_receita(self, elements, date):
        dirFile = config.outputdir + str(date.year)
        util.create_output_dir(dirFile)

        bicicletas, servicos, todos = self.getRecebimentosBicicletasProdutosServicosPecas(
            date)
        self.gen_graph(elements, bicicletas, date, 'Bicicletas')
        self.gen_graph(elements, servicos, date, 'Serviços')
        self.gen_graph(elements, todos, date, 'Todos')

        pdf.addSpace(elements)
