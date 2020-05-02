import psycopg2 # for database connection

# Database connection setup
t_host = "localhost"
t_port = "5432"
t_dbname = "bolsa"
t_user = "postgres"
t_pw = "postgres"

def conectaDB():
    # # Database connection setup
    # t_host = "localhost"
    # t_port = "5432"
    # t_dbname = "bolsa"
    # t_user = "postgres"
    # t_pw = "postgres"

    try:
        db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
        cur = db_conn.cursor()
        return cur
    except:
        print("nao conectei")


def get_datas_de_negociacoes():
    datas_de_negociacoes = []
    try:
        cur = conectaDB()
        cur.execute("""SELECT DISTINCT DATA FROM TRADES ORDER BY DATA;""")
        datas = cur.fetchall()

        for d in datas:
            datas_de_negociacoes.append(d[0])
        return datas_de_negociacoes

    except e:
        print(e)

def get_datas_de_negociacoes_modalidade_vazia():
    datas_de_negociacoes = []
    try:
        cur = conectaDB()
        cur.execute("""SELECT DISTINCT DATA FROM TRADES WHERE MODALIDADE IS NULL ORDER BY DATA;""")
        datas = cur.fetchall()

        for d in datas:
            datas_de_negociacoes.append(d[0])
        return datas_de_negociacoes

    except e:
        print(e)

def get_negociacoes_em(data_especifica):
    try:
        db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
        cur = db_conn.cursor()

        cur.execute(""" SELECT id, ativo, data, tipo_op, qtd
        from trades 
        where data =%s;
        """,[data_especifica,])
        results = cur.fetchall()

        return results
    except:
        print("erro no get negociacoes")


def avalia_modalidade2(negociacoes):
    ativos = {}
    ids_unicos = []

    #loop em busca de ativos unicos
    for n in negociacoes:
        if ( n[1] in ativos):
            ativos[n[1]] = False
        else:
            ativos[n[1]]=True

    #loop em anotando somente ativos unicos
    ativos_unicos = [a for a in ativos.keys() if ativos[a] == True]

    #segundo loop anotandos ids unicos
    for n in negociacoes:
        if n[1] in ativos_unicos:
            #print("em {} temos: {} com id: {} ".format(n[2],n[1],n[0]))
            ids_unicos.append(n[0])
    try:
        db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
        cur = db_conn.cursor()

        for i in ids_unicos:
            cur.execute("""UPDATE trades SET modalidade='SWINGTRADE' where modalidade is null and id=%s;""",[i,])
            print("update no id {}".format(i))
            db_conn.commit()

        cur.close()
        db_conn.close()
    except:
        print("erro no update")



def avalia_modalidade3(negociacoes):
    ativo_tipoOp = {}
    ativo_mesma_operacao = {}

    #primeiro loop
    for neg in negociacoes:

        #checa se vai entrar pela primeira vez
        if (not (neg[1] in ativo_tipoOp)):

            # infos do tipo ativo: compra /venda
            ativo_tipoOp[neg[1]] = neg[3]

            #infos do tipo ativo:True/False
            ativo_mesma_operacao[neg[1]] = True

        #se ja estava la checa se eh o mesmo tipoOp
        else:
            if (ativo_tipoOp[neg[1]] == neg[3]):
                ativo_mesma_operacao[neg[1]] = True
            else:
                ativo_mesma_operacao[neg[1]] = False


    #segundo loop
    ids_swing = []
    ids_day = []

    for neg in negociacoes:
        #se todas as operacoes do ativo em questao sao iguais
        if (ativo_mesma_operacao[neg[1]]):
            ids_swing.append(neg[0])
        else:
            ids_day.append(neg[0])

    #print("daytrades: {}".format(ids_day))
    #print("swingtrades: {}".format(ids_swing))

    try:
        db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
        cur = db_conn.cursor()

        for i in ids_swing:
            cur.execute("""UPDATE trades SET modalidade='SWINGTRADE' where modalidade is null and id=%s;""",[i,])
            db_conn.commit()

        for ix in ids_day:
            cur.execute("""UPDATE trades SET modalidade='DAYTRADE' where modalidade is null and id=%s;""", [ix, ])
            db_conn.commit()

        cur.close()
        db_conn.close()
    except:
        print("erro no update")


def inverte_sinal():
    ativo_tipoOp = {}
    ativo_mesma_operacao = {}

    try:
        db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
        cur = db_conn.cursor()

        cur.execute(""" SELECT id from trades_inv where tipo_op = 'venda' order by data; """)
        results = cur.fetchall()
        for r in results:
            print(r[0])
            cur.execute("""UPDATE trades_inv SET qtd=qtd*(-1) where tipo_op ='venda';""")
        cur.close()
        db_conn.close()
    except Exception as e:
        print(e)



# datas_modalidades_vazias = get_datas_de_negociacoes_modalidade_vazia()
#
# for data in datas_modalidades_vazias:
#     negociacoes_do_dia = get_negociacoes_em(data)
#     avalia_modalidade3(negociacoes_do_dia)

inverte_sinal()