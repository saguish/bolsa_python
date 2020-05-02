import TradesDAO, vendasDAO, posicaoDAO



def insere(self):
    pass

def apura_venda(self):

    pass

def avalia_modalidade(self):
    pass

def prepara_dados():
    """
    sequencia de passos:
        avalia modalidade, setando swingtrade ou daytrade

        """
    vendasDAO.clear_all()
    posicaoDAO.clear_all()

    all_trades_swingtrades = TradesDAO.get("SWINGTRADE")
    all_trades_daytrades = TradesDAO.get("DAYTRADE","RICO")

    for t in all_trades_swingtrades:

        # se o ativo esta na tabela de posicao
        if (posicaoDAO.get(t[4]) == []):
            posicaoDAO.save(t) # adiciona na tabela

        else: # ja estava na base
            valor_venda = posicaoDAO.adiciona_na_posicao_e_retorna_venda(t)

            if (valor_venda != None): # se teve venda, registra na tabela vendas
                vendasDAO.save(t[4],t[3], valor_venda)


if __name__ == "__main__":
    prepara_dados()
