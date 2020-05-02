from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo
import models.TradesDAO, models.vendasDAO

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/bolsa"
mongo = PyMongo(app)


@app.route('/')
def index():
    pass

    return render_template('base.html')

@app.route('/apurar/<modalidade>')
def apurar(modalidade):
    """
    funcao para realizar a apuração de resultados da modalidade escolhida: swingtrade ou daytrade
    :return:
    """
    pass
    return render_template('apurar.html', modal=modalidade)

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

