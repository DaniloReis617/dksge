# :Simulador de jogos

Estrutura de Pastas e Arquivos
Estrutura de Pastas:
app.py: Arquivo principal que conterá o código do Streamlit para login e cadastro de novos usuários.
   DB/: Pasta para armazenar o arquivo de banco de dados (database.py) com as tabelas Usuarios, Backlog e onde deve ficar os dados que o usuário inputa por meio do upload.
   utils/: Pasta para arquivos utilitários (db_utils.py e auth_utils.py).
      db_utils.py: funções que manipulam o banco de dados com açoes de inclusão, edição, visualização e exclusão de dados.
      auth_utils.py: funções que lidam com autenticação e autorização.
   pages/: Pasta para os diferentes componentes de páginas do aplicativo (dashboard.py, listview.py).
      dashboard.py: 
         Fluxo de Caixa Operacional: Mede a quantidade de dinheiro gerado pelas operações normais da empresa.
         Taxa de Crescimento de Vendas: Indica a velocidade com que as vendas da empresa estão aumentando.
         Lucro Bruto e Margem de Lucro Bruto: Mostra a rentabilidade das vendas após subtrair o custo dos bens vendidos.
         Lucro Líquido e Margem de Lucro Líquido: Reflete o lucro total após todas as despesas.
         Fluxo de Caixa: Monitora o dinheiro que entra e sai da empresa.
         Giro de Contas a Pagar: Avalia a eficiência com que a empresa paga suas obrigações.
         Custo dos Bens Vendidos (COGS): Ajuda a entender os custos diretos associados à produção dos bens ou serviços vendidos pela empresa.
         Custo de Aquisição de Cliente (CAC): Calcula o custo total associado à aquisição de um novo cliente.
      listview.py: tabela editavel com os dados das transações cadastradas pelo usuário.

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run app.py
   ```
