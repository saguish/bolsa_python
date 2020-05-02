import psycopg2 # for database connection

def conectaDB():
    # Database connection setup
    t_host = "localhost"
    t_port = "5432"
    t_dbname = "bolsa"
    t_user = "postgres"
    t_pw = "postgres"

    try:
        db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
        return db_conn
    except Exception as e:
        print(e)


def get_trades():

    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""SELECT * FROM TRADES ORDER BY DATA;""")
        datas = cur.fetchall()

        return datas

    except Exception as e:
        print(e)

def get_vendas():

    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""SELECT * FROM VENDAS ORDER BY DATA;""")
        vendas = cur.fetchall()

        return vendas

    except Exception as e:
        print(e)

def get_datas_de_negociacoes_modalidade_vazia():
    datas_de_negociacoes = []
    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""SELECT DISTINCT DATA FROM TRADES WHERE MODALIDADE IS NULL ORDER BY DATA;""")
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

def get_negociacoes_swingtrade():
    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute(""" SELECT * from trades where modalidade ='SWINGTRADE' ORDER BY data,tipo_op;""")
        results = cur.fetchall()
        return results

    except Exception as e:
        print(e)

def calcula_preco_medio_trade(trade):
    custos_transacao = sum(trade[8:13])
    qtd = trade[6]
    ticker = trade[4]
    preco = trade[7]
    preco_medio = (preco * qtd - custos_transacao)/qtd
    return [ticker,qtd,preco_medio]


def atualiza_posicao(trade):
    """
    funcao principal para atualizar tabela de vendas e tabela de posicao de ativos
    dentro dela, chama para calcular preço medio, atualizar vendas, atualizar posicao
    :param trade:
    :return:
    """
    # formato da posicao_trade: [ticker,qtd,preco_medio]
    posicao_trade = calcula_preco_medio_trade(trade)
    _ticker = posicao_trade[0]
    _qtd_trade = posicao_trade[1]
    _preco_med_trade = posicao_trade[2]

    _data_do_trade = trade[3]

    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""SELECT QTD, PRECO FROM POSICAO WHERE TICKER=%s """,[_ticker,])
        result = cur.fetchall()

        #se o ativo ainda nao estava na base
        if (result == []):
            cur.execute("""INSERT INTO POSICAO VALUES (%s,%s,%s) """,[_ticker,_qtd_trade,_preco_med_trade])
            conn.commit()
            cur.close()
            conn.close()

        else:
            posicao_antiga_qtd = result[0][0]
            posicao_antiga_preco = result[0][1]
            posicao_nova_qtd = _qtd_trade + posicao_antiga_qtd

            apurado_na_venda = 0
            """
            o preço medio so altera quando se adiciona uma compra
            se a quantidade zera, o preço tambem deve zerar
            """
            #se venda e quantidade nao zera
            if (_qtd_trade >= 0 and posicao_nova_qtd != 0):
                posicao_nova_preco = posicao_antiga_preco
                apurado_na_venda = (_preco_med_trade - posicao_antiga_preco)*_qtd_trade
                registra_apurado(_ticker,_data_do_trade,apurado_na_venda)

            #se venda e quantidade nao zera
            elif (_qtd_trade >= 0 and posicao_nova_qtd == 0):
                posicao_nova_preco = 0
                apurado_na_venda = (_preco_med_trade - posicao_antiga_preco) * _qtd_trade
                registra_apurado(_ticker, _data_do_trade, apurado_na_venda)

            #se compra
            elif (_qtd_trade < 0):
                monto = (_qtd_trade * _preco_med_trade) + (posicao_antiga_qtd*posicao_antiga_preco)

                posicao_nova_preco = monto / posicao_nova_qtd

            cur.execute("""UPDATE POSICAO SET QTD = %s, PRECO =%s WHERE TICKER=%s; """, [posicao_nova_qtd,posicao_nova_preco,_ticker])
            conn.commit()
            print("ativo ATUALIZADO na base")

    except Exception as e:
        print(e)

