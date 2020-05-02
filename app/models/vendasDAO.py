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

def get():

    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""SELECT * FROM VENDAS ORDER BY DATA;""")
        vendas = cur.fetchall()

        return vendas

    except Exception as e:
        print(e)


def clear_all():
    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""DELETE FROM VENDAS;""")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)

def save(_ticker,_data, _valor):
    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""INSERT INTO VENDAS (ativo,data,valor_venda) VALUES (%s,%s,%s);""", [_ticker, _data, _valor])
        conn.commit()

    except Exception as e:
        print(e)

def update(id, competencia):
    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""UPDATE VENDAS SET COMPETENCIA = %s WHERE ID=%s;""",[competencia,id])
        conn.commit()

    except Exception as e:
        print(e)

