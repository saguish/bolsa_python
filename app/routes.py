from flask import Flask, render_template
import sys
sys.path.append('C:\\Users\\sergi\\Documents\\projetos\\bolsa_python\\virtual\\app')
from controller.controller import controller_apurar, controller_consultar, render_controller

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html')

@app.route('/apurar')
def apurar():
    pagina, dados = render_controller(controller_apurar())
    return render_template(pagina, dados=dados)

@app.route('/show/<tabela_a_mostrar>')
def show(tabela_a_mostrar):
    pagina, dados = render_controller(controller_consultar(tabela_a_mostrar))
    return render_template(pagina, dados=dados)

app.run(debug=True)

