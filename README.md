# :Simulador de jogos

Estrutura de Pastas e Arquivos
Estrutura de Pastas:
app.py: Arquivo principal que conterá o código do Streamlit.
   DB/: Pasta para armazenar o arquivo de banco de dados (database.py) com as tabelas Usuarios, Jogos e Backlog.
   utils/: Pasta para arquivos utilitários (db_utils.py e auth_utils.py).
   pages/: Pasta para os diferentes componentes de páginas do aplicativo (dashboard.py, cadastro_jogos.py, listview_jogos.py).

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
