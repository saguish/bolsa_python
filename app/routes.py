from flask import Flask, render_template, url_for
import sys
sys.path.append('C:\\Users\\sergi\\Documents\\projetos\\bolsa_python\\virtual\\app')

import models.TradesDAO
import models.vendasDAO
from controller import controller

app = Flask(__name__)


@app.route('/')
def index():
    pass
    return render_template('base.html')

@app.route('/apurar')
def apurar():
    pagina, dados = controller.render(controller.controller_apurar())
    return render_template(pagina, dados=dados)

@app.route('/show/<tabela_a_mostrar>')
def show(tabela_a_mostrar):
    pagina, dados = controller.render(controller.controller_consultar(tabela_a_mostrar))
    return render_template(pagina, dados=dados)

app.run(debug=True)

