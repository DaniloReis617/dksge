# :gestao_empresarial_app

Pasta do Projeto: gestao_empresarial_app/

app.py: Arquivo principal onde o código do Streamlit será escrito.
   db/: Pasta para arquivos relacionados ao banco de dados SQLite.
      database.db: Arquivo SQLite que armazena todos os dados.
      createdb.ipynb: Aquivo python para criar as tabelas com os campos no database.db
   utils/: Pasta para funções utilitárias e lógica de negócios.
      db_utils.py: Funções para conexão ao banco de dados, consultas SQL, etc.
      auth_utils.py: Funções para autenticação e gerenciamento de usuários.
   pages/: Pasta para separar diferentes páginas do aplicativo.
      dashboard.py: Código relacionado ao dashboard principal.
      usuarios.py: Página para gestão de usuários.
      clientes.py: Página para gestão de clientes.
      vendas.py: Página para gestão de vendas.
      estoque.py: Página para gestão de estoque.
      funconarios.py: Página para gestão de funcionários. 

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
