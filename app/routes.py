from flask import Flask, render_template, url_for
import sys
sys.path.append('C:\\Users\\sergi\\Documents\\projetos\\bolsa_python\\virtual\\app')

import models.TradesDAO
import models.vendasDAO

app = Flask(__name__)


@app.route('/')
def index():
    pass

    return render_template('base.html')

@app.route('/apurar')
def apurar():
    """
    funcao para realizar a apuração de resultados da modalidade escolhida: swingtrade ou daytrade
    :return:
    """
    dados = models.vendasDAO.apuracao()
    return render_template('apurar.html', dados=dados)

@app.route('/classificar')
def classificar():
    """
    funcao para organizar trades, classificandos como swingtrade e day trade
    e separando as operações daytrade em açoes, indice ou dolar
    :return:
    """
    pass
    return render_template('classificar.html')

@app.route('/editar')
def editar():
    """
    funcao para edição de trades, alterando ou excluindo dados
    :return:
    """
    pass
    return render_template('editar.html')

@app.route('/show/<tabela_a_mostrar>')
def show(tabela_a_mostrar):
    """
    funcao para mostra tabela
    :return:
    """
    if (str(tabela_a_mostrar) == 'trades'):
        trades = models.TradesDAO.get('SWINGTRADE')
        return render_template('showtrades.html',dados=trades)

    if (str(tabela_a_mostrar) == 'vendas'):
        vendas = models.vendasDAO.get()
        return render_template('showvendas.html',dados=vendas)

app.run(debug=True)

