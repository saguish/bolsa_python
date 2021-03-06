import sys
sys.path.append('C:\\Users\\sergi\\Documents\\projetos\\bolsa_python\\virtual\\app')

from config.config import conectaDB

def get(modalidade, corretora = None):

    try:
        conn = conectaDB()
        cur = conn.cursor()
        if (corretora == None):
            cur.execute("""SELECT * FROM TRADES WHERE MODALIDADE=%s ORDER BY DATA,TIPO_OP;""",[modalidade,])
            trades = cur.fetchall()
        else:
            cur.execute("""SELECT * FROM TRADES WHERE MODALIDADE=%s and CORRETORA =%s ORDER BY DATA,TIPO_OP;""", [modalidade,corretora])
            trades = cur.fetchall()
        return trades

    except Exception as e:
        print(e)

def get_datas_de_negociacoes():
    datas_de_negociacoes = []
    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""SELECT DISTINCT DATA FROM TRADES ORDER BY DATA;""")
        datas = cur.fetchall()

        for d in datas:
            datas_de_negociacoes.append(d[0])
        return datas_de_negociacoes

    except Exception as e:
        print(e)

def get_negociacoes_em(data_especifica):
    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute(""" SELECT id, ativo, data, tipo_op, qtd from trades where data =%s;""",[data_especifica,])
        results = cur.fetchall()

        return results
    except Exception as e:
        print(e)

def save():
    pass

def delete():
    pass

def update():
    pass

def calcula_preco_medio_trade(trade):
    custos_transacao = sum(trade[8:13])
    qtd = trade[6]
    ticker = trade[4]
    preco = trade[7]
    preco_medio = (preco * qtd - custos_transacao)/qtd


    if (qtd == 0):
        print(trade)
    return preco_medio