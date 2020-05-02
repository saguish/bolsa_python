import psycopg2
import TradesDAO

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


def get(_ticker):
    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""SELECT QTD, PRECO FROM POSICAO WHERE TICKER=%s;""",[_ticker,])
        result = cur.fetchall()

        return result
    except Exception as e:
        print(e)

def adiciona_na_posicao_e_retorna_venda(_trade):
    # formato da posicao_trade: [ticker,qtd,preco_medio]
    _preco_medio = TradesDAO.calcula_preco_medio_trade(_trade)
    _ticker = _trade[4]
    _qtd_trade = _trade[6]
    _data_do_trade = _trade[3]


    try:
        result = get(_trade[4])
        posicao_antiga_qtd = result[0][0]
        posicao_antiga_preco = result[0][1]
        posicao_nova_qtd = _qtd_trade + posicao_antiga_qtd

        # if (_trade[2]=='VENDA' and posicao_nova_qtd ==0):
        #     print("posicao nova {} trade id {}".format(posicao_nova_qtd,_trade[0]))

        apurado_na_venda = 0
        """
        o preço medio so altera quando se adiciona uma compra
        se a quantidade zera, o preço tambem deve zerar
        """

        #se venda e quantidade zera
        if (_qtd_trade >= 0 and posicao_nova_qtd == 0):
            valor_venda = (_preco_medio - posicao_antiga_preco) * _qtd_trade
            if (valor_venda == 0):
                print(_trade)
                print("preco medio da venda zerada {}".format(_preco_medio))
            posicao_nova_preco = 0

        # se venda
        elif (_qtd_trade >= 0):
            valor_venda = (_preco_medio - posicao_antiga_preco) * _qtd_trade
            posicao_nova_preco = posicao_antiga_preco

        #se compra
        elif (_qtd_trade < 0):
            monto = (_qtd_trade * _preco_medio) + (posicao_antiga_qtd*posicao_antiga_preco)
            posicao_nova_preco = monto / posicao_nova_qtd
            valor_venda = None

        #print("ativo: {} data {} posicao nova qtd {} valor_venda {}".format(_ticker,_data_do_trade,posicao_nova_qtd,valor_venda))

        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""UPDATE POSICAO SET QTD = %s, PRECO =%s WHERE TICKER=%s; """, [posicao_nova_qtd,posicao_nova_preco,_ticker])
        conn.commit()
        print("ativo ATUALIZADO na base")

        return valor_venda

    except Exception as e:
        print(e)


def save(_trade):
    _ticker = _trade[4]
    _qtd_trade = _trade[6]
    _preco_med_trade = TradesDAO.calcula_preco_medio_trade(_trade)

    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""INSERT INTO POSICAO VALUES (%s,%s,%s); """, [_ticker, _qtd_trade, _preco_med_trade])
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)

def clear_all():

    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""DELETE FROM POSICAO ;""")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)

def update(_ticker, posicao_nova_qtd, posicao_nova_preco):
    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""UPDATE POSICAO SET QTD = %s, PRECO =%s WHERE TICKER=%s; """,[posicao_nova_qtd, posicao_nova_preco, _ticker])
        conn.commit()
    except Exception as e:
        print(e)
