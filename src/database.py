import sqlite3
import pandas as pd
import numpy as np
import os


def criar_banco():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_raiz = os.path.dirname(diretorio_atual)
    pasta_data = os.path.join(diretorio_raiz, "data")

    os.makedirs(pasta_data, exist_ok=True)
    caminho_db = os.path.join(pasta_data, "mock_producao.db")

    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordens_producao (
            id_ordem INTEGER PRIMARY KEY,
            data TEXT,
            linha_producao TEXT,
            produto TEXT,
            qtde_planejada INTEGER,
            qtde_produzida INTEGER,
            qtde_refugo INTEGER,
            horas_parada REAL,
            custo_padrao_unitario REAL,
            custo_real_unitario REAL,
            motivo_parada TEXT
        )
    """)

    dados = [
        ('2026-11-01', 'Linha 01', 'Produto A', 1000, 950,
         50, 1.5, 12.00, 13.50, 'Manutenção Corretiva'),
        ('2026-11-02', 'Linha 01', 'Produto A', 1000,
         980, 20, 0.5, 12.00, 12.20, 'Falta de Material'),
        ('2026-11-03', 'Linha 02', 'Produto B', 500,
         450, 40, 2.0, 25.00, 28.00, 'Setup de Máquina'),
        ('2026-11-04', 'Linha 02', 'Produto B', 500,
         490, 10, 0.2, 25.00, 25.50, 'Sem ocorrência'),
        ('2026-11-05', 'Linha 01', 'Produto A', 1000, 920,
         80, 3.0, 12.00, 14.80, 'Manutenção Corretiva'),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO ordens_producao 
        (data, linha_producao, produto, qtde_planejada, qtde_produzida, qtde_refugo, horas_parada, custo_padrao_unitario, custo_real_unitario, motivo_parada)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, dados)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    criar_banco()
    print("Banco de dados criado com sucesso!")
