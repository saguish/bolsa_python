import sys
sys.path.append('C:\\Users\\sergi\\Documents\\projetos\\bolsa_python\\virtual\\app')

from config.config import conectaDB

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

def apuracao():
    try:
        conn = conectaDB()
        cur = conn.cursor()
        cur.execute("""SELECT SUM(valor_venda), competencia FROM VENDAS GROUP BY competencia ORDER BY competencia;""")
        results = cur.fetchall()
        return results

    except Exception as e:
        print(e)
