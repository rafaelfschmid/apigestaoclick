

def ordens_servico(ordens):
	for os in ordens:
		print(os['nome_cliente'])
		print(os['data_entrada'])
		print(os['data_saida'])
		print(os['nome_situacao'])
		print(os['valor_servicos'])
		print(os['valor_produtos'])
		print(os['valor_total'])
		print(os['condicao_pagamento'])
		separador = "==================================================="
		print(separador)

def recebimentos(receb):
	for os in receb:
		print(os['nome_cliente'])
		print(os['nome_plano_conta'])
		print(os['plano_contas_id'])
		print(os['data_vencimento'])
		print(os['valor_total'])
		print(os['taxa_operadora'])
		separador = "==================================================="
		print(separador)