def registra_apurado(_ticker,_data, _valor):
    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""INSERT INTO VENDAS (ativo,data,valor_venda) VALUES (%s,%s,%s) """, [_ticker, _data, _valor])
        conn.commit()

    except Exception as e:
        print(e)

def atualiza_competencia(ultimo_dia,competencia):
    try:
        conn = conectaDB()
        cur = conn.cursor()
        #sql_update ="""UPDATE VENDAS SET COMPETENCIA = %s WHERE DATA < %s AND COMPETENCIA IS NULL;""".format(competencia,ultimo_dia)
        sql_update = """UPDATE VENDAS SET COMPETENCIA = %s WHERE DATA < %s AND COMPETENCIA IS NULL;"""
        cur.execute(sql_update,(competencia, ultimo_dia))
       #  cur.execute("""SELECT * FROM VENDAS WHERE COMPETENCIA is NULL and DATA < %s ;""",
       #              [ultimo_dia,])
        conn.commit()

    except Exception as e:
        print(e)

def teste():
    # pares = [
    #     ('2016-01-31', '2016-01-01'),
    #     ('2016-02-28', '2016-02-01'),
    #     ('2016-03-31', '2016-03-01'),
    #     ('2016-04-30', '2016-04-01'),
    #     ('2016-05-31', '2016-05-01'),
    #     ('2016-06-30', '2016-06-01'),
    #     ('2016-07-31', '2016-07-01'),
    #     ('2016-08-31', '2016-08-01'),
    #     ('2016-09-30', '2016-09-01'),
    #     ('2016-10-31', '2016-10-01'),
    #     ('2016-11-30', '2016-11-01'),
    #     ('2016-12-31', '2016-12-01'),
    #
    #     ('2017-01-31', '2017-01-01'),
    #     ('2017-02-28', '2017-02-01'),
    #     ('2017-03-31', '2017-03-01'),
    #     ('2017-04-30', '2017-04-01'),
    #     ('2017-05-31', '2017-05-01'),
    #     ('2017-06-30', '2017-06-01'),
    #     ('2017-07-31', '2017-07-01'),
    #     ('2017-08-31', '2017-08-01'),
    #     ('2017-09-30', '2017-09-01'),
    #     ('2017-10-31', '2017-10-01'),
    #     ('2017-11-30', '2017-11-01'),
    #     ('2017-12-31', '2017-12-01'),
    #
    #     ('2018-01-31', '2018-01-01'),
    #     ('2018-02-28', '2018-02-01'),
    #     ('2018-03-31', '2018-03-01'),
    #     ('2018-04-30', '2018-04-01'),
    #     ('2018-05-31', '2018-05-01'),
    #     ('2018-06-30', '2018-06-01'),
    #     ('2018-07-31', '2018-07-01'),
    #     ('2018-08-31', '2018-08-01'),
    #     ('2018-09-30', '2018-09-01'),
    #     ('2018-10-31', '2018-10-01'),
    #     ('2018-11-30', '2018-11-01'),
    #     ('2018-12-31', '2018-12-01'),
    #
    #     ('2019-01-31', '2019-01-01'),
    #     ('2019-02-28', '2019-02-01'),
    #     ('2019-03-31', '2019-03-01'),
    #     ('2019-04-30', '2019-04-01'),
    #     ('2019-05-31', '2019-05-01'),
    #     ('2019-06-30', '2019-06-01'),
    #     ('2019-07-31', '2019-07-01'),
    #     ('2019-08-31', '2019-08-01'),
    #     ('2019-09-30', '2019-09-01'),
    #     ('2019-10-31', '2019-10-01'),
    #     ('2019-11-30', '2019-11-01'),
    #     ('2019-12-31', '2019-12-01'),
    #
    #     ('2020-01-31', '2020-01-01'),
    #     ('2020-02-28', '2020-02-01'),
    #     ('2020-03-31', '2020-03-01'),
    #     ('2020-04-30', '2020-04-01'),
    #     ('2020-05-31', '2020-05-01'),
    #     ('2020-06-30', '2020-06-01'),
    #     ('2020-07-31', '2020-07-01'),
    #     ('2020-08-31', '2020-08-01'),
    #     ('2020-09-30', '2020-09-01'),
    #     ('2020-10-31', '2020-10-01'),
    #     ('2020-11-30', '2020-11-01'),
    #     ('2020-12-31', '2020-12-01')
    # ]
    #
    # for p in pares:
    #     atualiza_competencia(p[0],p[1])

    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute(""" SELECT * from trades WHERE MODALIDADE='SWINGTRADE' ORDER BY data,tipo_op;""")
        results = cur.fetchall()


        for result in results:
            atualiza_posicao(result)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    teste()
