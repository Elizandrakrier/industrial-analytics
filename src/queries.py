import sqlite3
import pandas as pd
import os


def carregar_dados_financeiros_producao():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_raiz = os.path.dirname(diretorio_atual)
    caminho_db = os.path.join(diretorio_raiz, "data", "mock_producao.db")

    conn = sqlite3.connect(caminho_db)

    query = """
        SELECT 
            data,
            linha_producao,
            produto,
            qtde_planejada,
            qtde_produzida,
            qtde_refugo,
            horas_parada,
            motivo_parada,
            ROUND((CAST(qtde_produzida AS REAL) / qtde_planejada) * 100, 2) as eficiencia_percentual,
            ROUND(qtde_refugo * custo_padrao_unitario, 2) as perda_financeira_refugo,
            ROUND((qtde_produzida * custo_real_unitario) - (qtde_produzida * custo_padrao_unitario), 2) as desvio_custo_total
        FROM ordens_producao
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df
