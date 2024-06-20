import streamlit as st
import pandas as pd
import os
from datetime import datetime
import seaborn as sns  # Importar seaborn para melhorar o estilo dos gráficos
import matplotlib.pyplot as plt
from utils.db_utils import add_data_to_extrato_table, get_extrato_data  # Importa funções utilitárias de banco de dados

# Caminho para a pasta 'Extratos'
extrato_folder_path = 'Extratos'

# Função para obter o caminho do arquivo mais recente na pasta 'Extratos'
def get_latest_file_path(folder_path):
    list_of_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    if list_of_files:
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    return None

# Função para renderizar o dashboard
def render_dashboard(username, user_id):
    # Configuração inicial
    st.markdown(f"### Olá, {username}! Bem-vindo ao seu Dashboard.")

    # Upload do arquivo CSV
    uploaded_file = st.file_uploader("Upload do Extrato Bancário", type="csv")
    
    # Variável para armazenar o caminho do arquivo carregado
    file_path = None

    if uploaded_file is not None:
        # Contar o número de arquivos na pasta 'Extratos'
        num_files = len([name for name in os.listdir(extrato_folder_path) if os.path.isfile(os.path.join(extrato_folder_path, name))])

        # Gerar o nome do arquivo com o formato desejado
        today = datetime.now().strftime('%Y-%m-%d')
        file_name = f"Extrato_{num_files}_{today}.csv"

        # Salvar o arquivo na pasta 'Extratos', substituindo se já existir
        file_path = os.path.join(extrato_folder_path, file_name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Arquivo salvo com o nome: " + file_name)

        # Ler arquivo CSV da pasta 'Extratos' e exibir os dados
        df_upload = pd.read_csv(file_path)

        # Verificar se as colunas esperadas estão presentes no DataFrame
        expected_columns = ['Data', 'Transação', 'Tipo Transação', 'Identificação', 'Valor']
        if all(col in df_upload.columns for col in expected_columns):
            # Processamento dos dados conforme instruções fornecidas
            df_upload['Tipo Transação'] = df_upload['Tipo Transação'].str.upper()
            df_upload['Entrada'] = df_upload.apply(lambda x: x['Valor'] if x['Tipo Transação'] == 'CRÉDITO' else 0, axis=1)
            df_upload['Saída'] = df_upload.apply(lambda x: x['Valor'] if x['Tipo Transação'] == 'DÉBITO' else 0, axis=1)

            # Mapeamento de número do mês para nome em português
            meses = {
                1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
                5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
                9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
            }

            # Extrair o mês da coluna 'Data' e mapear para o nome em português
            df_upload['Mês'] = pd.to_datetime(df_upload['Data'], format='%d/%m/%Y').dt.month.map(meses)

            # Calcular saldo com base nos dados do upload
            df_upload['Saldo'] = df_upload['Entrada'] - df_upload['Saída']

            # Renomear colunas conforme dados fornecidos
            df_upload.rename(columns={'Data':'Data da Transação','Transação':'Transacao','Identificação':'Identificacao','Valor': 'Valor (R$)', 'Tipo Transação': 'Tipo de Transação'}, inplace=True)

            add_data_to_extrato_table(df_upload, user_id)  # Pass user_id to add_data_to_extrato_table

            # Call the get_extrato_data function to retrieve the data from the Extrato table
            df_extrato = get_extrato_data(user_id)

            # Delete the uploaded CSV file
            if os.path.exists(file_path):
                os.remove(file_path)
                st.write(f"Arquivo '{file_name}' excluído com sucesso.")
            else:
                st.write(f"Arquivo '{file_name}' não encontrado.")

            # Display the metrics and visualizations using the retrieved data
            col1, col2, col3 = st.columns([3, 3, 3])
            with col1:
                # Exibir resumos financeiros
                st.metric("Entrada", f"R$ {df_extrato['Entrada'].sum():,.2f}")
            with col2:
                st.metric("Saída", f"R$ {df_extrato['Saida'].sum():,.2f}")
            with col3:
                st.metric("Saldo", f"R$ {df_extrato['Saldo'].sum():,.2f}")

            # Gráficos
            st.header("Gráficos")
            
            # Gráficos
            st.header("Gráficos")

            # Estilo Seaborn
            sns.set_theme(style="whitegrid", font_scale=1.2, palette="pastel")

            # Gráfico de histograma para Entrada e Saída por mês
            plt.figure(figsize=(10, 6))
            sns.histplot(data=df_extrato, x='Mes', hue='Tipo de Transação', multiple='stack', edgecolor='white', alpha=0.7)
            plt.xlabel('Mês')
            plt.ylabel('Valor (R$)')
            plt.title('Entrada e Saída por Mês (R$)')
            plt.xticks(rotation=90)
            plt.legend(title='Tipo de Transação', loc='upper right', bbox_to_anchor=(1.05, 1))
            st.pyplot()

            # Gráfico de linha para Saldo acumulado por mês
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=df_extrato, x='Mês', y=df_extrato['Saldo'].cumsum(), marker='o', linestyle='-', color='#3498db', label='Saldo acumulado')
            plt.xlabel('Mês')
            plt.ylabel('Valor (R$)')
            plt.title('Saldo Acumulado por Mês (R$)')
            plt.xticks(rotation=90)
            plt.legend(loc='upper right', bbox_to_anchor=(1.05, 1))
            st.pyplot()

            with st.container():
                col1, col2, col3 = st.columns([0.5,9,0.5])
                with col2:
                    # Tabela Editável
                    st.header("Demonstração do Resultado do Exercício (DRE)")
                    st.dataframe(df_extrato)  # Utiliza dataframe em vez de data_editor

        else:
            st.error("O arquivo CSV não contém todas as colunas necessárias. Verifique o formato do arquivo e tente novamente.")
    else:
        st.info("Por favor, faça o upload de um arquivo CSV para continuar.")

# Executar o dashboard
if __name__ == '__main__':
    # Criar a pasta 'Extratos' se ela não existir
    if not os.path.exists(extrato_folder_path):
        os.makedirs(extrato_folder_path)

    username = "username"
    user_id = 1  # Substitua pelo ID do usuário real
    render_dashboard(username, user_id)
