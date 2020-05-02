import sys
sys.path.append('C:\\Users\\sergi\\Documents\\projetos\\bolsa_python\\virtual\\app')

import models.TradesDAO
import models.vendasDAO


def render(funcao,*param):
	pagina, dados = funcao
	return pagina, dados

def controller_apurar():
	dados = models.vendasDAO.apuracao()
	return ['apurar.html', dados]

def controller_consultar(tabela_a_mostrar):
	if (str(tabela_a_mostrar) == 'trades'):
		dados = models.TradesDAO.get('SWINGTRADE')
		return ['showtrades.html',dados]
	
	if (str(tabela_a_mostrar) == 'vendas'):
		dados = models.vendasDAO.get()
		return ['showvendas.html',dados]
