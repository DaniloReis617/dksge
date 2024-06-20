# :Simulador de jogos

Estrutura de Pastas e Arquivos
Estrutura de Pastas:
app.py                 # Arquivo principal que contém o código do Streamlit para login e cadastro de novos usuários.
DB/                    # Pasta para armazenar o arquivo de banco de dados (database.py) e os dados do usuário.
   database.py         # Arquivo que cria e manipula as tabelas do banco de dados SQLite.
   database.db         # Arquivo do banco de dados SQLite (criado automaticamente pelo database.py).
utils/                 # Pasta para arquivos utilitários.
   auth_utils.py       # Funções que lidam com autenticação e autorização de usuários.
   db_utils.py         # Funções que manipulam o banco de dados, incluindo inserção, edição, visualização e exclusão de dados.
pages/                 # Pasta para os diferentes componentes de páginas do aplicativo.
   dashboard.py        # Página principal do dashboard com gráficos e métricas financeiras.
Extratos/              # Pasta para armazenar os arquivos de extratos bancários carregados pelo usuário.
   (arquivos CSV)      # Arquivos CSV carregados pelo usuário contendo os dados das transações bancárias.

Explicações detalhadas:
Arquivo app.py:

Este é o arquivo principal que contém o código do Streamlit para a aplicação.
Ele incluirá funcionalidades de login, cadastro de novos usuários e navegação entre diferentes páginas do aplicativo.
Pasta DB/:

database.py: Arquivo que contém o código para criação e manipulação das tabelas do banco de dados SQLite (database.db).
database.db: Arquivo do banco de dados SQLite onde serão armazenados os dados dos usuários e suas transações financeiras.
Pasta utils/:

auth_utils.py: Arquivo com funções relacionadas à autenticação e autorização de usuários.
db_utils.py: Arquivo com funções utilitárias para manipulação do banco de dados, incluindo inserção, edição, visualização e exclusão de dados.
Pasta pages/:

dashboard.py: Página principal do dashboard que apresenta gráficos e métricas financeiras importantes para o usuário, como Fluxo de Caixa Operacional, Lucro Líquido, etc.
Pasta Extratos/:

Pasta destinada a armazenar os arquivos CSV carregados pelo usuário contendo os dados dos extratos bancários.
Os arquivos CSV carregados serão processados e as informações relevantes serão inseridas no banco de dados (database.db) por meio do db_utils.py.
Considerações:
Certifique-se de configurar corretamente as dependências (requirements.txt) para o ambiente virtual do seu projeto.
Gerencie o fluxo de dados entre as páginas (app.py, dashboard.py) e os utilitários (db_utils.py, auth_utils.py) para garantir uma aplicação fluida e eficiente.

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run app.py
   ```
