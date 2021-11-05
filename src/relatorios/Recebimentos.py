# funções que consultam o banco de dados local

from datetime import datetime
import calendar
from database.DatabaseReader import DatabaseReader


class Recebimentos:
    '''Classe responsável por armazenar os recebimentos.'''

    def __init__(self, date):
        number_of_days = calendar.monthrange(date.year, date.month)[1]
        self.diario = [0]*number_of_days  # recebimentos do mês por dia
        self.mensal = [0]*12  # recebimentos do ano por mês

        '''Retorna os recebimentos do mês separado por dia.'''
        bd_recebimentos = DatabaseReader().recebimentos(date.year)
        for item in bd_recebimentos:
            categoria = item['nome_plano_conta']
            if(item['data_liquidacao'] is None or categoria == 'Ajuste de caixa'):
                continue

            date_time = datetime.strptime(item['data_liquidacao'], '%Y-%m-%d')
            if(date_time.year == date.year):
                self.mensal[date_time.month-1] += float(item['valor_total'])

                if(date_time.month == date.month):
                    self.diario[date_time.day-1] += float(item['valor_total'])
