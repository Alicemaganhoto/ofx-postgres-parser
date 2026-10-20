# OFX PostgreSQL Parser

Lê as transações de `extrato.ofx`, mostra um resumo no terminal e grava as
movimentações no PostgreSQL. Transações repetidas são ignoradas.

## Configuração

1. Crie e ative um ambiente virtual Python.
2. Instale as dependências:

   ```powershell
   pip install -r requirements.txt
   ```

3. Copie `.env.example` para `.env` e informe os dados da conexão PostgreSQL.
4. Crie a tabela no banco configurado:

   ```powershell
   psql -U postgres -d postgres -f schema.sql
   ```

   Ajuste usuário e banco conforme os valores do seu `.env`.
5. Coloque o extrato OFX na raiz do projeto com o nome `extrato.ofx`.
6. Execute:

   ```powershell
   python main.py
   ```

Não compartilhe seu `.env` nem extratos bancários. Esses arquivos são ignorados
pelo Git.
