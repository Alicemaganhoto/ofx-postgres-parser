import os
from contextlib import closing
from decimal import Decimal

import psycopg2
from dotenv import load_dotenv
from ofxparse import OfxParser


load_dotenv()

with open("extrato.ofx", "rb") as arquivo:
    ofx = OfxParser.parse(arquivo)

transacoes = ofx.account.statement.transactions

print("EXTRATO BANCÁRIO")
print("=" * 38)

entradas = Decimal("0")
saidas = Decimal("0")

for t in transacoes:
    descricao = t.memo or t.payee or "SEM DESCRIÇÃO"
    print(f"""
Data      : {t.date.strftime('%d/%m/%Y')}
Valor     : R$ {t.amount:.2f}
Descrição : {descricao}
--------------------------------------""")

    if t.amount > 0:
        entradas += t.amount
    else:
        saidas += t.amount

saldo = entradas + saidas

print(f"\nTotal de movimentações: {len(transacoes)}")
print(f"Entradas: R$ {entradas:.2f}")
print(f"Saídas:   R$ {saidas:.2f}")
print(f"Saldo:    R$ {saldo:.2f}")

configuracao_bd = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}
variaveis_ausentes = [nome for nome, valor in configuracao_bd.items() if not valor]
if variaveis_ausentes:
    raise ValueError(
        "Defina estas variáveis no arquivo .env: "
        + ", ".join(variaveis_ausentes)
    )

query_insercao = """
INSERT INTO movimentacoes (data_movimentacao, valor, descricao)
VALUES (%s, %s, %s)
ON CONFLICT (data_movimentacao, valor, descricao) DO NOTHING;
"""

with closing(psycopg2.connect(**configuracao_bd)) as conn:
    with conn:
        with conn.cursor() as cursor:
            for t in transacoes:
                data = t.date.strftime("%Y-%m-%d")
                descricao = t.memo or t.payee or "SEM DESCRIÇÃO"
                cursor.execute(query_insercao, (data, t.amount, descricao))

print("\n[BD] Movimentações registradas no PostgreSQL com sucesso!")
